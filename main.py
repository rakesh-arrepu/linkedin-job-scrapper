#!/usr/bin/env python3
"""
LinkedIn Job Scraper - CLI Interface
Scrape LinkedIn jobs and generate detailed reports
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich import box

from config.settings import settings
from src.models.job import SearchParameters
from src.scraper.linkedin_scraper import LinkedInScraper
from src.exporters.pdf_exporter import PDFExporter
from src.exporters.csv_exporter import CSVExporter
from src.exporters.json_exporter import JSONExporter
from src.utils.logger import setup_logger, logger

console = Console()


def print_banner():
    """Print application banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           LinkedIn Job Scraper                               ║
    ║           Find Your Dream Job                                ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


@click.command()
@click.option(
    '--keywords', '-k',
    required=True,
    help='Job keywords (e.g., "Python Developer", "Data Scientist")'
)
@click.option(
    '--location', '-l',
    default='',
    help='Job location (e.g., "New York", "Remote", "United States")'
)
@click.option(
    '--date-posted', '-d',
    type=click.Choice(['24h', 'week', 'month', 'any'], case_sensitive=False),
    default='any',
    help='Date range for job postings'
)
@click.option(
    '--experience', '-e',
    type=click.Choice(['1', '2', '3', '4', '5', '6'], case_sensitive=False),
    multiple=True,
    help='Experience level (1=Internship, 2=Entry, 3=Associate, 4=Mid-Senior, 5=Director, 6=Executive)'
)
@click.option(
    '--job-type', '-t',
    type=click.Choice(['F', 'P', 'C', 'T', 'I', 'V', 'O'], case_sensitive=False),
    multiple=True,
    help='Job type (F=Full-time, P=Part-time, C=Contract, T=Temporary, I=Internship, V=Volunteer, O=Other)'
)
@click.option(
    '--remote-only', '-r',
    is_flag=True,
    help='Show only remote jobs'
)
@click.option(
    '--max-jobs', '-m',
    type=int,
    default=50,
    help='Maximum number of jobs to scrape (default: 50)'
)
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Output file path (without extension)'
)
@click.option(
    '--format', '-f',
    type=click.Choice(['pdf', 'csv', 'json', 'all'], case_sensitive=False),
    default='all',
    help='Output format (default: all)'
)
@click.option(
    '--headless/--no-headless',
    default=True,
    help='Run browser in headless mode (default: headless)'
)
@click.option(
    '--enrich',
    is_flag=True,
    help='Enrich jobs with detailed information (slower but more data)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose logging'
)
def main(
    keywords: str,
    location: str,
    date_posted: str,
    experience: tuple,
    job_type: tuple,
    remote_only: bool,
    max_jobs: int,
    output: Optional[str],
    format: str,
    headless: bool,
    enrich: bool,
    verbose: bool
):
    """
    LinkedIn Job Scraper - Find and export job listings from LinkedIn.

    \b
    Examples:
        # Basic search
        python main.py -k "Python Developer" -l "Remote"

        # Advanced search with filters
        python main.py -k "Data Scientist" -l "New York" -d week -e 3 -e 4 -t F --max-jobs 100

        # Export to specific format
        python main.py -k "Software Engineer" -f pdf -o my_jobs

        # Enable enrichment for detailed job information
        python main.py -k "DevOps Engineer" --enrich
    """
    # Setup logger
    log_level = "DEBUG" if verbose else settings.log_level
    setup_logger(level=log_level, log_file=settings.log_file)

    # Print banner
    print_banner()

    try:
        # Create search parameters
        search_params = SearchParameters.from_cli_args(
            keywords=keywords,
            location=location,
            date_posted=date_posted,
            experience=list(experience) if experience else None,
            job_type=list(job_type) if job_type else None,
            remote_only=remote_only,
            max_jobs=max_jobs
        )

        # Display search info
        _display_search_info(search_params)

        # Initialize scraper
        scraper = LinkedInScraper(headless=headless)

        # Scrape jobs with progress bar
        jobs = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scraping jobs...", total=max_jobs)

            jobs = scraper.scrape(search_params)

            progress.update(task, completed=len(jobs))

        if not jobs:
            console.print("\n[red]❌ No jobs found. Try adjusting your search parameters.[/red]")
            return

        console.print(f"\n[green]✅ Successfully scraped {len(jobs)} jobs![/green]")

        # Enrich jobs if requested
        if enrich:
            console.print("\n[cyan]Enriching job details...[/cyan]")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Enriching jobs...", total=len(jobs))

                for idx, job in enumerate(jobs):
                    jobs[idx] = scraper.enrich_job_details(job)
                    progress.update(task, advance=1)

            console.print("[green]✅ Enrichment complete![/green]")

        # Display job summary
        _display_job_summary(jobs)

        # Generate output filename
        if not output:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_keywords = keywords.replace(" ", "_").replace("/", "_")
            output = f"{settings.output_dir}/{safe_keywords}_{timestamp}"
        else:
            output = str(Path(output).with_suffix(''))  # Remove extension if provided

        # Export data
        console.print("\n[cyan]Generating reports...[/cyan]")

        export_params = {
            'keywords': keywords,
            'location': location or 'Any',
            'date_posted': date_posted,
            'max_jobs': max_jobs
        }

        success_count = 0

        if format in ['pdf', 'all']:
            pdf_path = Path(f"{output}.pdf")
            if PDFExporter().export(jobs, pdf_path, export_params):
                console.print(f"[green]✅ PDF report: {pdf_path}[/green]")
                success_count += 1

        if format in ['csv', 'all']:
            csv_path = Path(f"{output}.csv")
            if CSVExporter.export(jobs, csv_path):
                console.print(f"[green]✅ CSV export: {csv_path}[/green]")
                success_count += 1

        if format in ['json', 'all']:
            json_path = Path(f"{output}.json")
            if JSONExporter.export(jobs, json_path):
                console.print(f"[green]✅ JSON export: {json_path}[/green]")
                success_count += 1

        # Final summary
        if success_count > 0:
            console.print(f"\n[bold green]🎉 Success! Generated {success_count} report(s)[/bold green]")
        else:
            console.print("\n[red]❌ Failed to generate reports[/red]")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Scraping interrupted by user[/yellow]")
        sys.exit(0)

    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        if verbose:
            console.print_exception()
        sys.exit(1)


