"""PDF export functionality with stunning visuals, company logos, and vibrant design."""

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import List
import io
import urllib.request
import urllib.error

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

from src.models.job import Job
from src.utils.logger import logger


class PDFExporter:
    """Export jobs to stunning PDF with logos, icons, and vibrant colors."""

    # Vibrant color palette
    COLORS = {
        'primary': colors.HexColor('#0A66C2'),  # LinkedIn blue
        'secondary': colors.HexColor('#00A0DC'),  # Bright blue
        'success': colors.HexColor('#057642'),  # Green
        'warning': colors.HexColor('#F5BA31'),  # Yellow/Gold
        'danger': colors.HexColor('#CC1016'),  # Red
        'purple': colors.HexColor('#7A3FF7'),  # Purple
        'orange': colors.HexColor('#FF6B35'),  # Orange
        'teal': colors.HexColor('#00BFA5'),  # Teal
        'pink': colors.HexColor('#E91E63'),  # Pink
        'gradient_start': colors.HexColor('#667EEA'),  # Gradient start
        'gradient_end': colors.HexColor('#764BA2'),  # Gradient end
        'card_bg': colors.HexColor('#F8F9FA'),  # Light gray
        'text_primary': colors.HexColor('#212529'),  # Dark text
        'text_secondary': colors.HexColor('#6C757D'),  # Gray text
    }

    # Icon mappings (using Unicode symbols)
    ICONS = {
        'company': '🏢',
        'location': '📍',
        'calendar': '📅',
        'users': '👥',
        'briefcase': '💼',
        'level': '📊',
        'skills': '🛠️',
        'link': '🔗',
        'money': '💰',
        'chart': '📈',
        'trophy': '🏆',
        'star': '⭐',
        'fire': '🔥',
    }

    def __init__(self):
        """Initialize PDF exporter."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom paragraph styles with vibrant colors."""
        # Main title style
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=self.COLORS['primary'],
            spaceAfter=10,
            spaceBefore=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtitle
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=self.COLORS['text_secondary'],
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))

        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.COLORS['secondary'],
            spaceAfter=15,
            spaceBefore=25,
            fontName='Helvetica-Bold',
            borderColor=self.COLORS['secondary'],
            borderWidth=2,
            borderPadding=10,
            backColor=colors.HexColor('#E3F2FD'),
        ))

        # Job company name
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=self.COLORS['primary'],
            fontName='Helvetica-Bold',
            spaceAfter=4
        ))

        # Job title
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=self.COLORS['text_primary'],
            fontName='Helvetica-Bold',
            spaceAfter=8
        ))

        # Job details
        self.styles.add(ParagraphStyle(
            name='JobDetail',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.COLORS['text_secondary'],
            spaceAfter=3,
            fontName='Helvetica'
        ))

    def export(self, jobs: List[Job], output_path: Path, search_params: dict = None) -> bool:
        """
        Export jobs to stunning PDF.

        Args:
            jobs: List of Job objects
            output_path: Output file path
            search_params: Optional search parameters

        Returns:
            True if successful
        """
        try:
            if not jobs:
                logger.warning("No jobs to export")
                return False

            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create PDF
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )

            story = []

            # Add cover page with gradient background
            story.extend(self._create_cover_page(jobs, search_params))
            story.append(PageBreak())

            # Add statistics with vibrant charts
            story.extend(self._create_statistics_page(jobs))
            story.append(PageBreak())

            # Add job listings with logos and icons
            story.extend(self._create_job_listings(jobs))

            # Build PDF
            doc.build(story)

            logger.info(f"✨ Exported {len(jobs)} jobs to stunning PDF: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export PDF: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def _create_cover_page(self, jobs: List[Job], search_params: dict = None) -> List:
        """Create stunning cover page with gradient effect."""
        elements = []

        # Add some space at top
        elements.append(Spacer(1, 0.5*inch))

        # Main title with icon
        title_text = f"{self.ICONS['trophy']} LinkedIn Job Search Report {self.ICONS['trophy']}"
        title = Paragraph(title_text, self.styles['MainTitle'])
        elements.append(title)

        # Subtitle with search info
        if search_params:
            info_parts = []
            if search_params.get('keywords'):
                info_parts.append(f"{self.ICONS['briefcase']} {search_params['keywords']}")
            if search_params.get('location'):
                info_parts.append(f"{self.ICONS['location']} {search_params['location']}")

            if info_parts:
                subtitle_text = " | ".join(info_parts)
                subtitle = Paragraph(subtitle_text, self.styles['Subtitle'])
                elements.append(subtitle)

        elements.append(Spacer(1, 0.3*inch))

        # Create stats summary box
        stats_data = [
            [
                Paragraph(f"<b>{self.ICONS['chart']} Total Jobs</b>", self.styles['Normal']),
                Paragraph(f"<b>{self.ICONS['company']} Companies</b>", self.styles['Normal']),
                Paragraph(f"<b>{self.ICONS['location']} Locations</b>", self.styles['Normal'])
            ],
            [
                Paragraph(f"<font size=20 color='#0A66C2'><b>{len(jobs)}</b></font>", self.styles['Normal']),
                Paragraph(f"<font size=20 color='#057642'><b>{len(set(j.company for j in jobs))}</b></font>", self.styles['Normal']),
                Paragraph(f"<font size=20 color='#7A3FF7'><b>{len(set(j.location for j in jobs))}</b></font>", self.styles['Normal'])
            ]
        ]

        stats_table = Table(stats_data, colWidths=[2.2*inch, 2.2*inch, 2.2*inch])
        stats_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3F2FD')),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('BOX', (0, 0), (-1, -1), 2, self.COLORS['primary']),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor('#BBDEFB')),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))

        elements.append(stats_table)
        elements.append(Spacer(1, 0.5*inch))

        # Report metadata
        date_text = f"{self.ICONS['calendar']} Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        date_para = Paragraph(date_text, self.styles['Subtitle'])
        elements.append(date_para)

        return elements

    def _create_statistics_page(self, jobs: List[Job]) -> List:
        """Create statistics page with vibrant charts."""
        elements = []

        # Page title
        title = Paragraph(f"{self.ICONS['chart']} Market Analytics & Insights", self.styles['SectionHeader'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))

        # Create two charts side by side
        chart1 = self._create_colorful_companies_chart(jobs)
        chart2 = self._create_colorful_locations_chart(jobs)

        if chart1 and chart2:
            chart_table = Table([[chart1, chart2]], colWidths=[3.25*inch, 3.25*inch])
            chart_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(chart_table)
            elements.append(Spacer(1, 0.3*inch))

        # Skills analysis
        skills_chart = self._create_skills_chart(jobs)
        if skills_chart:
            elements.append(skills_chart)
            elements.append(Spacer(1, 0.2*inch))

        # Summary table with colors
        summary_table = self._create_colorful_summary_table(jobs)
        if summary_table:
            elements.append(summary_table)

        return elements

    def _create_colorful_companies_chart(self, jobs: List[Job], top_n: int = 10) -> Image:
        """Create vibrant horizontal bar chart of top companies."""
        try:
            companies = [job.company for job in jobs if job.company != "Unknown Company"]
            company_counts = Counter(companies).most_common(top_n)

            if not company_counts:
                return None

            fig, ax = plt.subplots(figsize=(6, 4.5), facecolor='#F8F9FA')

            companies_list = [c[0][:25] for c in company_counts]
            counts = [c[1] for c in company_counts]

            # Vibrant gradient colors
            colors_list = plt.cm.viridis(range(len(companies_list)))

            y_pos = range(len(companies_list))
            bars = ax.barh(y_pos, counts, color=colors_list, edgecolor='white', linewidth=2)

            # Add value labels
            for i, (bar, count) in enumerate(zip(bars, counts)):
                ax.text(count + 0.1, i, str(count), va='center', fontweight='bold', fontsize=9)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(companies_list, fontsize=9, fontweight='bold')
            ax.invert_yaxis()
            ax.set_xlabel('Number of Job Openings', fontsize=10, fontweight='bold')
            ax.set_title(f'{self.ICONS["company"]} Top {top_n} Hiring Companies',
                        fontsize=12, fontweight='bold', color='#0A66C2', pad=15)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.set_facecolor('#FFFFFF')

            # Style the plot
            for spine in ax.spines.values():
                spine.set_edgecolor('#CCCCCC')
                spine.set_linewidth(1.5)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#F8F9FA')
            plt.close()
            buf.seek(0)

            return Image(buf, width=3*inch, height=2.8*inch)

        except Exception as e:
            logger.error(f"Error creating companies chart: {e}")
            return None

    def _create_colorful_locations_chart(self, jobs: List[Job], top_n: int = 10) -> Image:
        """Create vibrant chart of top locations."""
        try:
            locations = [job.location for job in jobs if job.location != "Unknown Location"]
            location_counts = Counter(locations).most_common(top_n)

            if not location_counts:
                return None

            fig, ax = plt.subplots(figsize=(6, 4.5), facecolor='#F8F9FA')

            locations_list = [loc[0][:25] for loc in location_counts]
            counts = [loc[1] for loc in location_counts]

            # Different vibrant colors
            colors_list = plt.cm.plasma(range(len(locations_list)))

            y_pos = range(len(locations_list))
            bars = ax.barh(y_pos, counts, color=colors_list, edgecolor='white', linewidth=2)

            # Add value labels
            for i, (bar, count) in enumerate(zip(bars, counts)):
                ax.text(count + 0.1, i, str(count), va='center', fontweight='bold', fontsize=9)

            ax.set_yticks(y_pos)
            ax.set_yticklabels(locations_list, fontsize=9, fontweight='bold')
            ax.invert_yaxis()
            ax.set_xlabel('Number of Opportunities', fontsize=10, fontweight='bold')
            ax.set_title(f'{self.ICONS["location"]} Top {top_n} Job Locations',
                        fontsize=12, fontweight='bold', color='#7A3FF7', pad=15)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.set_facecolor('#FFFFFF')

            for spine in ax.spines.values():
                spine.set_edgecolor('#CCCCCC')
                spine.set_linewidth(1.5)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#F8F9FA')
            plt.close()
            buf.seek(0)

            return Image(buf, width=3*inch, height=2.8*inch)

        except Exception as e:
            logger.error(f"Error creating locations chart: {e}")
            return None

    def _create_skills_chart(self, jobs: List[Job]) -> Image:
        """Create colorful pie chart of top skills."""
        try:
            all_skills = []
            for job in jobs:
                if job.skills:
                    all_skills.extend(job.skills[:5])  # Top 5 per job

            if not all_skills:
                return None

            skill_counts = Counter(all_skills).most_common(8)

            fig, ax = plt.subplots(figsize=(6.5, 3.5), facecolor='#F8F9FA')

            skills = [s[0] for s in skill_counts]
            counts = [s[1] for s in skill_counts]

            colors_list = ['#0A66C2', '#057642', '#7A3FF7', '#FF6B35',
                          '#00BFA5', '#F5BA31', '#E91E63', '#667EEA']

            wedges, texts, autotexts = ax.pie(counts, labels=skills, colors=colors_list,
                                               autopct='%1.1f%%', startangle=90,
                                               textprops={'fontsize': 9, 'weight': 'bold'},
                                               explode=[0.05] * len(skills))

            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(8)
                autotext.set_weight('bold')

            ax.set_title(f'{self.ICONS["skills"]} Most In-Demand Skills',
                        fontsize=12, fontweight='bold', color='#0A66C2', pad=15)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='#F8F9FA')
            plt.close()
            buf.seek(0)

            return Image(buf, width=6.5*inch, height=3*inch)

        except Exception as e:
            logger.error(f"Error creating skills chart: {e}")
            return None

    def _create_colorful_summary_table(self, jobs: List[Job]) -> Table:
        """Create colorful summary statistics table."""
        try:
            total_jobs = len(jobs)
            unique_companies = len(set(job.company for job in jobs))
            unique_locations = len(set(job.location for job in jobs))
            jobs_with_skills = sum(1 for job in jobs if job.skills)

            all_skills = []
            for job in jobs:
                if job.skills:
                    all_skills.extend(job.skills)

            top_skills = Counter(all_skills).most_common(5)
            top_skills_text = ", ".join([f"<b>{skill}</b> ({count})" for skill, count in top_skills]) if top_skills else "N/A"

            data = [
                [Paragraph(f"<b>{self.ICONS['chart']} Metric</b>", self.styles['Normal']),
                 Paragraph(f"<b>{self.ICONS['star']} Value</b>", self.styles['Normal'])],
                [Paragraph(f"{self.ICONS['briefcase']} Total Job Postings", self.styles['Normal']),
                 Paragraph(f"<b><font color='#0A66C2'>{total_jobs}</font></b>", self.styles['Normal'])],
                [Paragraph(f"{self.ICONS['company']} Unique Companies", self.styles['Normal']),
                 Paragraph(f"<b><font color='#057642'>{unique_companies}</font></b>", self.styles['Normal'])],
                [Paragraph(f"{self.ICONS['location']} Unique Locations", self.styles['Normal']),
                 Paragraph(f"<b><font color='#7A3FF7'>{unique_locations}</font></b>", self.styles['Normal'])],
                [Paragraph(f"{self.ICONS['skills']} Jobs with Skills Listed", self.styles['Normal']),
                 Paragraph(f"<b><font color='#FF6B35'>{jobs_with_skills}</font></b>", self.styles['Normal'])],
                [Paragraph(f"{self.ICONS['fire']} Top 5 In-Demand Skills", self.styles['Normal']),
                 Paragraph(top_skills_text, self.styles['Normal'])],
            ]

            table = Table(data, colWidths=[2.5*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8F9FA')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
                ('TEXTCOLOR', (0, 1), (-1, -1), self.COLORS['text_primary']),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),

                ('GRID', (0, 0), (-1, -1), 1.5, colors.HexColor('#CCCCCC')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ]))

            return table

        except Exception as e:
            logger.error(f"Error creating summary table: {e}")
            return None

    def _create_job_listings(self, jobs: List[Job]) -> List:
        """Create stunning job listings with logos and icons."""
        elements = []

        # Section header
        header = Paragraph(f"{self.ICONS['briefcase']} Job Opportunities", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 0.2*inch))

        for idx, job in enumerate(jobs, 1):
            job_card = self._create_vibrant_job_card(job, idx)
            if job_card:
                elements.append(KeepTogether(job_card))
                if idx < len(jobs):
                    elements.append(Spacer(1, 0.15*inch))

        return elements

    def _get_company_logo(self, company_name: str, small: bool = False) -> Image:
        """Fetch company logo from Clearbit API."""
        try:
            # Use Clearbit logo API (free, no API key required)
            # Format company name to domain
            domain = company_name.lower().replace(' ', '').replace(',', '').replace('inc', '').replace('ltd', '').strip() + '.com'
            logo_url = f"https://logo.clearbit.com/{domain}"

            # Download logo
            req = urllib.request.Request(logo_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=2) as response:
                logo_data = response.read()

            buf = io.BytesIO(logo_data)

            # Return smaller logo for inline display
            if small:
                return Image(buf, width=0.35*inch, height=0.35*inch)
            else:
                return Image(buf, width=0.6*inch, height=0.6*inch)

        except:
            # Return None if logo fetch fails
            return None

    def _create_vibrant_job_card(self, job: Job, number: int) -> List:
        """Create a stunning job card with logo, icons, and vibrant colors."""
        elements = []

        # Get small company logo for inline display
        logo = self._get_company_logo(job.company, small=True)

        # Create header row with job title (left), company name (right), and logo (far right)
        # Job Title on left, Company Name and Logo on right (same line)
        header_components = []

        # Left side: Job number and title
        job_title_text = f"<font color='#0A66C2'><b>{number}. {job.title}</b></font>"
        job_title_para = Paragraph(job_title_text, self.styles['JobTitle'])

        # Right side: Company name and logo
        if logo:
            # Create company name with logo on the right
            company_text = f"<font color='#057642'><b>{job.company}</b></font>"
            company_para = Paragraph(company_text, self.styles['CompanyName'])

            # Header: Job Title | Company + Logo
            header_data = [[job_title_para, company_para, logo]]
            header_table = Table(header_data, colWidths=[3.5*inch, 2.4*inch, 0.6*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Job title left
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Company name right
                ('ALIGN', (2, 0), (2, 0), 'RIGHT'),  # Logo right
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (1, 0), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
        else:
            # No logo available, just company name on right
            company_text = f"{self.ICONS['company']} <font color='#057642'><b>{job.company}</b></font>"
            company_para = Paragraph(company_text, self.styles['CompanyName'])

            header_data = [[job_title_para, company_para]]
            header_table = Table(header_data, colWidths=[3.8*inch, 2.7*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))

        elements.append(header_table)
        elements.append(Spacer(1, 0.1*inch))

        # Create colorful details table with icons
        details = []

        # Only add rows for fields that have actual data (not N/A)
        # Row 1: Location and Employment Type
        row1 = []
        if job.location and job.location != "Location not specified":
            row1.append(Paragraph(f"{self.ICONS['location']} <b>Location:</b> {job.location}", self.styles['JobDetail']))
        if job.employment_type:
            row1.append(Paragraph(f"{self.ICONS['briefcase']} <b>Type:</b> {job.employment_type}", self.styles['JobDetail']))

        if row1:
            # Ensure we have 2 columns
            while len(row1) < 2:
                row1.append("")
            details.append(row1)

        # Row 2: Experience Level and Posted Date
        row2 = []
        if job.experience_level:
            row2.append(Paragraph(f"{self.ICONS['level']} <b>Level:</b> {job.experience_level}", self.styles['JobDetail']))
        if job.posted_date:
            row2.append(Paragraph(f"{self.ICONS['calendar']} <b>Posted:</b> {job.posted_date}", self.styles['JobDetail']))

        if row2:
            while len(row2) < 2:
                row2.append("")
            details.append(row2)

        # Row 3: Applicants and Salary (only if available)
        row3 = []
        if job.applicants_count:
            row3.append(Paragraph(f"{self.ICONS['users']} <b>Applicants:</b> {job.applicants_count}", self.styles['JobDetail']))
        if job.salary_range:
            row3.append(Paragraph(f"{self.ICONS['money']} <b>Salary:</b> {job.salary_range}", self.styles['JobDetail']))

        if row3:
            while len(row3) < 2:
                row3.append("")
            details.append(row3)

        # Row: Skills (full width, only if available)
        if job.skills and len(job.skills) > 0:
            skills_text = ", ".join([f"<b>{s}</b>" for s in job.skills[:8]])
            if len(job.skills) > 8:
                skills_text += f" <i>(+{len(job.skills) - 8} more)</i>"

            details.append([
                Paragraph(f"{self.ICONS['skills']} <b>Skills:</b> {skills_text}", self.styles['JobDetail']),
                ""
            ])

        # Row: Description snippet (if available)
        if job.description:
            desc_snippet = job.description[:200] + "..." if len(job.description) > 200 else job.description
            details.append([
                Paragraph(f"📝 <b>Description:</b> <i>{desc_snippet}</i>", self.styles['JobDetail']),
                ""
            ])

        # Row: Job URL (full width)
        url_display = job.job_url[:70] + "..." if len(job.job_url) > 70 else job.job_url
        url_text = f'{self.ICONS["link"]} <b>Apply:</b> <link href="{job.job_url}" color="blue"><u>{url_display}</u></link>'
        details.append([
            Paragraph(url_text, self.styles['JobDetail']),
            ""
        ])

        # Create table with vibrant styling
        details_table = Table(details, colWidths=[3.25*inch, 3.25*inch])

        # Count how many rows need spanning (skills, description, URL)
        span_rows = []
        for idx, row in enumerate(details):
            if row[1] == "":
                span_rows.append(idx)

        # Alternate row colors for visual appeal
        row_colors = [colors.white, colors.HexColor('#F0F8FF')]

        style_commands = [
            # Alternate row colors
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), row_colors),

            # Border and padding
            ('BOX', (0, 0), (-1, -1), 2, self.COLORS['secondary']),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BBDEFB')),

            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]

        # Add span commands for full-width rows
        for span_row in span_rows:
            style_commands.append(('SPAN', (0, span_row), (1, span_row)))
            # Alternate colors for spanned rows
            if span_row % 2 == 0:
                style_commands.append(('BACKGROUND', (0, span_row), (1, span_row), colors.HexColor('#FFF8E1')))

        details_table.setStyle(TableStyle(style_commands))

        elements.append(details_table)

        return elements
