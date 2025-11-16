"""CSV export functionality."""

from pathlib import Path
from typing import List

import pandas as pd

from src.models.job import Job
from src.utils.logger import logger


class CSVExporter:
    """Export jobs to CSV format."""

    @staticmethod
    def export(jobs: List[Job], output_path: Path) -> bool:
        """
        Export jobs to CSV file.

        Args:
            jobs: List of Job objects
            output_path: Output file path

        Returns:
            True if successful, False otherwise
        """
        try:
            if not jobs:
                logger.warning("No jobs to export")
                return False

            # Convert jobs to dictionaries
            data = [job.to_dict() for job in jobs]

            # Create DataFrame
            df = pd.DataFrame(data)

            # Reorder columns for better readability
            column_order = [
                'title',
                'company',
                'location',
                'employment_type',
                'experience_level',
                'posted_date',
                'applicants_count',
                'salary_range',
                'skills',
                'job_url',
                'job_id',
                'scraped_at'
            ]

            # Only include columns that exist
            existing_columns = [col for col in column_order if col in df.columns]
            df = df[existing_columns]

            # Export to CSV
            output_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_path, index=False, encoding='utf-8')

            logger.info(f"Exported {len(jobs)} jobs to CSV: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            return False
