"""LinkedIn job scraper implementation."""

import re
import time
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings
from src.models.job import Job, SearchParameters
from src.scraper.browser_manager import BrowserManager
from src.utils.logger import logger
from src.utils.rate_limiter import RateLimiter


class LinkedInScraper:
    """Scrapes job postings from LinkedIn."""

    def __init__(self, headless: bool = True):
        """
        Initialize scraper.

        Args:
            headless: Whether to run browser in headless mode
        """
        self.browser = BrowserManager(headless=headless)
        self.rate_limiter = RateLimiter(
            min_delay=settings.min_delay,
            max_delay=settings.max_delay,
            random_delay=settings.random_delay
        )
        self.jobs: List[Job] = []

    def scrape(self, search_params: SearchParameters) -> List[Job]:
        """
        Scrape jobs based on search parameters.

        New workflow:
        1. Collect all job links from search pages
        2. Open each link in a separate tab sequentially
        3. Extract job info from each tab
        4. Store and return all jobs

        Args:
            search_params: Search parameters

        Returns:
            List of scraped jobs
        """
        logger.info(f"Starting job scrape: {search_params.keywords} in {search_params.location or 'Any location'}")

        try:
            # Start browser
            self.browser.start()

            # Build search URL
            search_url = search_params.build_url()
            logger.info(f"Search URL: {search_url}")

            # Step 1: Collect all job links from search pages
            logger.info("Step 1: Collecting all job links from search pages...")
            job_links = self._collect_all_job_links(search_url, search_params.max_jobs)

            if not job_links:
                logger.warning("No job links found")
                return []

            logger.info(f"Found {len(job_links)} job links")

            # Step 2 & 3: Open each link in a separate tab and extract job info
            logger.info("Step 2: Opening each job link in separate tabs and extracting data...")
            jobs = self._scrape_jobs_from_links(job_links)

            logger.info(f"Scraping complete! Total jobs scraped: {len(jobs)}")
            self.jobs = jobs
            return jobs

        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return self.jobs

        finally:
            self.browser.close()

    def _collect_all_job_links(self, search_url: str, max_jobs: int) -> List[str]:
        """
        Collect all job links from search result pages.

        Args:
            search_url: LinkedIn search URL
            max_jobs: Maximum number of job links to collect

        Returns:
            List of job URLs
        """
        all_job_links = []
        page_num = 0

        try:
            # Navigate to search page
            if not self.browser.get(search_url):
                logger.error("Failed to load search page")
                return []

            # Wait for page to load
            time.sleep(3)

            # Handle any popups that might block scrolling
            self._handle_popups()

            # Wait for job listings to load
            time.sleep(2)

            while len(all_job_links) < max_jobs:
                logger.info(f"Collecting links from page {page_num + 1}...")

                # Scroll to load more jobs and handle popups
                if page_num > 0:
                    time.sleep(2)

                self._scroll_to_load_more_jobs()

                # Get job links on current page
                page_links = self._extract_job_links_from_page()

                if not page_links:
                    logger.warning("No job links found on page")
                    break

                # Add new links (avoid duplicates)
                for link in page_links:
                    if link not in all_job_links and len(all_job_links) < max_jobs:
                        all_job_links.append(link)
                        logger.debug(f"Added job link {len(all_job_links)}/{max_jobs}: {link}")

                logger.info(f"Collected {len(all_job_links)} links so far")

                # Check if we have enough links
                if len(all_job_links) >= max_jobs:
                    break

                # Go to next page
                if not self._go_to_next_page():
                    logger.info("No more pages available")
                    break

                page_num += 1
                time.sleep(2)

            return all_job_links[:max_jobs]

        except Exception as e:
            logger.error(f"Error collecting job links: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return all_job_links

    def _extract_job_links_from_page(self) -> List[str]:
        """
        Extract all job links from the current search results page.

        Returns:
            List of job URLs
        """
        job_links = []

        try:
            # Multiple selectors for job cards
            card_selectors = [
                "div.job-search-card",
                "div.base-card",
                "li.jobs-search-results__list-item",
                "div.jobs-search__results-list li"
            ]

            cards = []
            for selector in card_selectors:
                try:
                    cards = self.browser.driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards:
                        logger.debug(f"Found {len(cards)} job cards using selector: {selector}")
                        break
                except:
                    continue

            if not cards:
                logger.warning("Could not find job cards with any selector")
                return []

            # Extract links from each card
            for card in cards:
                try:
                    # Find job link in card
                    link_elem = card.find_element(By.CSS_SELECTOR, 'a[href*="/jobs/view/"]')
                    job_link = link_elem.get_attribute('href')

                    if job_link:
                        # Clean URL
                        if not job_link.startswith('http'):
                            job_link = f"https://www.linkedin.com{job_link}"

                        # Remove tracking parameters
                        job_link = job_link.split('?')[0]

                        job_links.append(job_link)

                except Exception as e:
                    logger.debug(f"Could not extract link from card: {e}")
                    continue

            logger.debug(f"Extracted {len(job_links)} job links from current page")
            return job_links

        except Exception as e:
            logger.error(f"Error extracting job links from page: {e}")
            return job_links

    def _scrape_jobs_from_links(self, job_links: List[str]) -> List[Job]:
        """
        Open each job link in a separate tab and extract job information.

        Args:
            job_links: List of job URLs to scrape

        Returns:
            List of Job objects
        """
        jobs = []

        try:
            # Store the main window handle
            main_window = self.browser.driver.current_window_handle

            for idx, job_link in enumerate(job_links):
                try:
                    logger.info(f"Processing job {idx + 1}/{len(job_links)}: {job_link}")

                    # Open job link in a new tab
                    self.browser.driver.execute_script(f"window.open('{job_link}', '_blank');")

                    # Switch to the new tab
                    all_windows = self.browser.driver.window_handles
                    new_tab = all_windows[-1]
                    self.browser.driver.switch_to.window(new_tab)

                    # Wait for page to load
                    time.sleep(3)

                    # Handle popups
                    self._handle_popups()

                    # Extract job data from the tab
                    job = self._extract_detailed_job_data(job_link)

                    if job:
                        jobs.append(job)
                        logger.info(f"Successfully scraped: {job.title} at {job.company}")
                    else:
                        logger.warning(f"Could not extract job data from: {job_link}")

                    # Close the current tab
                    self.browser.driver.close()

                    # Switch back to main window
                    self.browser.driver.switch_to.window(main_window)

                    # Rate limiting
                    self.rate_limiter.wait()

                except Exception as e:
                    logger.error(f"Error processing job link {job_link}: {e}")

                    # Try to close tab and switch back to main window
                    try:
                        self.browser.driver.close()
                        self.browser.driver.switch_to.window(main_window)
                    except:
                        pass

                    continue

            return jobs

        except Exception as e:
            logger.error(f"Error scraping jobs from links: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return jobs

    def _handle_popups(self):
        """Detect and close LinkedIn popups that might block interaction."""
        try:
            logger.debug("Checking for popups...")

            # Common LinkedIn popup selectors
            popup_selectors = [
                # Sign-in modal
                'button[data-tracking-control-name*="public_jobs_contextual-sign-in-modal_modal_dismiss"]',
                'button[aria-label="Dismiss"]',
                'button.modal__dismiss',

                # Cookie consent
                'button[action-type="ACCEPT"]',
                'button.artdeco-global-alert-action',

                # Generic close buttons
                'button[data-test-modal-close-btn]',
                '.modal button[aria-label*="lose"]',
                '.artdeco-modal__dismiss',

                # Sign-in prompts
                '.contextual-sign-in-modal__modal-dismiss',
                'button[data-tracking-control-name="public_jobs_contextual-sign-in-modal_modal_dismiss"]'
            ]

            popups_closed = 0
            for selector in popup_selectors:
                try:
                    elements = self.browser.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            element.click()
                            popups_closed += 1
                            logger.info(f"Closed popup: {selector}")
                            time.sleep(0.5)
                except:
                    continue

            if popups_closed > 0:
                logger.info(f"Closed {popups_closed} popup(s)")
                time.sleep(1)  # Wait for popups to fully close
            else:
                logger.debug("No popups detected")

        except Exception as e:
            logger.warning(f"Error handling popups (non-critical): {e}")

    def _scroll_to_load_more_jobs(self):
        """Scroll down the page to load more job listings."""
        try:
            logger.debug("Scrolling to load more jobs...")

            # Close any popups before scrolling
            self._handle_popups()

            # Scroll down in increments
            for i in range(3):
                self.browser.driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(0.5)

                # Check for and close popups that might appear during scroll
                self._handle_popups()

            # Scroll back up a bit
            self.browser.driver.execute_script("window.scrollBy(0, -400);")
            time.sleep(0.5)

        except Exception as e:
            logger.warning(f"Error during scroll (non-critical): {e}")

    def _extract_job_id(self, url: str) -> Optional[str]:
        """
        Extract job ID from LinkedIn URL.

        Args:
            url: LinkedIn job URL

        Returns:
            Job ID or None
        """
        try:
            # Pattern: /jobs/view/1234567890/
            match = re.search(r'/jobs/view/(\d+)', url)
            if match:
                return match.group(1)

            # Alternative: from query parameter
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            if 'currentJobId' in params:
                return params['currentJobId'][0]

            return None

        except Exception as e:
            logger.debug(f"Could not extract job ID: {e}")
            return None

    def _go_to_next_page(self) -> bool:
        """
        Navigate to next page of results.

        Returns:
            True if successful, False if no next page
        """
        try:
            # Find pagination buttons
            next_button_selectors = [
                'button[aria-label="View next page"]',
                'button[aria-label="Next"]',
                'li.artdeco-pagination__indicator--number:last-child button',
                'button.artdeco-pagination__button--next'
            ]

            for selector in next_button_selectors:
                try:
                    next_button = self.browser.driver.find_element(By.CSS_SELECTOR, selector)

                    # Check if button is enabled
                    if next_button.is_enabled() and next_button.is_displayed():
                        # Scroll to button
                        self.browser.driver.execute_script(
                            "arguments[0].scrollIntoView(true);",
                            next_button
                        )
                        time.sleep(1)

                        # Click
                        next_button.click()
                        logger.info("Navigated to next page")

                        # Wait for page to load
                        time.sleep(3)
                        return True

                except NoSuchElementException:
                    continue

            logger.info("No next page button found")
            return False

        except Exception as e:
            logger.error(f"Error navigating to next page: {e}")
            return False

    def _extract_detailed_job_data(self, job_url: str) -> Optional[Job]:
        """
        Extract comprehensive job information from job detail page.

        Args:
            job_url: LinkedIn job URL

        Returns:
            Job object with all available fields or None
        """
        try:
            logger.debug(f"Extracting detailed data from: {job_url}")

            # Get page HTML
            soup = BeautifulSoup(self.browser.driver.page_source, 'lxml')

            # Extract job ID
            job_id = self._extract_job_id(job_url)

            # Extract job title
            title_selectors = [
                '.top-card-layout__title',
                'h1.topcard__title',
                'h2.topcard__title',
                'h1',
                '.job-details-jobs-unified-top-card__job-title'
            ]
            title = None
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break

            if not title:
                logger.warning("Could not extract job title")
                return None

            # Extract company name
            company_selectors = [
                '.topcard__org-name-link',
                '.topcard__flavor--black-link',
                'a.topcard__org-name-link',
                '.job-details-jobs-unified-top-card__company-name'
            ]
            company = None
            for selector in company_selectors:
                company_elem = soup.select_one(selector)
                if company_elem:
                    company = company_elem.get_text(strip=True)
                    break

            if not company:
                company = "Unknown Company"

            # Extract location
            location_selectors = [
                '.topcard__flavor--bullet',
                '.job-details-jobs-unified-top-card__bullet'
            ]
            location = None
            for selector in location_selectors:
                location_elem = soup.select_one(selector)
                if location_elem:
                    location = location_elem.get_text(strip=True)
                    break

            if not location:
                location = "Location not specified"

            # Extract description
            description = None
            desc_selectors = [
                '.show-more-less-html__markup',
                '.description__text',
                '.job-details-jobs-unified-top-card__job-description'
            ]
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    description = desc_elem.get_text(strip=True)[:2000]  # Limit to 2000 chars
                    break

            # Extract skills
            skills = []
            skills_selectors = [
                '.job-details-skill-match-status-list li',
                '.job-details-how-you-match__skills-item',
                '.job-details-jobs-unified-top-card__job-insight span'
            ]
            for selector in skills_selectors:
                skills_section = soup.select(selector)
                if skills_section:
                    skills = [skill.get_text(strip=True) for skill in skills_section if skill.get_text(strip=True)]
                    if skills:
                        break

            # Extract salary range
            salary_range = None
            salary_selectors = [
                '.salary',
                '.compensation__salary',
                '.job-details-jobs-unified-top-card__job-insight--highlight'
            ]
            for selector in salary_selectors:
                salary_elem = soup.select_one(selector)
                if salary_elem:
                    text = salary_elem.get_text(strip=True)
                    if '$' in text or 'salary' in text.lower():
                        salary_range = text
                        break

            # Extract applicants count
            applicants_count = None
            applicants_selectors = [
                '.num-applicants__caption',
                'figure',
                '.job-details-jobs-unified-top-card__applicant-count'
            ]
            for selector in applicants_selectors:
                applicants_elem = soup.select_one(selector)
                if applicants_elem:
                    text = applicants_elem.get_text(strip=True)
                    if 'applicant' in text.lower():
                        applicants_count = text
                        break

            # Extract employment type and experience level from criteria items
            employment_type = None
            experience_level = None
            criteria_items = soup.select('.description__job-criteria-item')

            for item in criteria_items:
                header = item.select_one('.description__job-criteria-subheader')
                value = item.select_one('.description__job-criteria-text')

                if header and value:
                    header_text = header.get_text(strip=True).lower()
                    value_text = value.get_text(strip=True)

                    if 'employment type' in header_text or 'job type' in header_text:
                        employment_type = value_text
                    elif 'seniority level' in header_text or 'experience' in header_text:
                        experience_level = value_text

            # Extract posted date
            posted_date = None
            posted_selectors = [
                'time',
                '.posted-time-ago__text',
                '.job-details-jobs-unified-top-card__posted-date'
            ]
            for selector in posted_selectors:
                posted_elem = soup.select_one(selector)
                if posted_elem:
                    # Try to get datetime attribute first
                    if posted_elem.has_attr('datetime'):
                        posted_date = posted_elem['datetime']
                    else:
                        posted_date = posted_elem.get_text(strip=True)
                    if posted_date:
                        break

            # Create Job object with all extracted data
            job = Job(
                title=title,
                company=company,
                location=location,
                job_url=job_url,
                job_id=job_id,
                description=description,
                skills=skills,
                employment_type=employment_type,
                experience_level=experience_level,
                posted_date=posted_date,
                applicants_count=applicants_count,
                salary_range=salary_range
            )

            logger.debug(f"Successfully extracted detailed data for: {title}")
            return job

        except Exception as e:
            logger.error(f"Error extracting detailed job data: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None

    def enrich_job_details(self, job: Job) -> Job:
        """
        Enrich job with detailed information by visiting job page.

        Args:
            job: Job object to enrich

        Returns:
            Enriched job object
        """
        try:
            logger.debug(f"Enriching job details for: {job.title}")

            # Navigate to job page
            if not self.browser.get(job.job_url):
                return job

            time.sleep(2)

            # Get page HTML
            soup = BeautifulSoup(self.browser.driver.page_source, 'lxml')

            # Extract description
            desc_elem = soup.select_one('.description__text, .show-more-less-html__markup')
            if desc_elem:
                job.description = desc_elem.get_text(strip=True)[:1000]  # Limit to 1000 chars

            # Extract skills (if available)
            skills_section = soup.select('.job-details-skill-match-status-list li, .job-details-how-you-match__skills-item')
            if skills_section:
                job.skills = [skill.get_text(strip=True) for skill in skills_section]

            # Extract salary (if available)
            salary_elem = soup.select_one('.salary, .compensation__salary')
            if salary_elem:
                job.salary_range = salary_elem.get_text(strip=True)

            # Extract applicants count
            applicants_elem = soup.select_one('.num-applicants__caption, figure')
            if applicants_elem:
                job.applicants_count = applicants_elem.get_text(strip=True)

            # Extract employment type and experience level
            criteria = soup.select('.description__job-criteria-item')
            for item in criteria:
                header = item.select_one('.description__job-criteria-subheader')
                value = item.select_one('.description__job-criteria-text')

                if header and value:
                    header_text = header.get_text(strip=True).lower()
                    value_text = value.get_text(strip=True)

                    if 'employment type' in header_text:
                        job.employment_type = value_text
                    elif 'seniority level' in header_text or 'experience' in header_text:
                        job.experience_level = value_text

            return job

        except Exception as e:
            logger.error(f"Error enriching job details: {e}")
            return job

    def get_jobs(self) -> List[Job]:
        """Get list of scraped jobs."""
        return self.jobs

    def clear_jobs(self):
        """Clear scraped jobs list."""
        self.jobs = []
