#!/usr/bin/env python3
"""Diagnostic script to understand LinkedIn's job page structure."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def analyze_linkedin_structure():
    """Analyze how LinkedIn job search page works."""

    print("\n" + "="*70)
    print("LINKEDIN STRUCTURE ANALYSIS")
    print("="*70)

    # Setup Chrome
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # Navigate to job search
        url = "https://www.linkedin.com/jobs/search/?keywords=Python%20Developer"
        print(f"\n1. Navigating to: {url}")
        driver.get(url)
        time.sleep(4)

        # Close popups
        try:
            popup = driver.find_element(By.CSS_SELECTOR, 'button[data-tracking-control-name*="modal_dismiss"]')
            popup.click()
            time.sleep(1)
        except:
            pass

        # Get page source and analyze
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Check for main containers
        print("\n2. Checking main page containers:")
        print("   -" * 30)

        containers = {
            'Jobs list container': 'ul.jobs-search__results-list',
            'Job details container': 'div.jobs-search__job-details',
            'Right panel': 'div.jobs-details',
            'Job view layout': 'div.job-view-layout',
            'Base card list': 'div.base-search-card-list'
        }

        for name, selector in containers.items():
            elem = soup.select_one(selector)
            print(f"   {name:30s}: {'✅ FOUND' if elem else '❌ NOT FOUND'}")

        # Find and click first job card
        print("\n3. Finding job cards...")
        cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list > li")
        print(f"   Found {len(cards)} job cards")

        if cards:
            print("\n4. Clicking first job card...")
            first_card = cards[0]

            # Try clicking the card
            first_card.click()
            time.sleep(4)

            # Take screenshot
            driver.save_screenshot("output/structure_after_click.png")

            # Re-analyze page
            soup = BeautifulSoup(driver.page_source, 'lxml')

            print("\n5. After clicking, checking containers again:")
            print("   -" * 30)
            for name, selector in containers.items():
                elem = soup.select_one(selector)
                print(f"   {name:30s}: {'✅ FOUND' if elem else '❌ NOT FOUND'}")

            # Check what changed in URL
            print(f"\n6. Current URL after click: {driver.current_url}")

            # Look for job details in the page
            print("\n7. Looking for job detail selectors:")
            print("   -" * 30)

            detail_selectors = {
                'Job title (h1)': 'h1',
                'Top card title': '.top-card-layout__title',
                'Topcard title': 'h1.topcard__title',
                'Job description': '.show-more-less-html__markup',
                'Description text': '.description__text',
                'Company name': '.topcard__org-name-link',
                'Location': '.topcard__flavor--bullet',
            }

            for name, selector in detail_selectors.items():
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(strip=True)[:100]
                    print(f"   {name:30s}: ✅ '{text}'")
                else:
                    print(f"   {name:30s}: ❌ NOT FOUND")

            # Check if there are multiple sections
            print("\n8. Analyzing page layout...")

            # Look for two-panel layout
            left_panel = soup.select_one('.jobs-search__left-rail, .jobs-search-results-list')
            right_panel = soup.select_one('.jobs-search__right-rail, .jobs-search__job-details')

            print(f"   Left panel (job list): {'✅ FOUND' if left_panel else '❌ NOT FOUND'}")
            print(f"   Right panel (job details): {'✅ FOUND' if right_panel else '❌ NOT FOUND'}")

            # If right panel exists, show what's in it
            if right_panel:
                print("\n9. Right panel content:")
                print("   " + "="*60)
                # Get first 500 chars of right panel text
                panel_text = right_panel.get_text(strip=True)[:500]
                print(f"   {panel_text}")

            # Save full HTML for manual inspection
            with open("output/page_structure.html", "w") as f:
                f.write(driver.page_source)
            print(f"\n✅ Saved full HTML to: output/page_structure.html")

    finally:
        driver.quit()
        print("\n✅ Analysis complete!")

if __name__ == "__main__":
    analyze_linkedin_structure()
