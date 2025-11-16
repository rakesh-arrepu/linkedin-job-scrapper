"""Browser management with Selenium and stealth mode."""

import os
import random
import ssl
import time
from typing import Optional

import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from src.utils.logger import logger

# Fix SSL certificate issues
try:
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
except ImportError:
    logger.warning("certifi not installed, SSL verification may fail")


class BrowserManager:
    """Manages browser instance with anti-detection measures."""

    def __init__(self, headless: bool = True):
        """
        Initialize browser manager.

        Args:
            headless: Whether to run browser in headless mode
        """
        self.headless = headless
        self.driver: Optional[uc.Chrome] = None
        self.wait: Optional[WebDriverWait] = None

    def start(self) -> uc.Chrome:
        """
        Start browser with stealth configuration.

        Returns:
            Chrome driver instance
        """
        logger.info("Starting browser...")

        try:
            # Set SSL context to unverified to avoid SSL errors
            try:
                import ssl
                ssl._create_default_https_context = ssl._create_unverified_context
            except:
                pass

            options = self._get_chrome_options()

            # Start browser with simplified approach
            logger.info("Initializing Chrome driver...")
            self.driver = uc.Chrome(
                options=options,
                use_subprocess=True,
                version_main=None
            )

            logger.info("Chrome driver started")

            # Set window size
            try:
                self.driver.set_window_size(
                    settings.browser_window_width,
                    settings.browser_window_height
                )
            except:
                pass  # Window size is optional

            # Initialize wait
            self.wait = WebDriverWait(self.driver, settings.page_load_timeout)

            # Execute stealth scripts
            try:
                self._apply_stealth_scripts()
            except Exception as e:
                logger.warning(f"Stealth scripts failed (non-critical): {e}")

            logger.info("Browser started successfully")
            return self.driver

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to start browser: {error_msg}")

            # Provide helpful error messages
            if 'SSL' in error_msg or 'CERTIFICATE' in error_msg:
                logger.error("SSL certificate error. Run: python fix_ssl_certificates.py")
            elif 'chrome' in error_msg.lower():
                logger.error("Chrome/ChromeDriver issue. Ensure Chrome is installed.")
            elif 'excludeSwitches' in error_msg or 'capability' in error_msg:
                logger.error("ChromeDriver compatibility issue. This has been fixed, please pull latest code.")

            raise

    def _get_chrome_options(self):
        """
        Get Chrome options with anti-detection settings.

        Returns:
            Chrome options
        """
        options = uc.ChromeOptions()

        # Basic arguments that work with undetected_chromedriver
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--lang=en-US')
        options.add_argument('--window-size=1920,1080')

        # Headless mode (if requested)
        if self.headless:
            options.add_argument('--headless=new')

        # User agent
        try:
            ua = UserAgent()
            options.add_argument(f'--user-agent={ua.random}')
        except:
            # Fallback to default if UserAgent fails
            pass

        # Preferences (simpler version without experimental options that cause issues)
        try:
            prefs = {
                'profile.default_content_setting_values.notifications': 2,
            }
            options.add_experimental_option('prefs', prefs)
        except:
            # If experimental options fail, skip them
            pass

        return options

    def _apply_stealth_scripts(self):
        """Apply JavaScript to hide automation."""
        if not self.driver:
            return

        # Override navigator.webdriver
        stealth_scripts = [
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
            "window.chrome = { runtime: {} }",
        ]

        for script in stealth_scripts:
            try:
                self.driver.execute_script(script)
            except Exception as e:
                logger.debug(f"Failed to execute stealth script: {e}")

    def get(self, url: str, retry: int = 3) -> bool:
        """
        Navigate to URL with retry logic.

        Args:
            url: URL to navigate to
            retry: Number of retries

        Returns:
            True if successful, False otherwise
        """
        for attempt in range(retry):
            try:
                logger.info(f"Navigating to: {url}")
                self.driver.get(url)

                # Random delay to mimic human behavior
                time.sleep(random.uniform(1, 3))

                return True

            except TimeoutException:
                logger.warning(f"Timeout loading {url}, attempt {attempt + 1}/{retry}")
                if attempt < retry - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to load {url} after {retry} attempts")
                    return False

            except WebDriverException as e:
                logger.error(f"WebDriver error: {e}")
                return False

        return False

    def scroll_slowly(self, scroll_pause: float = 0.5):
        """
        Scroll page slowly to mimic human behavior.

        Args:
            scroll_pause: Pause between scrolls in seconds
        """
        if not self.driver:
            return

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait for page to load
            time.sleep(scroll_pause)

            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

        # Scroll back to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(scroll_pause)

    def wait_for_element(
        self,
        by: By,
        value: str,
        timeout: Optional[int] = None
    ):
        """
        Wait for element to be present.

        Args:
            by: Selenium By locator
            value: Element selector
            timeout: Optional timeout override

        Returns:
            WebElement if found, None otherwise
        """
        if not self.driver:
            return None

        try:
            wait_time = timeout or settings.page_load_timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Element not found: {value}")
            return None

    def close(self):
        """Close browser gracefully."""
        if self.driver:
            try:
                logger.info("Closing browser...")
                self.driver.quit()
                self.driver = None
                logger.info("Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
