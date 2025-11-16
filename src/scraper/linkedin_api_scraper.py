"""LinkedIn API-based job scraper implementation."""

import time
from typing import List, Optional
import requests

from config.settings import settings
from src.models.job import Job, SearchParameters
from src.utils.logger import logger
from src.utils.rate_limiter import RateLimiter


class LinkedInAPIScraper:
    """Scrapes job postings from LinkedIn using API."""

    def __init__(self):
        """Initialize API scraper."""
        self.rate_limiter = RateLimiter(
            min_delay=settings.min_delay,
            max_delay=settings.max_delay,
            random_delay=settings.random_delay
        )
        self.jobs: List[Job] = []
        self.api_provider = self._detect_api_provider()

    def _detect_api_provider(self) -> str:
        """Detect which API provider to use based on available keys."""
        if settings.rapidapi_key:
            logger.info("Using RapidAPI LinkedIn Data API")
            return "rapidapi"
        elif settings.jsearch_api_key:
            logger.info("Using JSSearch API")
            return "jsearch"
        elif settings.linkedin_api_key:
            logger.info("Using custom LinkedIn API")
            return "custom"
        else:
            logger.warning("No API key configured. API scraping will not work.")
            logger.info("Please set RAPIDAPI_KEY or JSEARCH_API_KEY in your .env file")
            logger.info("Get RapidAPI key: https://rapidapi.com/letscrape-6bRBa3QguO5/api/linkedin-data-api")
            logger.info("Get JSSearch key: https://rapidapi.com/jsearch/api/jsearch (free tier available)")
            return None

    def scrape(self, search_params: SearchParameters) -> List[Job]:
        """
        Scrape jobs using API based on search parameters.

        Args:
            search_params: Search parameters

        Returns:
            List of scraped jobs
        """
        logger.info(f"Starting API job scrape: {search_params.keywords} in {search_params.location or 'Any location'}")

        if not self.api_provider:
            logger.error("No API provider configured. Please set API key in .env file")
            return []

        try:
            if self.api_provider == "rapidapi":
                return self._scrape_with_rapidapi(search_params)
            elif self.api_provider == "jsearch":
                return self._scrape_with_jsearch(search_params)
            elif self.api_provider == "custom":
                return self._scrape_with_custom_api(search_params)
            else:
                logger.error("Unknown API provider")
                return []

        except Exception as e:
            logger.error(f"API scraping failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return self.jobs

    def _scrape_with_rapidapi(self, search_params: SearchParameters) -> List[Job]:
        """Scrape using RapidAPI LinkedIn Data API."""
        logger.info("Fetching jobs from RapidAPI LinkedIn Data API...")

        url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"

        headers = {
            "X-RapidAPI-Key": settings.rapidapi_key,
            "X-RapidAPI-Host": settings.rapidapi_host
        }

        # Build query parameters
        querystring = {
            "keywords": search_params.keywords,
            "locationId": search_params.location or "",
            "datePosted": self._map_date_filter(search_params.date_posted),
            "sort": "mostRelevant"
        }

        # Remove empty parameters
        querystring = {k: v for k, v in querystring.items() if v}

        try:
            # Make API request
            response = requests.get(url, headers=headers, params=querystring, timeout=30)
            response.raise_for_status()

            data = response.json()

            if not data or 'data' not in data:
                logger.warning("No jobs found in API response")
                return []

            jobs_data = data['data']
            logger.info(f"Found {len(jobs_data)} jobs from API")

            # Process each job
            for job_data in jobs_data[:search_params.max_jobs]:
                try:
                    job = self._parse_rapidapi_job(job_data)
                    if job:
                        self.jobs.append(job)
                        logger.info(f"Parsed job {len(self.jobs)}/{search_params.max_jobs}: {job.title} at {job.company}")

                    # Rate limiting
                    self.rate_limiter.wait()

                except Exception as e:
                    logger.error(f"Error parsing job: {e}")
                    continue

            logger.info(f"API scraping complete! Total jobs: {len(self.jobs)}")
            return self.jobs

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []

    def _scrape_with_jsearch(self, search_params: SearchParameters) -> List[Job]:
        """Scrape using JSSearch API (alternative with free tier)."""
        logger.info("Fetching jobs from JSSearch API...")

        url = "https://jsearch.p.rapidapi.com/search"

        headers = {
            "X-RapidAPI-Key": settings.jsearch_api_key,
            "X-RapidAPI-Host": settings.jsearch_api_host
        }

        # Build query
        query = f"{search_params.keywords}"
        if search_params.location:
            query += f" in {search_params.location}"

        querystring = {
            "query": query,
            "page": "1",
            "num_pages": "1",
            "date_posted": self._map_jsearch_date_filter(search_params.date_posted)
        }

        try:
            # Make API request
            response = requests.get(url, headers=headers, params=querystring, timeout=30)
            response.raise_for_status()

            data = response.json()

            if not data or 'data' not in data:
                logger.warning("No jobs found in API response")
                return []

            jobs_data = data['data']
            logger.info(f"Found {len(jobs_data)} jobs from JSSearch API")

            # Process each job
            for job_data in jobs_data[:search_params.max_jobs]:
                try:
                    job = self._parse_jsearch_job(job_data)
                    if job:
                        self.jobs.append(job)
                        logger.info(f"Parsed job {len(self.jobs)}/{search_params.max_jobs}: {job.title} at {job.company}")

                    # Rate limiting
                    self.rate_limiter.wait()

                except Exception as e:
                    logger.error(f"Error parsing job: {e}")
                    continue

            logger.info(f"API scraping complete! Total jobs: {len(self.jobs)}")
            return self.jobs

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []

    def _scrape_with_custom_api(self, search_params: SearchParameters) -> List[Job]:
        """Scrape using custom LinkedIn API (if user has their own)."""
        logger.warning("Custom API scraping not yet implemented")
        logger.info("Please use RapidAPI or JSSearch API instead")
        return []

    def _parse_rapidapi_job(self, job_data: dict) -> Optional[Job]:
        """Parse job data from RapidAPI response."""
        try:
            # Extract job ID from URL
            job_url = job_data.get('url', '')
            job_id = job_url.split('/')[-1].split('?')[0] if job_url else None

            # Create Job object
            job = Job(
                title=job_data.get('title', 'Unknown Title'),
                company=job_data.get('company', {}).get('name', 'Unknown Company'),
                location=job_data.get('location', 'Location not specified'),
                job_url=job_url,
                job_id=job_id,
                description=job_data.get('description', None),
                skills=job_data.get('skills', []),
                employment_type=job_data.get('type', None),
                experience_level=job_data.get('experienceLevel', None),
                posted_date=job_data.get('postedAt', None),
                applicants_count=job_data.get('applicantsCount', None),
                salary_range=job_data.get('salary', None)
            )

            return job

        except Exception as e:
            logger.error(f"Error parsing RapidAPI job: {e}")
            return None

    def _parse_jsearch_job(self, job_data: dict) -> Optional[Job]:
        """Parse job data from JSSearch API response."""
        try:
            # Extract relevant fields from JSSearch format
            job_url = job_data.get('job_apply_link') or job_data.get('job_url', '')
            job_id = job_data.get('job_id')

            # Parse skills from job highlights or description
            skills = []
            if 'job_highlights' in job_data and job_data['job_highlights']:
                qualifications = job_data['job_highlights'].get('Qualifications', [])
                # Extract potential skills from qualifications
                for qual in qualifications[:5]:
                    skills.append(qual[:50])  # Limit skill length

            # Create Job object
            job = Job(
                title=job_data.get('job_title', 'Unknown Title'),
                company=job_data.get('employer_name', 'Unknown Company'),
                location=job_data.get('job_city', '') + ', ' + job_data.get('job_state', '') if job_data.get('job_city') else job_data.get('job_country', 'Location not specified'),
                job_url=job_url,
                job_id=job_id,
                description=job_data.get('job_description', None),
                skills=skills if skills else [],
                employment_type=job_data.get('job_employment_type', None),
                experience_level=job_data.get('job_required_experience', {}).get('experience_mentioned', None) if isinstance(job_data.get('job_required_experience'), dict) else None,
                posted_date=job_data.get('job_posted_at_datetime_utc', None) or job_data.get('job_posted_at_timestamp', None),
                applicants_count=None,  # JSSearch doesn't provide this
                salary_range=self._format_salary(job_data)
            )

            return job

        except Exception as e:
            logger.error(f"Error parsing JSSearch job: {e}")
            return None

    def _format_salary(self, job_data: dict) -> Optional[str]:
        """Format salary information from JSSearch response."""
        try:
            min_salary = job_data.get('job_min_salary')
            max_salary = job_data.get('job_max_salary')
            currency = job_data.get('job_salary_currency', 'USD')
            period = job_data.get('job_salary_period', 'YEAR')

            if min_salary and max_salary:
                return f"${min_salary:,} - ${max_salary:,} {currency}/{period.lower()}"
            elif min_salary:
                return f"${min_salary:,}+ {currency}/{period.lower()}"
            elif max_salary:
                return f"Up to ${max_salary:,} {currency}/{period.lower()}"
            else:
                return None

        except Exception:
            return None

    def _map_date_filter(self, date_filter: Optional[str]) -> str:
        """Map search parameters date filter to RapidAPI format."""
        if not date_filter:
            return "anyTime"

        date_map = {
            "r86400": "past24Hours",
            "r604800": "pastWeek",
            "r2592000": "pastMonth"
        }

        return date_map.get(date_filter, "anyTime")

    def _map_jsearch_date_filter(self, date_filter: Optional[str]) -> str:
        """Map search parameters date filter to JSSearch format."""
        if not date_filter:
            return "all"

        date_map = {
            "r86400": "today",
            "r604800": "week",
            "r2592000": "month"
        }

        return date_map.get(date_filter, "all")

    def close(self):
        """Close scraper (no cleanup needed for API)."""
        logger.info("API scraper closed")
