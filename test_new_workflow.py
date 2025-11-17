#!/usr/bin/env python3
"""
Test script to explore new LinkedIn job scraper workflow.
This simulates what MCP server would do and documents each action.

New Workflow:
1. Navigate to job search page
2. List down job cards displayed on left
3. Click on each job card in same tab (don't open new tab)
4. On right section, click 'See More' link to expand content
5. Get info and store for each job
6. Once done for 1st job, do for 2nd job and continue as per limit
7. Generate report for all jobs
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class LinkedInWorkflowTester:
    """Test and document LinkedIn job scraping workflow."""

    def __init__(self, headless: bool = False):
        """Initialize tester with browser."""
        self.headless = headless
        self.driver = None
        self.wait = None
        self.workflow_log = []
        self.jobs_data = []

    def log_action(self, action: str, details: dict = None):
        """Log each action for documentation."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details or {}
        }
        self.workflow_log.append(log_entry)
        print(f"\n📝 {action}")
        if details:
            for key, value in details.items():
                print(f"   {key}: {value}")

    def start_browser(self):
        """Step 0: Start browser and configure."""
        print("\n" + "="*70)
        print("STEP 0: Starting Browser")
        print("="*70)

        options = Options()
        if self.headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 10)

        self.log_action("Browser started", {
            "headless": self.headless,
            "window_size": "1920x1080"
        })

    def navigate_to_job_search(self, keywords: str = "Python Developer", location: str = ""):
        """Step 1: Navigate to job search page."""
        print("\n" + "="*70)
        print("STEP 1: Navigate to Job Search Page")
        print("="*70)

        # Build search URL
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords.replace(' ', '%20')}"
        if location:
            search_url += f"&location={location.replace(' ', '%20')}"

        self.driver.get(search_url)
        time.sleep(3)  # Wait for page load

        # Take screenshot
        self.driver.save_screenshot("output/step1_search_page.png")

        self.log_action("Navigated to job search", {
            "url": search_url,
            "page_title": self.driver.title,
            "screenshot": "output/step1_search_page.png"
        })

        # Handle any popups
        self._close_popups()

        return search_url

    def _close_popups(self):
        """Close any LinkedIn popups that might appear."""
        popup_selectors = [
            'button[data-tracking-control-name*="public_jobs_contextual-sign-in-modal_modal_dismiss"]',
            'button[aria-label="Dismiss"]',
            'button.modal__dismiss',
            '.contextual-sign-in-modal__modal-dismiss'
        ]

        for selector in popup_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.is_displayed():
                        elem.click()
                        time.sleep(0.5)
                        self.log_action("Closed popup", {"selector": selector})
            except:
                pass

    def list_job_cards(self) -> List[dict]:
        """Step 2: List down job cards displayed on left."""
        print("\n" + "="*70)
        print("STEP 2: List Job Cards on Left Panel")
        print("="*70)

        # Try different selectors for job cards
        job_card_selectors = [
            "ul.jobs-search__results-list > li",
            "div.jobs-search-results__list-item",
            "div.job-search-card",
            "li.jobs-search-results__list-item",
            "div.base-card"
        ]

        job_cards = []
        working_selector = None

        for selector in job_card_selectors:
            try:
                cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if cards and len(cards) > 0:
                    job_cards = cards
                    working_selector = selector
                    break
            except:
                continue

        self.log_action("Found job cards", {
            "working_selector": working_selector,
            "count": len(job_cards),
            "total_selectors_tried": len(job_card_selectors)
        })

        # List basic info about each card
        cards_info = []
        for idx, card in enumerate(job_cards[:10], 1):  # Limit to first 10 for testing
            try:
                html = card.get_attribute('outerHTML')
                soup = BeautifulSoup(html, 'lxml')

                # Try to extract basic info from card
                title_elem = soup.select_one('h3, .base-search-card__title, .job-search-card__title, a.base-card__full-link')
                company_elem = soup.select_one('h4, .base-search-card__subtitle, .job-search-card__company-name')

                title = title_elem.get_text(strip=True) if title_elem else f"Job {idx}"
                company = company_elem.get_text(strip=True) if company_elem else "Unknown"

                card_info = {
                    "index": idx,
                    "title": title,
                    "company": company,
                    "element": card
                }
                cards_info.append(card_info)

                print(f"   {idx}. {title} at {company}")

            except Exception as e:
                print(f"   {idx}. [Could not extract info: {e}]")

        # Take screenshot
        self.driver.save_screenshot("output/step2_job_cards_list.png")
        self.log_action("Listed job cards", {
            "screenshot": "output/step2_job_cards_list.png",
            "cards_found": len(cards_info)
        })

        return cards_info

    def click_job_card(self, card_element, index: int):
        """Step 3: Click on job card to load right panel (without navigation)."""
        print(f"\n{'='*70}")
        print(f"STEP 3: Click Job Card #{index} (Load Right Panel)")
        print("="*70)

        try:
            # Scroll card into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_element)
            time.sleep(0.5)

            # LinkedIn loads job details when you click on certain parts of the card
            # Try clicking title/info divs which trigger panel without navigation

            clicked = False
            working_selector = None

            # Approach 1: Click on the info/title div (usually triggers panel)
            clickable_selectors = [
                'div.base-search-card__info',  # Info container
                'h3.base-search-card__title',  # Title
                'div.job-card-container__metadata-wrapper',  # Metadata wrapper
                'img',  # Company logo
            ]

            for selector in clickable_selectors:
                try:
                    element = card_element.find_element(By.CSS_SELECTOR, selector)
                    if element and element.is_displayed():
                        # Regular click to trigger LinkedIn's event handlers
                        element.click()
                        time.sleep(3)  # Wait for right panel to load
                        clicked = True
                        working_selector = selector
                        print(f"   ✅ Clicked: {selector}")
                        break
                except Exception as e:
                    continue

            # Approach 2: Click the card (li) element itself
            if not clicked:
                try:
                    card_element.click()
                    time.sleep(3)
                    working_selector = "li_card_element"
                    clicked = True
                    print(f"   ✅ Clicked: card element directly")
                except:
                    pass

            self.log_action(f"Clicked job card #{index} to load right panel", {
                "working_selector": working_selector,
                "wait_time": "3 seconds"
            })

            # Take screenshot after click
            self.driver.save_screenshot(f"output/step3_job_{index}_right_panel.png")

            return True

        except Exception as e:
            self.log_action(f"Failed to click job card #{index}", {
                "error": str(e)
            })
            return False

    def expand_see_more(self, job_index: int) -> bool:
        """Step 4: Click 'See More' link to expand content on RIGHT PANEL."""
        print(f"\n{'='*70}")
        print(f"STEP 4: Click 'See More' on Right Panel (Job #{job_index})")
        print("="*70)

        # Focus on right panel selectors for "See More" button
        see_more_selectors = [
            'button.show-more-less-html__button--more',
            'button.show-more-less-html__button',
            'button[aria-label*="Show more"]',
            'button[aria-label*="see more"]',
            '.show-more-less-html button',
            'div.show-more-less-html__markup ~ button'
        ]

        expanded = False
        working_selector = None

        for selector in see_more_selectors:
            try:
                # Look for See More button in the right panel
                see_more_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)

                for btn in see_more_buttons:
                    if btn.is_displayed() and 'more' in btn.text.lower():
                        # Scroll into view
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                        time.sleep(0.5)

                        # Click
                        btn.click()
                        time.sleep(1.5)

                        expanded = True
                        working_selector = selector
                        print(f"   ✅ Clicked 'See More' button: {btn.text}")
                        break

                if expanded:
                    break

            except Exception as e:
                continue

        if expanded:
            self.log_action(f"Expanded 'See More' content for job #{job_index}", {
                "working_selector": working_selector,
                "location": "right panel"
            })
            self.driver.save_screenshot(f"output/step4_job_{job_index}_expanded.png")
        else:
            self.log_action(f"'See More' button not found for job #{job_index}", {
                "note": "Content may already be fully visible or selector needs update"
            })

        return expanded

    def extract_job_details(self, job_index: int) -> dict:
        """Step 5: Extract detailed job information from RIGHT PANEL."""
        print(f"\n{'='*70}")
        print(f"STEP 5: Extract Job Details from Right Panel (Job #{job_index})")
        print("="*70)

        # Wait a moment for content to be ready
        time.sleep(1)

        # Get page source - focus on right panel
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        # Try to identify right panel container
        right_panel_selectors = [
            'div.job-view-layout',
            'div.jobs-details',
            'section.jobs-details__main-content',
            'div.jobs-search__job-details'
        ]

        right_panel = None
        for selector in right_panel_selectors:
            panel = soup.select_one(selector)
            if panel:
                right_panel = panel
                print(f"   📍 Found right panel: {selector}")
                break

        # If we found right panel, search within it; otherwise search whole page
        search_context = right_panel if right_panel else soup

        job_data = {
            "index": job_index,
            "scraped_at": datetime.now().isoformat()
        }

        # Extract job title (from right panel)
        title_selectors = [
            '.top-card-layout__title',
            'h1.topcard__title',
            'h2.topcard__title',
            '.job-details-jobs-unified-top-card__job-title',
            'h1',
            'h2'
        ]
        for selector in title_selectors:
            elem = search_context.select_one(selector)
            if elem:
                job_data['title'] = elem.get_text(strip=True)
                break

        # Extract company (from right panel)
        company_selectors = [
            '.topcard__org-name-link',
            'a.topcard__org-name-link',
            '.job-details-jobs-unified-top-card__company-name',
            '.topcard__flavor--black-link',
            'a.app-aware-link'
        ]
        for selector in company_selectors:
            elem = search_context.select_one(selector)
            if elem:
                job_data['company'] = elem.get_text(strip=True)
                break

        # Extract location (from right panel)
        location_selectors = [
            '.topcard__flavor--bullet',
            '.job-details-jobs-unified-top-card__bullet',
            'span.topcard__flavor--bullet',
            'span.topcard__flavor'
        ]
        for selector in location_selectors:
            elem = search_context.select_one(selector)
            if elem:
                job_data['location'] = elem.get_text(strip=True)
                break

        # Extract description (from right panel - after See More)
        desc_selectors = [
            '.show-more-less-html__markup',
            '.description__text',
            '.job-details-jobs-unified-top-card__job-description',
            'div.show-more-less-html'
        ]
        for selector in desc_selectors:
            elem = search_context.select_one(selector)
            if elem:
                job_data['description'] = elem.get_text(strip=True)[:1000]  # First 1000 chars
                job_data['description_full_length'] = len(elem.get_text(strip=True))
                break

        # Extract job criteria (employment type, experience level, etc.)
        criteria_items = search_context.select('.description__job-criteria-item')
        criteria = {}
        for item in criteria_items:
            header = item.select_one('.description__job-criteria-subheader')
            value = item.select_one('.description__job-criteria-text')
            if header and value:
                criteria[header.get_text(strip=True)] = value.get_text(strip=True)
        job_data['criteria'] = criteria

        # Extract skills
        skills = []
        skill_selectors = [
            '.job-details-skill-match-status-list li',
            '.job-details-how-you-match__skills-item',
            'li.job-details-skill-match-status-list__unmatched-skill'
        ]
        for selector in skill_selectors:
            skill_elems = search_context.select(selector)
            if skill_elems:
                skills = [s.get_text(strip=True) for s in skill_elems]
                break
        job_data['skills'] = skills

        # Extract applicants count
        applicants_selectors = [
            '.num-applicants__caption',
            'figure',
            '.job-details-jobs-unified-top-card__applicant-count',
            'span.num-applicants__caption'
        ]
        for selector in applicants_selectors:
            elem = search_context.select_one(selector)
            if elem and 'applicant' in elem.get_text().lower():
                job_data['applicants'] = elem.get_text(strip=True)
                break

        # Extract posted date
        posted_selectors = [
            'time',
            '.posted-time-ago__text',
            '.job-details-jobs-unified-top-card__posted-date',
            'span.posted-time-ago__text'
        ]
        for selector in posted_selectors:
            elem = search_context.select_one(selector)
            if elem:
                job_data['posted_date'] = elem.get_text(strip=True)
                break

        # Extract job URL from current visible job
        # Look for job link in the page
        job_link_elem = soup.select_one('a[href*="/jobs/view/"]')
        if job_link_elem and 'href' in job_link_elem.attrs:
            job_url = job_link_elem['href']
            if not job_url.startswith('http'):
                job_url = f"https://www.linkedin.com{job_url}"
            job_data['url'] = job_url
        else:
            job_data['url'] = self.driver.current_url

        # Log what we extracted
        self.log_action(f"Extracted job #{job_index} details", {
            "title": job_data.get('title', 'N/A'),
            "company": job_data.get('company', 'N/A'),
            "fields_extracted": len([k for k, v in job_data.items() if v])
        })

        print(f"\n   ✅ Title: {job_data.get('title', 'N/A')}")
        print(f"   ✅ Company: {job_data.get('company', 'N/A')}")
        print(f"   ✅ Location: {job_data.get('location', 'N/A')}")
        print(f"   ✅ Skills: {len(job_data.get('skills', []))} found")
        print(f"   ✅ Description: {len(job_data.get('description', ''))} characters")

        return job_data

    def test_workflow(self, keywords: str = "Python Developer", max_jobs: int = 5):
        """Test the complete workflow for multiple jobs."""
        print("\n" + "="*70)
        print("LINKEDIN JOB SCRAPER - NEW WORKFLOW TEST")
        print("="*70)

        try:
            # Step 0: Start browser
            self.start_browser()

            # Step 1: Navigate to search page
            self.navigate_to_job_search(keywords)

            # Step 2: List job cards
            job_cards = self.list_job_cards()

            if not job_cards:
                print("\n❌ No job cards found!")
                return

            # Limit to max_jobs
            job_cards = job_cards[:max_jobs]

            # Steps 3-5: For each job card
            for idx in range(min(len(job_cards), max_jobs)):
                print(f"\n{'='*70}")
                print(f"PROCESSING JOB {idx+1}/{min(len(job_cards), max_jobs)}")
                print("="*70)

                # RE-FIND job cards to avoid stale elements
                job_card_selector = "ul.jobs-search__results-list > li"
                current_cards = self.driver.find_elements(By.CSS_SELECTOR, job_card_selector)

                if idx < len(current_cards):
                    # Step 3: Click job card to load right panel
                    if self.click_job_card(current_cards[idx], idx+1):

                        # Step 4: Expand "See More" on right panel
                        self.expand_see_more(idx+1)

                        # Step 5: Extract details from right panel
                        job_data = self.extract_job_details(idx+1)
                        self.jobs_data.append(job_data)

                        # Small delay before next job
                        time.sleep(1.5)

            # Step 7: Generate report
            self.generate_report()

        except Exception as e:
            print(f"\n❌ Error during workflow: {e}")
            import traceback
            traceback.print_exc()

        finally:
            # Close browser
            if self.driver:
                self.driver.quit()
                print("\n✅ Browser closed")

    def generate_report(self):
        """Step 7: Generate report for all jobs."""
        print(f"\n{'='*70}")
        print("STEP 7: Generate Report")
        print("="*70)

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # Save workflow log
        workflow_log_path = output_dir / "workflow_log.json"
        with open(workflow_log_path, 'w') as f:
            json.dump(self.workflow_log, f, indent=2)

        print(f"\n✅ Workflow log saved: {workflow_log_path}")

        # Save jobs data
        jobs_data_path = output_dir / "jobs_data.json"
        with open(jobs_data_path, 'w') as f:
            json.dump(self.jobs_data, f, indent=2)

        print(f"✅ Jobs data saved: {jobs_data_path}")

        # Generate summary report
        summary_path = output_dir / "workflow_summary.txt"
        with open(summary_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("LINKEDIN SCRAPER - WORKFLOW TEST SUMMARY\n")
            f.write("="*70 + "\n\n")

            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Jobs Scraped: {len(self.jobs_data)}\n")
            f.write(f"Total Actions Logged: {len(self.workflow_log)}\n\n")

            f.write("="*70 + "\n")
            f.write("JOBS SCRAPED\n")
            f.write("="*70 + "\n\n")

            for idx, job in enumerate(self.jobs_data, 1):
                f.write(f"{idx}. {job.get('title', 'N/A')}\n")
                f.write(f"   Company: {job.get('company', 'N/A')}\n")
                f.write(f"   Location: {job.get('location', 'N/A')}\n")
                f.write(f"   URL: {job.get('url', 'N/A')}\n\n")

            f.write("\n" + "="*70 + "\n")
            f.write("WORKING SELECTORS (for implementation)\n")
            f.write("="*70 + "\n\n")

            # Extract working selectors from log
            for entry in self.workflow_log:
                if 'working_selector' in entry.get('details', {}):
                    f.write(f"{entry['action']}:\n")
                    f.write(f"  Selector: {entry['details']['working_selector']}\n\n")

        print(f"✅ Summary report saved: {summary_path}")

        print(f"\n{'='*70}")
        print("TEST COMPLETE!")
        print("="*70)
        print(f"\nTotal jobs scraped: {len(self.jobs_data)}")
        print(f"Reports generated:")
        print(f"  - {workflow_log_path}")
        print(f"  - {jobs_data_path}")
        print(f"  - {summary_path}")
        print(f"\nScreenshots saved in: output/")


if __name__ == "__main__":
    # Create tester instance
    tester = LinkedInWorkflowTester(headless=False)  # Set to True for headless

    # Run workflow test
    tester.test_workflow(
        keywords="Python Developer",
        max_jobs=5  # Test with 5 jobs as requested
    )
