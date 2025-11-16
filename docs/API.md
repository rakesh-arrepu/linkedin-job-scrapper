# API Documentation

This document describes how to use LinkedIn Job Scraper as a Python library.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Components](#core-components)
- [Examples](#examples)

## Installation

```bash
pip install -e .
```

Or directly:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from src.models.job import SearchParameters
from src.scraper.linkedin_scraper import LinkedInScraper
from src.exporters.pdf_exporter import PDFExporter

# Create search parameters
search_params = SearchParameters(
    keywords="Python Developer",
    location="Remote",
    max_jobs=50
)

# Initialize and run scraper
scraper = LinkedInScraper(headless=True)
jobs = scraper.scrape(search_params)

# Export to PDF
PDFExporter().export(jobs, "jobs.pdf")
```

## Core Components

### SearchParameters

```python
class SearchParameters(BaseModel):
    """LinkedIn job search parameters."""

    keywords: str                        # Required: Search keywords
    location: str = ""                   # Optional: Location
    date_posted: Optional[str] = None    # Optional: Time filter
    experience_level: Optional[List[str]] = None
    job_type: Optional[List[str]] = None
    remote: Optional[List[str]] = None
    max_jobs: int = 50
    start_page: int = 0
```

#### Date Posted Options

```python
date_posted = "r86400"    # Past 24 hours
date_posted = "r604800"   # Past week
date_posted = "r2592000"  # Past month
```

#### Experience Level Options

```python
experience_level = ["1"]  # Internship
experience_level = ["2"]  # Entry level
experience_level = ["3"]  # Associate
experience_level = ["4"]  # Mid-Senior level
experience_level = ["5"]  # Director
experience_level = ["6"]  # Executive
```

#### Job Type Options

```python
job_type = ["F"]  # Full-time
job_type = ["P"]  # Part-time
job_type = ["C"]  # Contract
job_type = ["T"]  # Temporary
job_type = ["I"]  # Internship
job_type = ["V"]  # Volunteer
job_type = ["O"]  # Other
```

#### Remote Options

```python
remote = ["1"]  # On-site
remote = ["2"]  # Remote
remote = ["3"]  # Hybrid
```

### LinkedInScraper

```python
class LinkedInScraper:
    """Main scraper class."""

    def __init__(self, headless: bool = True):
        """Initialize scraper with headless mode option."""

    def scrape(self, search_params: SearchParameters) -> List[Job]:
        """Scrape jobs based on search parameters."""

    def enrich_job_details(self, job: Job) -> Job:
        """Enrich job with detailed information."""

    def get_jobs(self) -> List[Job]:
        """Get list of scraped jobs."""

    def clear_jobs(self):
        """Clear scraped jobs list."""
```

### Job Model

```python
class Job(BaseModel):
    """Represents a LinkedIn job posting."""

    # Core fields
    title: str
    company: str
    location: str
    job_url: str

    # Optional fields
    description: Optional[str] = None
    skills: List[str] = []
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    posted_date: Optional[str] = None
    applicants_count: Optional[str] = None
    salary_range: Optional[str] = None

    # Metadata
    scraped_at: datetime
    job_id: Optional[str] = None
```

### Exporters

#### PDFExporter

```python
from src.exporters.pdf_exporter import PDFExporter

exporter = PDFExporter()
exporter.export(
    jobs=jobs,
    output_path=Path("report.pdf"),
    search_params={
        'keywords': 'Python Developer',
        'location': 'Remote'
    }
)
```

#### CSVExporter

```python
from src.exporters.csv_exporter import CSVExporter

CSVExporter.export(jobs, Path("jobs.csv"))
```

#### JSONExporter

```python
from src.exporters.json_exporter import JSONExporter

JSONExporter.export(jobs, Path("jobs.json"))
```

## Examples

### Basic Search

```python
from src.models.job import SearchParameters
from src.scraper.linkedin_scraper import LinkedInScraper

search_params = SearchParameters(
    keywords="Data Scientist",
    location="New York",
    max_jobs=100
)

scraper = LinkedInScraper(headless=True)
jobs = scraper.scrape(search_params)

print(f"Found {len(jobs)} jobs")
for job in jobs[:5]:
    print(f"- {job.title} at {job.company}")
```

### Advanced Search with Filters

```python
search_params = SearchParameters(
    keywords="Software Engineer",
    location="San Francisco",
    date_posted="r604800",  # Past week
    experience_level=["3", "4"],  # Associate and Mid-Senior
    job_type=["F"],  # Full-time only
    remote=["2", "3"],  # Remote or Hybrid
    max_jobs=200
)

scraper = LinkedInScraper(headless=True)
jobs = scraper.scrape(search_params)
```

### Job Enrichment

```python
# Basic scrape
jobs = scraper.scrape(search_params)

# Enrich with detailed information
enriched_jobs = []
for job in jobs:
    enriched = scraper.enrich_job_details(job)
    enriched_jobs.append(enriched)
    print(f"Skills for {job.title}: {', '.join(enriched.skills)}")
```

### Custom Processing

```python
from collections import Counter

# Scrape jobs
jobs = scraper.scrape(search_params)

# Analyze top companies
companies = [job.company for job in jobs]
top_companies = Counter(companies).most_common(10)

print("Top 10 hiring companies:")
for company, count in top_companies:
    print(f"{company}: {count} jobs")

# Analyze top locations
locations = [job.location for job in jobs]
top_locations = Counter(locations).most_common(10)

print("\nTop 10 job locations:")
for location, count in top_locations:
    print(f"{location}: {count} jobs")
```

### Export to Multiple Formats

```python
from pathlib import Path
from src.exporters.pdf_exporter import PDFExporter
from src.exporters.csv_exporter import CSVExporter
from src.exporters.json_exporter import JSONExporter

output_dir = Path("./output")
output_dir.mkdir(exist_ok=True)

# PDF
PDFExporter().export(jobs, output_dir / "report.pdf")

# CSV
CSVExporter.export(jobs, output_dir / "jobs.csv")

# JSON
JSONExporter.export(jobs, output_dir / "jobs.json")
```

### Filter Jobs After Scraping

```python
# Get all jobs
all_jobs = scraper.scrape(SearchParameters(
    keywords="Developer",
    max_jobs=200
))

# Filter for specific criteria
remote_jobs = [j for j in all_jobs if "Remote" in j.location]
python_jobs = [j for j in all_jobs if "Python" in j.title]
senior_jobs = [j for j in all_jobs if j.experience_level == "Mid-Senior level"]

print(f"Total: {len(all_jobs)}")
print(f"Remote: {len(remote_jobs)}")
print(f"Python: {len(python_jobs)}")
print(f"Senior: {len(senior_jobs)}")
```

### Context Manager Usage

```python
from src.scraper.browser_manager import BrowserManager

# Use browser manager with context manager
with BrowserManager(headless=True) as browser:
    browser.get("https://www.linkedin.com/jobs/search/")
    # Browser automatically closes when done
```

### Custom Configuration

```python
from config.settings import Settings

# Create custom settings
settings = Settings(
    max_jobs=100,
    headless_mode=False,
    min_delay=5,
    max_delay=10,
    output_dir="./my_output"
)

# Use in scraper
scraper = LinkedInScraper(headless=settings.headless_mode)
```

### Error Handling

```python
from selenium.common.exceptions import WebDriverException

try:
    scraper = LinkedInScraper(headless=True)
    jobs = scraper.scrape(search_params)

    if not jobs:
        print("No jobs found")
    else:
        # Export results
        PDFExporter().export(jobs, "results.pdf")

except WebDriverException as e:
    print(f"Browser error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Cleanup is automatic
    pass
```

## Logging

```python
from src.utils.logger import setup_logger

# Setup custom logging
logger = setup_logger(
    name="my_scraper",
    level="DEBUG",
    log_file="my_scraper.log"
)

# Use logger
logger.info("Starting scrape")
logger.debug("Debug information")
logger.error("Error occurred")
```

## Rate Limiting

```python
from src.utils.rate_limiter import RateLimiter

# Custom rate limiter
rate_limiter = RateLimiter(
    min_delay=3.0,
    max_delay=7.0,
    random_delay=True
)

# Use in loop
for item in items:
    rate_limiter.wait()
    # Process item
```

## Best Practices

1. **Always use headless mode in production**
2. **Implement error handling** for network issues
3. **Use rate limiting** to avoid detection
4. **Start with small max_jobs** for testing
5. **Enrich jobs selectively** (it's slower)
6. **Save results incrementally** for large scrapes
7. **Check job count** before processing
8. **Use logging** for debugging
9. **Respect LinkedIn's ToS**
10. **Don't scrape excessively**