def _display_search_info(params: SearchParameters):
    """Display search parameters in a formatted panel."""
    info_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    info_table.add_column("Parameter", style="cyan bold")
    info_table.add_column("Value", style="white")

    info_table.add_row("Keywords", params.keywords)
    info_table.add_row("Location", params.location or "Any")
    info_table.add_row("Max Jobs", str(params.max_jobs))

    if params.date_posted:
        date_map = {
            'r86400': 'Past 24 hours',
            'r604800': 'Past week',
            'r2592000': 'Past month'
        }
        info_table.add_row("Date Posted", date_map.get(params.date_posted, 'Any time'))

    if params.remote:
        info_table.add_row("Remote Filter", "Remote only")

    panel = Panel(
        info_table,
        title="[bold]Search Parameters[/bold]",
        border_style="cyan",
        padding=(1, 2)
    )

    console.print(panel)
    console.print()


def _display_job_summary(jobs):
    """Display summary of scraped jobs."""
    console.print("\n[bold cyan]📊 Job Summary[/bold cyan]")

    summary_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    summary_table.add_column("Company", style="cyan", max_width=30)
    summary_table.add_column("Title", style="white", max_width=35)
    summary_table.add_column("Location", style="green", max_width=25)

    # Show first 10 jobs
    for job in jobs[:10]:
        summary_table.add_row(
            job.company[:30],
            job.title[:35],
            job.location[:25]
        )

    if len(jobs) > 10:
        summary_table.add_row(
            f"... and {len(jobs) - 10} more",
            "",
            "",
            style="dim"
        )

    console.print(summary_table)


if __name__ == '__main__':
    main()
