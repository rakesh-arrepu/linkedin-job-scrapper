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
            options = self._get_chrome_options()

            # Try to start browser with SSL certificate verification
            try:
                self.driver = uc.Chrome(options=options, version_main=None)
            except Exception as ssl_error:
                # Check if it's an SSL certificate error
                if 'SSL' in str(ssl_error) or 'CERTIFICATE' in str(ssl_error):
                    logger.warning("SSL certificate error detected. Trying workaround...")
                    logger.warning("To fix this permanently, run: python fix_ssl_certificates.py")

                    # Try setting SSL context to unverified (not recommended but works)
                    try:
                        import ssl
                        ssl._create_default_https_context = ssl._create_unverified_context
                        self.driver = uc.Chrome(options=options, version_main=None)
                        logger.warning("⚠️  Using unverified SSL context (not secure)")
                    except Exception as retry_error:
                        logger.error(f"Failed to start browser even with SSL workaround: {retry_error}")
                        raise Exception(
                            "SSL certificate verification failed. Please run:\n"
                            "  python fix_ssl_certificates.py\n"
                            "Or manually install certificates for Python:\n"
                            "  pip install --upgrade certifi\n"
                            f"Original error: {ssl_error}"
                        )
                else:
                    raise

            # Set window size
            self.driver.set_window_size(
                settings.browser_window_width,
                settings.browser_window_height
            )

            # Initialize wait
            self.wait = WebDriverWait(self.driver, settings.page_load_timeout)

            # Execute stealth scripts
            self._apply_stealth_scripts()

            logger.info("Browser started successfully")
            return self.driver

        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise

    def _get_chrome_options(self) -> Options:
        """
        Get Chrome options with anti-detection settings.

        Returns:
            Chrome options
        """
        options = uc.ChromeOptions()

        # Headless mode
        if self.headless:
            options.add_argument('--headless=new')

        # Anti-detection arguments
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')

        # Random user agent
        ua = UserAgent()
        options.add_argument(f'--user-agent={ua.random}')

        # Language
        options.add_argument('--lang=en-US')

        # Preferences
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2,
                'images': 2,  # Disable images for faster loading
            },
            'profile.managed_default_content_settings': {
                'images': 2
            }
        }
        options.add_experimental_option('prefs', prefs)

        # Exclude automation switches
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)

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
