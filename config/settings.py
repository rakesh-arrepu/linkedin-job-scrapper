"""Configuration settings for LinkedIn Job Scraper."""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

    # Scraping Settings
    max_jobs: int = 50
    delay_between_requests: int = 3
    page_load_timeout: int = 30
    headless_mode: bool = True

    # Browser Settings
    browser_window_width: int = 1920
    browser_window_height: int = 1080
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    # Output Settings
    output_dir: Path = Path("./output")
    default_output_format: str = "pdf"
    include_timestamps: bool = True

    # Logging
    log_level: str = "INFO"
    log_file: str = "scraper.log"

    # Rate Limiting
    min_delay: int = 2
    max_delay: int = 5
    random_delay: bool = True

    # LinkedIn Settings (Optional)
    linkedin_email: Optional[str] = None
    linkedin_password: Optional[str] = None

    # Scraper Method Configuration
    scraper_method: str = "api"  # 'selenium' or 'api'

    # API Configuration
    rapidapi_key: Optional[str] = None
    rapidapi_host: str = "linkedin-data-api.p.rapidapi.com"
    jsearch_api_key: Optional[str] = None
    jsearch_api_host: str = "jsearch.p.rapidapi.com"
    linkedin_api_key: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
