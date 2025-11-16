"""JSON export functionality."""

import json
from pathlib import Path
from typing import List

from src.models.job import Job
from src.utils.logger import logger


class JSONExporter:
    """Export jobs to JSON format."""

    @staticmethod
    def export(jobs: List[Job], output_path: Path) -> bool:
        """
        Export jobs to JSON file.

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
            data = {
                "total_jobs": len(jobs),
                "jobs": [job.to_dict() for job in jobs]
            }

            # Export to JSON
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Exported {len(jobs)} jobs to JSON: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export JSON: {e}")
            return False
