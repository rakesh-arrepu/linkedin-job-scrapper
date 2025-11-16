# Contributing to LinkedIn Job Scraper

First off, thank you for considering contributing to LinkedIn Job Scraper! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (command-line arguments, screenshots, etc.)
- **Describe the behavior you observed** and what you expected
- **Include logs** from `scraper.log`
- **Specify your environment**:
  - OS (Windows, macOS, Linux)
  - Python version
  - Chrome version

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List some examples** of how it would be used

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the code follows the existing style
4. Update the README.md with details of changes if needed
5. Issue the pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/linkedin-job-scrapper.git
cd linkedin-job-scrapper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Add comments for complex logic

### Example:

```python
def scrape_jobs(keywords: str, location: str) -> List[Job]:
    """
    Scrape jobs from LinkedIn.

    Args:
        keywords: Search keywords
        location: Job location

    Returns:
        List of Job objects
    """
    # Implementation
    pass
```

## Testing

Before submitting a PR, test your changes:

```bash
# Run the scraper with various options
python main.py -k "Python Developer" -m 10 --verbose

# Test different export formats
python main.py -k "Data Scientist" -m 5 -f pdf
python main.py -k "DevOps" -m 5 -f csv
python main.py -k "Designer" -m 5 -f json
```

## Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- [ ] Improved error handling and retry logic
- [ ] Better CAPTCHA handling
- [ ] Support for more LinkedIn regions/languages
- [ ] Performance optimizations
- [ ] Better job detail extraction

### Medium Priority
- [ ] Web dashboard (Flask/Streamlit)
- [ ] Email notifications
- [ ] Scheduled scraping (cron jobs)
- [ ] Job deduplication
- [ ] Database integration (SQLite/PostgreSQL)

### Documentation
- [ ] Video tutorials
- [ ] More usage examples
- [ ] API documentation
- [ ] Troubleshooting guides

### Nice to Have
- [ ] Docker support
- [ ] CI/CD pipeline
- [ ] Unit tests
- [ ] Integration tests
- [ ] Chrome extension

## Questions?

Feel free to create an issue labeled "question" if you need help or clarification.

Thank you for contributing! 🚀
