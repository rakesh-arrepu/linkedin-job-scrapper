"""
Example usage of LinkedIn Job Scraper programmatically.

This demonstrates how to use the scraper as a Python library
rather than via command line.
"""

from pathlib import Path
from src.models.job import SearchParameters
from src.scraper.linkedin_scraper import LinkedInScraper
from src.exporters.pdf_exporter import PDFExporter
from src.exporters.csv_exporter import CSVExporter
from src.exporters.json_exporter import JSONExporter
from src.utils.logger import setup_logger


def example_basic_search():
    """Example: Basic job search."""
    print("Example 1: Basic Search")
    print("-" * 50)

    # Setup logging
    logger = setup_logger(level="INFO")

    # Create search parameters
    search_params = SearchParameters(
        keywords="Python Developer",
        location="Remote",
        max_jobs=10
    )

    # Initialize scraper
    scraper = LinkedInScraper(headless=True)

    # Scrape jobs
    jobs = scraper.scrape(search_params)

    # Print results
    print(f"Found {len(jobs)} jobs:")
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job.title} at {job.company} - {job.location}")

    return jobs


def example_advanced_search():
    """Example: Advanced search with filters."""
    print("\nExample 2: Advanced Search with Filters")
    print("-" * 50)

    # Create search parameters with filters
    search_params = SearchParameters(
        keywords="Data Scientist",
        location="New York",
        date_posted="r604800",  # Past week
        experience_level=["3", "4"],  # Associate and Mid-Senior
        job_type=["F"],  # Full-time only
        max_jobs=20
    )

    # Initialize scraper
    scraper = LinkedInScraper(headless=True)

    # Scrape jobs
    jobs = scraper.scrape(search_params)

    print(f"Found {len(jobs)} jobs matching criteria")

    return jobs


def example_export_all_formats(jobs):
    """Example: Export jobs to all formats."""
    print("\nExample 3: Export to All Formats")
    print("-" * 50)

    output_dir = Path("./output/examples")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export to PDF
    pdf_path = output_dir / "jobs_report.pdf"
    PDFExporter().export(jobs, pdf_path, {
        'keywords': 'Python Developer',
        'location': 'Remote',
        'max_jobs': len(jobs)
    })
    print(f"✅ PDF exported to: {pdf_path}")

    # Export to CSV
    csv_path = output_dir / "jobs_data.csv"
    CSVExporter.export(jobs, csv_path)
    print(f"✅ CSV exported to: {csv_path}")

    # Export to JSON
    json_path = output_dir / "jobs_data.json"
    JSONExporter.export(jobs, json_path)
    print(f"✅ JSON exported to: {json_path}")


def example_job_enrichment():
    """Example: Enrich jobs with detailed information."""
    print("\nExample 4: Job Enrichment")
    print("-" * 50)

    # Create simple search
    search_params = SearchParameters(
        keywords="DevOps Engineer",
        max_jobs=5  # Keep it small for demo
    )

    # Initialize scraper
    scraper = LinkedInScraper(headless=True)

    # Scrape jobs
    jobs = scraper.scrape(search_params)

    print(f"Enriching {len(jobs)} jobs with detailed information...")

    # Enrich each job
    enriched_jobs = []
    for job in jobs:
        enriched_job = scraper.enrich_job_details(job)
        enriched_jobs.append(enriched_job)

        # Show difference
        print(f"\nJob: {job.title}")
        print(f"  Description available: {bool(enriched_job.description)}")
        print(f"  Skills found: {len(enriched_job.skills)}")
        if enriched_job.skills:
            print(f"  Skills: {', '.join(enriched_job.skills[:5])}")

    return enriched_jobs


def example_custom_filters():
    """Example: Using custom filters."""
    print("\nExample 5: Custom Filters")
    print("-" * 50)

    # Remote only + Full-time + Mid-Senior level
    search_params = SearchParameters(
        keywords="Software Engineer",
        remote=["2"],  # Remote only
        job_type=["F"],  # Full-time
        experience_level=["4"],  # Mid-Senior
        date_posted="r86400",  # Past 24 hours
        max_jobs=15
    )

    scraper = LinkedInScraper(headless=True)
    jobs = scraper.scrape(search_params)

    print(f"Found {len(jobs)} remote, full-time, mid-senior positions")

    return jobs


if __name__ == "__main__":
    print("=" * 50)
    print("LinkedIn Job Scraper - Example Usage")
    print("=" * 50)

    # Run examples
    try:
        # Example 1: Basic search
        jobs = example_basic_search()

        # Example 2: Advanced search (commented out to save time)
        # jobs = example_advanced_search()

        # Example 3: Export to all formats
        if jobs:
            example_export_all_formats(jobs)

        # Example 4: Job enrichment (commented out - takes longer)
        # enriched_jobs = example_job_enrichment()

        # Example 5: Custom filters (commented out)
        # filtered_jobs = example_custom_filters()

        print("\n" + "=" * 50)
        print("Examples completed successfully!")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")

    except Exception as e:
        print(f"\n\nError running examples: {e}")
        import traceback
        traceback.print_exc()
