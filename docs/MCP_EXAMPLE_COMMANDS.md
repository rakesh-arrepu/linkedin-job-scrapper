# Selenium MCP Server - Example Commands

This document contains example commands you can use with the Selenium MCP server through Claude or other AI assistants.

## Getting Started

### 1. Start a Browser Session

```
"Start a Chrome browser in headless mode"
```

or for visual debugging:

```
"Start a Chrome browser with the window visible"
```

## LinkedIn Job Scraping Examples

### 2. Navigate to LinkedIn Jobs

```
"Use the Selenium MCP server to navigate to https://www.linkedin.com/jobs/"
```

### 3. Search for Jobs

```
"Using the Selenium MCP server:
1. Navigate to https://www.linkedin.com/jobs/
2. Find the job search input field
3. Type 'Python Developer' into it
4. Click the search button"
```

### 4. Explore Page Structure

```
"Navigate to LinkedIn jobs search page and tell me:
1. What CSS selector identifies job cards
2. How many job cards are visible on the page
3. Take a screenshot of the results"
```

### 5. Extract Job Information

```
"On the LinkedIn jobs page:
1. Find all job card elements
2. For each card, extract:
   - Job title
   - Company name
   - Location
3. Return the first 5 jobs as a list"
```

### 6. Test Popup Handling

```
"Navigate to LinkedIn jobs and check if any popups appear.
If they do, tell me:
1. What type of popup (sign-in, cookie consent, etc.)
2. What selector I can use to close it
3. Take a screenshot before and after closing"
```

### 7. Scroll Testing

```
"On LinkedIn jobs search results:
1. Scroll down the page 3 times
2. Check if new jobs load
3. Tell me if it uses infinite scroll or pagination"
```

### 8. Click Into Job Details

```
"Using Selenium MCP:
1. Navigate to LinkedIn jobs for 'Data Scientist'
2. Click on the first job card
3. Wait 2 seconds for the detail panel to load
4. Extract the full job description
5. Take a screenshot"
```

## Advanced Scraping Scenarios

### 9. Test Different Selectors

```
"Help me find the best CSS selector for LinkedIn job cards by:
1. Navigating to the jobs page
2. Testing these selectors:
   - div.job-search-card
   - div.base-card
   - li.jobs-search-results__list-item
3. Tell me which one finds the most elements"
```

### 10. Extract Detailed Job Data

```
"Navigate to this job URL: [paste LinkedIn job URL]
Then extract:
1. Job title
2. Company name
3. Location
4. Posted date
5. Number of applicants
6. Required skills (if listed)
7. Employment type (Full-time, Part-time, etc.)
8. Experience level"
```

### 11. Handle Authentication

```
"Check if LinkedIn requires login to view job details.
If it shows a login prompt:
1. Take a screenshot of it
2. Tell me what selector can close it
3. Try to access jobs without logging in"
```

### 12. Test Rate Limiting

```
"Perform this sequence:
1. Load 5 different job postings rapidly
2. Note if LinkedIn shows any blocking or rate limit messages
3. Tell me what happened and take screenshots of any warnings"
```

## Debugging & Testing

### 13. Find Broken Selectors

```
"I have this selector in my code: '.topcard__org-name-link'
Navigate to a LinkedIn job detail page and tell me:
1. Does this selector exist?
2. If not, what's the current selector for company name?
3. Show me alternatives"
```

### 14. Compare Page Structures

```
"Compare these two LinkedIn job pages:
- [URL 1]
- [URL 2]

Tell me if they use the same HTML structure and selectors"
```

### 15. Screenshot Documentation

```
"Create a visual guide by:
1. Navigating to LinkedIn jobs search
2. Taking screenshots of:
   - The search page
   - A job card (zoomed/highlighted)
   - The job detail panel
   - Any popups that appear
Save these with descriptive names"
```

## API Alternatives Research

### 16. Inspect Network Requests

```
"While navigating LinkedIn jobs:
1. Execute JavaScript to log all XHR/fetch requests
2. Tell me if LinkedIn uses any JSON APIs
3. Share the API endpoint URLs if found"
```

### 17. Check Page Source

```
"Get the page source of LinkedIn jobs search and tell me:
1. Is job data embedded in the HTML?
2. Or is it loaded via JavaScript?
3. Are there any data- attributes with job info?"
```

## Integration Testing

### 18. Test Current Scraper Logic

```
"Simulate my scraper's workflow:
1. Navigate to LinkedIn jobs
2. Search for 'Software Engineer'
3. Handle any popups
4. Scroll to load more jobs
5. Extract the first 10 job cards
6. For each card, click and extract detailed info
7. Report any errors or issues encountered"
```

### 19. Validate Selectors from Code

```
"I use these selectors in my scraper:
- Job cards: 'div.job-search-card'
- Title: '.base-search-card__title'
- Company: '.base-search-card__subtitle'
- Location: '.job-search-card__location'

Navigate to LinkedIn jobs and validate each selector still works"
```

### 20. Performance Testing

```
"Time how long it takes to:
1. Load LinkedIn jobs page
2. Extract 20 job listings
3. Click into 5 job details
Tell me the total time and any bottlenecks"
```

## Tips for Using MCP Commands

### Be Specific
Instead of: "Check LinkedIn"
Use: "Navigate to https://www.linkedin.com/jobs/search/?keywords=Python and take a screenshot"

### Break Down Complex Tasks
Instead of: "Scrape all jobs"
Use: Step-by-step instructions with verification points

### Request Screenshots
Screenshots help verify what the MCP server is seeing

### Handle Errors Gracefully
Ask the AI to report errors and suggest fixes

### Save Findings
Ask Claude to document what works for your scraper code

## Comparison: MCP vs Your Current Code

| Task | MCP Command | Current Code |
|------|-------------|--------------|
| **Navigate** | "Navigate to [URL]" | `self.browser.get(url)` |
| **Find element** | "Find element with selector..." | `driver.find_element(By.CSS_SELECTOR, ...)` |
| **Click** | "Click on element..." | `element.click()` |
| **Extract text** | "Get text from element..." | `element.get_text(strip=True)` |
| **Screenshot** | "Take a screenshot" | Manual implementation needed |
| **Debug** | "Show me what selector works" | Trial and error in code |

## Next Steps

1. Try simple commands first (navigate, screenshot)
2. Build up to complex workflows
3. Document what works in your code
4. Update `linkedin_scraper.py` with findings

---

**Remember**: The MCP server is for exploration and testing. Your production scraper should use direct Selenium code for reliability and speed!
