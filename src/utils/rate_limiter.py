"""Rate limiting utilities to avoid detection."""

import random
import time
from typing import Optional

from src.utils.logger import logger


class RateLimiter:
    """Handles rate limiting for web scraping."""

    def __init__(
        self,
        min_delay: float = 2.0,
        max_delay: float = 5.0,
        random_delay: bool = True
    ):
        """
        Initialize rate limiter.

        Args:
            min_delay: Minimum delay in seconds
            max_delay: Maximum delay in seconds
            random_delay: Whether to randomize delays
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.random_delay = random_delay
        self.last_request_time: Optional[float] = None

    def wait(self):
        """Wait before next request."""
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time

            if self.random_delay:
                delay = random.uniform(self.min_delay, self.max_delay)
            else:
                delay = self.min_delay

            remaining = delay - elapsed

            if remaining > 0:
                logger.debug(f"Rate limiting: waiting {remaining:.2f}s")
                time.time()
                time.sleep(remaining)

        self.last_request_time = time.time()

    def reset(self):
        """Reset the rate limiter."""
        self.last_request_time = None
