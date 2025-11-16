"""Job data models."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class Job(BaseModel):
    """Represents a LinkedIn job posting."""

    # Core Information
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    job_url: str = Field(..., description="LinkedIn job URL")

    # Additional Details
    description: Optional[str] = Field(None, description="Job description")
    skills: List[str] = Field(default_factory=list, description="Required skills")
    employment_type: Optional[str] = Field(None, description="Full-time, Part-time, Contract, etc.")
    experience_level: Optional[str] = Field(None, description="Entry, Mid, Senior, etc.")

    # Metadata
    posted_date: Optional[str] = Field(None, description="When the job was posted")
    applicants_count: Optional[str] = Field(None, description="Number of applicants")
    salary_range: Optional[str] = Field(None, description="Salary information if available")

    # Internal tracking
    scraped_at: datetime = Field(default_factory=datetime.now, description="When this job was scraped")
    job_id: Optional[str] = Field(None, description="LinkedIn job ID")

    @field_validator('skills', mode='before')
    @classmethod
    def parse_skills(cls, v):
        """Parse skills from various formats."""
        if isinstance(v, str):
            # Split by common delimiters
            return [s.strip() for s in v.replace(',', '|').split('|') if s.strip()]
        elif isinstance(v, list):
            return [str(s).strip() for s in v if str(s).strip()]
        return []

    @field_validator('job_url', mode='before')
    @classmethod
    def validate_url(cls, v):
        """Ensure URL is a string."""
        if v:
            return str(v)
        return v

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_dict(self) -> dict:
        """Convert job to dictionary."""
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "job_url": self.job_url,
            "description": self.description,
            "skills": ", ".join(self.skills) if self.skills else "",
            "employment_type": self.employment_type or "N/A",
            "experience_level": self.experience_level or "N/A",
            "posted_date": self.posted_date or "N/A",
            "applicants_count": self.applicants_count or "N/A",
            "salary_range": self.salary_range or "N/A",
            "scraped_at": self.scraped_at.isoformat(),
            "job_id": self.job_id or "N/A"
        }


class SearchParameters(BaseModel):
    """LinkedIn job search parameters."""

    keywords: str = Field(..., description="Job title, skills, or company")
    location: str = Field(default="", description="Location (city, country, or remote)")

    # Filters
    date_posted: Optional[str] = Field(
        None,
        description="Time filter: r86400 (24h), r604800 (week), r2592000 (month)"
    )
    experience_level: Optional[List[str]] = Field(
        None,
        description="Experience levels: 1 (Internship), 2 (Entry), 3 (Associate), 4 (Mid-Senior), 5 (Director), 6 (Executive)"
    )
    job_type: Optional[List[str]] = Field(
        None,
        description="Job types: F (Full-time), P (Part-time), C (Contract), T (Temporary), I (Internship), V (Volunteer), O (Other)"
    )
    remote: Optional[List[str]] = Field(
        None,
        description="Work location: 1 (On-site), 2 (Remote), 3 (Hybrid)"
    )

    # Pagination
    max_jobs: int = Field(default=50, ge=1, le=1000, description="Maximum number of jobs to scrape")
    start_page: int = Field(default=0, ge=0, description="Starting page number")

    def build_url(self) -> str:
        """Build LinkedIn job search URL with all parameters."""
        base_url = "https://www.linkedin.com/jobs/search/?"

        params = []

        # Keywords
        if self.keywords:
            params.append(f"keywords={self.keywords.replace(' ', '%20')}")

        # Location
        if self.location:
            params.append(f"location={self.location.replace(' ', '%20')}")

        # Date posted filter
        if self.date_posted:
            params.append(f"f_TPR={self.date_posted}")

        # Experience level filter
        if self.experience_level:
            exp_levels = ",".join(str(level) for level in self.experience_level)
            params.append(f"f_E={exp_levels}")

        # Job type filter
        if self.job_type:
            job_types = ",".join(self.job_type)
            params.append(f"f_JT={job_types}")

        # Remote/On-site filter
        if self.remote:
            remote_types = ",".join(str(r) for r in self.remote)
            params.append(f"f_WT={remote_types}")

        # Pagination
        if self.start_page > 0:
            params.append(f"start={self.start_page * 25}")  # LinkedIn shows 25 jobs per page

        return base_url + "&".join(params)

    @classmethod
    def from_cli_args(
        cls,
        keywords: str,
        location: str = "",
        date_posted: Optional[str] = None,
        experience: Optional[List[str]] = None,
        job_type: Optional[List[str]] = None,
        remote_only: bool = False,
        max_jobs: int = 50
    ) -> "SearchParameters":
        """Create SearchParameters from CLI arguments."""
        # Map date posted to LinkedIn filter codes
        date_map = {
            "24h": "r86400",
            "day": "r86400",
            "week": "r604800",
            "month": "r2592000",
            "any": None
        }

        date_filter = date_map.get(date_posted.lower() if date_posted else "any")

        # Handle remote filter
        remote_filter = ["2"] if remote_only else None  # 2 = Remote

        return cls(
            keywords=keywords,
            location=location,
            date_posted=date_filter,
            experience_level=experience,
            job_type=job_type,
            remote=remote_filter,
            max_jobs=max_jobs
        )
