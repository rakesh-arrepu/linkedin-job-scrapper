"""PDF export functionality with detailed formatting and charts."""

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import List
import io

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from src.models.job import Job
from src.utils.logger import logger


class PDFExporter:
    """Export jobs to detailed PDF format with charts and statistics."""

    def __init__(self):
        """Initialize PDF exporter."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0A66C2'),  # LinkedIn blue
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#666666'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0A66C2'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))

        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#000000'),
            fontName='Helvetica-Bold',
            spaceAfter=6
        ))

        # Compact style for job details
        self.styles.add(ParagraphStyle(
            name='JobDetail',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#333333'),
            spaceAfter=3
        ))

    def export(self, jobs: List[Job], output_path: Path, search_params: dict = None) -> bool:
        """
        Export jobs to PDF with detailed formatting.

        Args:
            jobs: List of Job objects
            output_path: Output file path
            search_params: Optional search parameters for report header

        Returns:
            True if successful, False otherwise
        """
        try:
            if not jobs:
                logger.warning("No jobs to export")
                return False

            # Create output directory
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=1*inch,
                bottomMargin=0.75*inch
            )

            # Build PDF content
            story = []

            # Add header
            story.extend(self._create_header(jobs, search_params))

            # Add statistics and charts
            story.extend(self._create_statistics_section(jobs))

            # Add page break
            story.append(PageBreak())

            # Add job listings
            story.extend(self._create_job_listings(jobs))

            # Build PDF
            doc.build(story)

            logger.info(f"Exported {len(jobs)} jobs to PDF: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export PDF: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def _create_header(self, jobs: List[Job], search_params: dict = None) -> List:
        """Create PDF header with title and search info."""
        elements = []

        # Main title
        title = Paragraph("LinkedIn Job Search Report", self.styles['CustomTitle'])
        elements.append(title)

        # Search parameters
        if search_params:
            info_lines = []
            if search_params.get('keywords'):
                info_lines.append(f"<b>Keywords:</b> {search_params['keywords']}")
            if search_params.get('location'):
                info_lines.append(f"<b>Location:</b> {search_params['location']}")
            if search_params.get('date_posted'):
                info_lines.append(f"<b>Date Range:</b> {search_params['date_posted']}")

            info_text = " | ".join(info_lines)
            info = Paragraph(info_text, self.styles['CustomSubtitle'])
            elements.append(info)

        # Report metadata
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        metadata = Paragraph(
            f"<b>Report Generated:</b> {report_date} | <b>Total Jobs:</b> {len(jobs)}",
            self.styles['CustomSubtitle']
        )
        elements.append(metadata)
        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _create_statistics_section(self, jobs: List[Job]) -> List:
        """Create statistics section with charts."""
        elements = []

        # Section header
        header = Paragraph("📊 Job Market Statistics", self.styles['SectionHeader'])
        elements.append(header)

        # Create charts
        charts_row = []

        # Top companies chart
        company_chart = self._create_top_companies_chart(jobs)
        if company_chart:
            charts_row.append(company_chart)

        # Top locations chart
        location_chart = self._create_top_locations_chart(jobs)
        if location_chart:
            charts_row.append(location_chart)

        # Add charts side by side
        if charts_row:
            chart_table = Table([charts_row], colWidths=[3.25*inch, 3.25*inch])
            chart_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(chart_table)
            elements.append(Spacer(1, 0.2*inch))

        # Summary statistics table
        stats_table = self._create_summary_stats_table(jobs)
        if stats_table:
            elements.append(stats_table)

        elements.append(Spacer(1, 0.3*inch))

        return elements

    def _create_top_companies_chart(self, jobs: List[Job], top_n: int = 10) -> Image:
        """Create horizontal bar chart of top companies."""
        try:
            # Count companies
            companies = [job.company for job in jobs if job.company != "Unknown Company"]
            company_counts = Counter(companies).most_common(top_n)

            if not company_counts:
                return None

            # Create chart
            fig, ax = plt.subplots(figsize=(6, 4))

            companies_list = [c[0][:30] for c in company_counts]  # Truncate long names
            counts = [c[1] for c in company_counts]

            y_pos = range(len(companies_list))
            ax.barh(y_pos, counts, color='#0A66C2')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(companies_list, fontsize=8)
            ax.invert_yaxis()
            ax.set_xlabel('Number of Jobs', fontsize=9)
            ax.set_title(f'Top {top_n} Companies', fontsize=10, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)

            # Save to buffer
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            buf.seek(0)

            # Create ReportLab image
            img = Image(buf, width=3*inch, height=2.5*inch)
            return img

        except Exception as e:
            logger.error(f"Error creating companies chart: {e}")
            return None

    def _create_top_locations_chart(self, jobs: List[Job], top_n: int = 10) -> Image:
        """Create horizontal bar chart of top locations."""
        try:
            # Count locations
            locations = [job.location for job in jobs if job.location != "Unknown Location"]
            location_counts = Counter(locations).most_common(top_n)

            if not location_counts:
                return None

            # Create chart
            fig, ax = plt.subplots(figsize=(6, 4))

            locations_list = [loc[0][:30] for loc in location_counts]  # Truncate long names
            counts = [loc[1] for loc in location_counts]

            y_pos = range(len(locations_list))
            ax.barh(y_pos, counts, color='#057642')  # Green color
            ax.set_yticks(y_pos)
            ax.set_yticklabels(locations_list, fontsize=8)
            ax.invert_yaxis()
            ax.set_xlabel('Number of Jobs', fontsize=9)
            ax.set_title(f'Top {top_n} Locations', fontsize=10, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)

            # Save to buffer
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            buf.seek(0)

            # Create ReportLab image
            img = Image(buf, width=3*inch, height=2.5*inch)
            return img

        except Exception as e:
            logger.error(f"Error creating locations chart: {e}")
            return None

    def _create_summary_stats_table(self, jobs: List[Job]) -> Table:
        """Create summary statistics table."""
        try:
            # Calculate statistics
            total_jobs = len(jobs)
            unique_companies = len(set(job.company for job in jobs))
            unique_locations = len(set(job.location for job in jobs))

            # Count jobs with skills
            jobs_with_skills = sum(1 for job in jobs if job.skills)

            # Most common skills
            all_skills = []
            for job in jobs:
                if job.skills:
                    all_skills.extend(job.skills)
            top_skills = Counter(all_skills).most_common(5)
            top_skills_text = ", ".join([f"{skill} ({count})" for skill, count in top_skills]) if top_skills else "N/A"

            # Create table data
            data = [
                ['Metric', 'Value'],
                ['Total Job Postings', str(total_jobs)],
                ['Unique Companies', str(unique_companies)],
                ['Unique Locations', str(unique_locations)],
                ['Jobs with Skills Listed', str(jobs_with_skills)],
                ['Top 5 Skills', top_skills_text],
            ]

            # Create table
            table = Table(data, colWidths=[2.5*inch, 4*inch])
            table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A66C2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

                # Data rows
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),

                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))

            return table

        except Exception as e:
            logger.error(f"Error creating summary stats table: {e}")
            return None

    def _create_job_listings(self, jobs: List[Job]) -> List:
        """Create detailed job listings section."""
        elements = []

        # Section header
        header = Paragraph("📋 Job Listings", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 0.2*inch))

        # Add each job
        for idx, job in enumerate(jobs, 1):
            job_elements = self._create_job_card(job, idx)
            elements.append(KeepTogether(job_elements))

            # Add spacer between jobs
            if idx < len(jobs):
                elements.append(Spacer(1, 0.15*inch))

        return elements

    def _create_job_card(self, job: Job, number: int) -> List:
        """Create a styled card for a single job."""
        elements = []

        # Job number and title
        title_text = f"<b>{number}. {job.title}</b>"
        title = Paragraph(title_text, self.styles['JobTitle'])
        elements.append(title)

        # Create table for job details
        data = []

        # Company and location row
        data.append([
            Paragraph(f"<b>🏢 Company:</b> {job.company}", self.styles['JobDetail']),
            Paragraph(f"<b>📍 Location:</b> {job.location}", self.styles['JobDetail'])
        ])

        # Employment type and experience level
        emp_type = job.employment_type or "N/A"
        exp_level = job.experience_level or "N/A"
        data.append([
            Paragraph(f"<b>💼 Type:</b> {emp_type}", self.styles['JobDetail']),
            Paragraph(f"<b>📊 Level:</b> {exp_level}", self.styles['JobDetail'])
        ])

        # Posted date and applicants
        posted = job.posted_date or "N/A"
        applicants = job.applicants_count or "N/A"
        data.append([
            Paragraph(f"<b>📅 Posted:</b> {posted}", self.styles['JobDetail']),
            Paragraph(f"<b>👥 Applicants:</b> {applicants}", self.styles['JobDetail'])
        ])

        # Skills (full width)
        if job.skills:
            skills_text = ", ".join(job.skills[:10])  # Limit to 10 skills
            if len(job.skills) > 10:
                skills_text += f" (+{len(job.skills) - 10} more)"
        else:
            skills_text = "Not specified"

        data.append([
            Paragraph(f"<b>🛠️ Skills:</b> {skills_text}", self.styles['JobDetail']),
            ""
        ])

        # Job URL (full width)
        url_text = f'<b>🔗 Link:</b> <link href="{job.job_url}" color="blue">{job.job_url[:80]}...</link>'
        data.append([
            Paragraph(url_text, self.styles['JobDetail']),
            ""
        ])

        # Create table
        table = Table(data, colWidths=[3.25*inch, 3.25*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F6F8')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#0A66C2')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            # Make skills and URL row span full width
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (0, 4), (1, 4)),
        ]))

        elements.append(table)

        return elements
