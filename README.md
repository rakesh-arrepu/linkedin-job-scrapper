# 🚀 LinkedIn Job Scraper

A powerful, feature-rich Python tool to scrape LinkedIn job postings and generate beautiful, detailed reports in PDF, CSV, and JSON formats.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%20|%203.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13 Compatible](https://img.shields.io/badge/python%203.13-compatible-brightgreen.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🔍 **Advanced Search Filters**: Keywords, location, date range, experience level, job type, remote options
- 📊 **Detailed PDF Reports**: Professional reports with charts, statistics, and formatted job listings
- 📁 **Multiple Export Formats**: PDF, CSV, and JSON
- 🎭 **Stealth Mode**: Anti-detection measures using undetected-chromedriver
- 🌐 **Global Support**: Works across different LinkedIn regions
- 💻 **Beautiful CLI**: Rich terminal interface with progress bars and colors
- 🔄 **Pagination Support**: Scrape multiple pages of results
- 📈 **Job Market Analytics**: Top companies, locations, and skills analysis
- 🎨 **Customizable**: Configure via environment variables or CLI arguments
- 🆓 **100% Free**: No API keys or paid services required

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Examples](#-examples)
- [Configuration](#-configuration)
- [Output Formats](#-output-formats)
- [Legal Disclaimer](#-legal-disclaimer)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[INSTALL.md](INSTALL.md)** - Detailed installation guide
- **[SSL_FIX.md](SSL_FIX.md)** - Fix SSL certificate errors (macOS)
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[API.md](docs/API.md)** - Programmatic usage
- **[DOCKER.md](docs/DOCKER.md)** - Docker deployment

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher (Python 3.13 supported ✅)
- Chrome browser (ChromeDriver will be auto-downloaded)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/linkedin-job-scrapper.git
cd linkedin-job-scrapper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_setup.py
```

### ⚠️ Common Issues

**Python 3.13+ - `ModuleNotFoundError: No module named 'distutils'`:**
```bash
pip install "setuptools>=68.0.0"
pip install -r requirements.txt
```

**macOS - SSL Certificate Error:**
```bash
# Quick fix
pip install --upgrade certifi
export SSL_CERT_FILE=$(python -m certifi)

# Or run the fix script
python fix_ssl_certificates.py
```

**See [INSTALL.md](INSTALL.md) for detailed installation and [SSL_FIX.md](SSL_FIX.md) for SSL troubleshooting.**

## 🚀 Quick Start

### Basic Search

```bash
python main.py --keywords "Python Developer" --location "Remote"
```

### With More Options

```bash
python main.py \
  --keywords "Data Scientist" \
  --location "New York" \
  --date-posted week \
  --max-jobs 100 \
  --format pdf
```

## 📖 Usage

### Command Line Options

```
Options:
  -k, --keywords TEXT            Job keywords (REQUIRED)
                                 Examples: "Python Developer", "Data Scientist"

  -l, --location TEXT            Job location
                                 Examples: "New York", "Remote", "United States"

  -d, --date-posted [24h|week|month|any]
                                 Date range for job postings (default: any)

  -e, --experience [1|2|3|4|5|6] Experience level (can be multiple)
                                 1=Internship, 2=Entry, 3=Associate
                                 4=Mid-Senior, 5=Director, 6=Executive

  -t, --job-type [F|P|C|T|I|V|O] Job type (can be multiple)
                                 F=Full-time, P=Part-time, C=Contract
                                 T=Temporary, I=Internship, V=Volunteer, O=Other

  -r, --remote-only              Show only remote jobs

  -m, --max-jobs INTEGER         Maximum number of jobs to scrape (default: 50)

  -o, --output PATH              Output file path (without extension)

  -f, --format [pdf|csv|json|all]
                                 Output format (default: all)

  --headless/--no-headless       Run browser in headless mode (default: headless)

  --enrich                       Enrich jobs with detailed information
                                 (slower but includes description, skills, etc.)

  -v, --verbose                  Enable verbose logging

  --help                         Show this message and exit
```

## 💡 Examples

### 1. Search for Python Jobs (Remote)

```bash
python main.py -k "Python Developer" -l "Remote" -m 50
```

### 2. Search for Data Science Jobs (Posted This Week)

```bash
python main.py -k "Data Scientist" -d week -m 100
```

### 3. Search for Entry-Level Software Engineering Jobs

```bash
python main.py -k "Software Engineer" -e 2 -t F -m 75
```

### 4. Search with Multiple Experience Levels

```bash
python main.py -k "DevOps Engineer" -e 3 -e 4 -l "San Francisco" -m 100
```

### 5. Export Only to CSV

```bash
python main.py -k "Product Manager" -l "New York" -f csv -m 50
```

### 6. Detailed Search with Enrichment

```bash
python main.py \
  --keywords "Machine Learning Engineer" \
  --location "Remote" \
  --date-posted week \
  --experience 4 \
  --job-type F \
  --max-jobs 100 \
  --enrich \
  --format all \
  --output ml_jobs
```

### 7. Search Multiple Job Types

```bash
python main.py -k "Full Stack Developer" -t F -t C -l "Austin" -m 80
```

### 8. Remote-Only Full-Time Jobs

```bash
python main.py -k "Backend Engineer" --remote-only -t F -m 100
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Scraping Settings
MAX_JOBS=50
DELAY_BETWEEN_REQUESTS=3
PAGE_LOAD_TIMEOUT=30
HEADLESS_MODE=true

# Browser Settings
BROWSER_WINDOW_WIDTH=1920
BROWSER_WINDOW_HEIGHT=1080

# Output Settings
OUTPUT_DIR=./output
DEFAULT_OUTPUT_FORMAT=pdf

# Logging
LOG_LEVEL=INFO
LOG_FILE=scraper.log

# Rate Limiting
MIN_DELAY=2
MAX_DELAY=5
RANDOM_DELAY=true
```

## 📦 Output Formats

### 📄 PDF Report

Professional PDF report includes:
- **Header**: Search parameters and metadata
- **Statistics Section**:
  - Top 10 companies (bar chart)
  - Top 10 locations (bar chart)
  - Summary statistics table
- **Job Listings**: Detailed cards for each job with:
  - Company name and logo area
  - Job title and location
  - Employment type and experience level
  - Posted date and applicant count
  - Skills required
  - Direct link to job posting

### 📊 CSV Export

Structured CSV with columns:
- Title
- Company
- Location
- Employment Type
- Experience Level
- Posted Date
- Applicants Count
- Salary Range
- Skills
- Job URL
- Job ID
- Scraped At

### 📋 JSON Export

Structured JSON with:
```json
{
  "total_jobs": 50,
  "jobs": [
    {
      "title": "Senior Python Developer",
      "company": "Google",
      "location": "Remote",
      "job_url": "https://linkedin.com/jobs/view/...",
      "skills": ["Python", "Django", "AWS"],
      ...
    }
  ]
}
```

## 📂 Project Structure

```
linkedin-job-scrapper/
├── src/
│   ├── scraper/
│   │   ├── linkedin_scraper.py    # Main scraping logic
│   │   └── browser_manager.py     # Browser automation
│   ├── models/
│   │   └── job.py                 # Data models
│   ├── exporters/
│   │   ├── pdf_exporter.py        # PDF generation
│   │   ├── csv_exporter.py        # CSV export
│   │   └── json_exporter.py       # JSON export
│   └── utils/
│       ├── logger.py              # Logging setup
│       └── rate_limiter.py        # Rate limiting
├── config/
│   └── settings.py                # Configuration
├── main.py                        # CLI entry point
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
└── README.md                      # Documentation
```

## ⚖️ Legal Disclaimer

**IMPORTANT**: This tool is for educational and personal use only.

- Web scraping may violate LinkedIn's Terms of Service
- This tool should be used responsibly and ethically
- Users are responsible for compliance with LinkedIn's ToS and applicable laws
- Do not use for commercial purposes without proper authorization
- The authors are not responsible for misuse of this tool

### Recommendations:
1. Use for personal job searching only
2. Implement respectful rate limiting (already built-in)
3. Do not scrape excessively
4. Consider using LinkedIn's official API for commercial use
5. Respect robots.txt and website policies

## 🐛 Troubleshooting

### Common Issues

#### ❌ `ModuleNotFoundError: No module named 'distutils'` (Python 3.13+)

```bash
pip install "setuptools>=68.0.0"
pip install -r requirements.txt
```

#### ❌ SSL Certificate Error (macOS)

```bash
# Option 1: Run fix script
python fix_ssl_certificates.py

# Option 2: Manual fix
pip install --upgrade certifi
export SSL_CERT_FILE=$(python -m certifi)
```

See **[SSL_FIX.md](SSL_FIX.md)** for detailed SSL troubleshooting.

#### ❌ ChromeDriver Not Found

The script automatically downloads ChromeDriver. Ensure Chrome browser is installed from https://www.google.com/chrome/

#### ❌ No Jobs Found

- Broaden your search keywords
- Remove strict filters
- Try different location formats
- Check if LinkedIn is accessible in your region

#### ❌ Bot Detection / CAPTCHA

```bash
# Increase delays in .env
MIN_DELAY=5
MAX_DELAY=10

# Or use non-headless mode
python main.py -k "Developer" --no-headless
```

### More Help

See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for comprehensive troubleshooting guide including:
- Installation issues
- Import errors
- Runtime errors
- Scraping issues
- Export problems
- Advanced diagnostics

## 🔍 Tips for Best Results

1. **Use Specific Keywords**: "Python Developer" better than "Developer"
2. **Filter by Date**: Recent jobs (week/month) have higher response rates
3. **Enable Enrichment**: Use `--enrich` for detailed job information
4. **Start Small**: Test with 10-20 jobs before scraping hundreds
5. **Respect Rate Limits**: Don't scrape too frequently
6. **Save Outputs**: Use `--output` to organize your searches
7. **Review Logs**: Check `scraper.log` for debugging

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Selenium](https://www.selenium.dev/) for browser automation
- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) for stealth mode
- [ReportLab](https://www.reportlab.com/) for PDF generation
- [Click](https://click.palletsprojects.com/) for CLI framework
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output

## 📧 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing GitHub issues
3. Create a new issue with detailed information

## 🌟 Star History

If you find this tool helpful, please consider giving it a star ⭐️

---

**Happy Job Hunting! 🎉**

Made with ❤️ by developers, for developers
