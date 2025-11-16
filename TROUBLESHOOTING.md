# Troubleshooting Guide

Common issues and solutions for LinkedIn Job Scraper.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Import Errors](#import-errors)
- [Runtime Errors](#runtime-errors)
- [Scraping Issues](#scraping-issues)
- [Export Issues](#export-issues)

---

## Installation Issues

### ❌ `ModuleNotFoundError: No module named 'distutils'`

**Cause:** Python 3.12+ removed the deprecated `distutils` module.

**Solution:**
```bash
pip install setuptools>=68.0.0
pip install -r requirements.txt
```

**Why:** `undetected-chromedriver` depends on `distutils`. The `setuptools` package provides compatibility.

**Verification:**
```bash
python -c "from distutils.version import LooseVersion; print('OK')"
# Should print: OK
```

---

### ❌ `ERROR: Could not find a version that satisfies the requirement`

**Cause:** Python version too old or pip out of date.

**Solution:**
```bash
# Update pip
pip install --upgrade pip

# Check Python version
python --version  # Should be 3.8+

# Try installing again
pip install -r requirements.txt
```

---

### ❌ `lxml` installation fails on macOS

**Error:**
```
error: command 'clang' failed with exit status 1
```

**Solution:**
```bash
# Install dependencies
brew install libxml2 libxslt

# Install lxml
pip install lxml>=5.0.0
```

---

### ❌ `lxml` installation fails on Linux

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libxml2-dev libxslt1-dev

# Fedora/RHEL
sudo yum install python3-devel libxml2-devel libxslt-devel

# Then install lxml
pip install lxml>=5.0.0
```

---

## Import Errors

### ❌ `ImportError: cannot import name 'Job' from 'src.models.job'`

**Cause:** Python can't find the project modules.

**Solution:**
```bash
# Make sure you're in the project root directory
cd /path/to/linkedin-job-scrapper

# Run from project root
python main.py --help
```

---

### ❌ `ModuleNotFoundError: No module named 'undetected_chromedriver'`

**Solution:**
```bash
# Reinstall undetected-chromedriver
pip install undetected-chromedriver>=3.5.5

# If that fails, try
pip install undetected-chromedriver --no-cache-dir
```

---

### ❌ `ImportError: DLL load failed` (Windows)

**Solution:**
```bash
# Install Visual C++ Redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

# Or install specific packages with binaries
pip install --only-binary :all: lxml pandas matplotlib
```

---

## Runtime Errors

### ❌ ChromeDriver issues

**Error:**
```
selenium.common.exceptions.SessionNotCreatedException:
Message: session not created: This version of ChromeDriver only supports Chrome version X
```

**Solution 1: Update Chrome**
```bash
# macOS
brew upgrade --cask google-chrome

# Linux
sudo apt update && sudo apt upgrade google-chrome-stable

# Windows: Download latest from https://www.google.com/chrome/
```

**Solution 2: Let undetected-chromedriver auto-download**
```bash
# Remove existing chromedriver
rm chromedriver  # or delete manually

# Run the scraper - it will auto-download the correct version
python main.py --help
```

---

### ❌ `selenium.common.exceptions.WebDriverException: unknown error: cannot find Chrome binary`

**Cause:** Chrome is not installed.

**Solution:**
Install Google Chrome from https://www.google.com/chrome/

**Verification:**
```bash
# macOS/Linux
google-chrome --version
# or
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version
```

---

### ❌ `Permission denied` errors on macOS/Linux

**Solution:**
```bash
# Make scripts executable
chmod +x main.py
chmod +x test_setup.py

# Or run with python explicitly
python main.py -k "Developer"
```

---

## Scraping Issues

### ❌ No jobs found

**Causes & Solutions:**

1. **Too narrow search criteria**
   ```bash
   # Try broader keywords
   python main.py -k "Developer" -m 50  # Instead of "Senior Python Django Developer"
   ```

2. **LinkedIn blocking**
   ```bash
   # Increase delays in .env
   MIN_DELAY=5
   MAX_DELAY=10

   # Use non-headless mode
   python main.py -k "Developer" --no-headless
   ```

3. **Wrong location format**
   ```bash
   # Use simple location names
   python main.py -k "Developer" -l "New York"  # Good
   python main.py -k "Developer" -l "New York, NY, USA"  # May not work
   ```

---

### ❌ Bot detection / CAPTCHA

**Solutions:**

1. **Increase delays**
   ```bash
   # Edit .env
   MIN_DELAY=5
   MAX_DELAY=10
   DELAY_BETWEEN_REQUESTS=5
   ```

2. **Use non-headless mode**
   ```bash
   python main.py -k "Developer" --no-headless
   # Manually solve CAPTCHA if it appears
   ```

3. **Reduce scraping volume**
   ```bash
   # Scrape fewer jobs at a time
   python main.py -k "Developer" -m 10  # Instead of -m 500
   ```

4. **Use VPN or different network**

5. **Wait before retrying** (LinkedIn may have rate-limited your IP)

---

### ❌ Scraper stops mid-way

**Cause:** Network timeout or element not found.

**Solution:**
```bash
# Increase timeout in .env
PAGE_LOAD_TIMEOUT=60

# Run with verbose logging
python main.py -k "Developer" -m 50 --verbose

# Check scraper.log for details
tail -f scraper.log
```

---

## Export Issues

### ❌ PDF generation fails

**Error:**
```
OSError: cannot open resource
```

**Solution:**
```bash
# Reinstall reportlab
pip install --upgrade --force-reinstall reportlab

# Check font support
python -c "from reportlab.pdfbase import pdfmetrics; print('OK')"
```

---

### ❌ Charts not appearing in PDF

**Solution:**
```bash
# Reinstall matplotlib
pip install --upgrade matplotlib

# Test matplotlib backend
python -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; print('OK')"
```

---

### ❌ CSV encoding issues (special characters)

**Solution:**
The scraper uses UTF-8 encoding. To open in Excel:

**Windows:**
1. Open Excel
2. Go to Data > Get Data > From Text/CSV
3. Select the file
4. Choose "UTF-8" encoding
5. Click Load

**macOS:**
CSV files should open correctly by default in Numbers or Excel.

---

### ❌ Permission denied when saving files

**Solution:**
```bash
# Create output directory
mkdir -p output

# Check permissions
ls -la output/

# If needed, fix permissions
chmod 755 output/
```

---

## Advanced Troubleshooting

### Run Diagnostic Test

```bash
python test_setup.py
```

This will check:
- Python version
- All required packages
- Project imports
- Basic functionality
- Export capabilities

### Enable Debug Logging

```bash
# Method 1: CLI flag
python main.py -k "Developer" --verbose

# Method 2: Edit .env
LOG_LEVEL=DEBUG

# Check logs
tail -f scraper.log
```

### Test Individual Components

```python
# Test imports
python -c "from src.scraper.linkedin_scraper import LinkedInScraper; print('OK')"

# Test browser
python -c "from src.scraper.browser_manager import BrowserManager; bm = BrowserManager(headless=True); bm.start(); print('OK'); bm.close()"

# Test models
python -c "from src.models.job import Job; j = Job(title='Test', company='Test', location='Test', job_url='http://test.com'); print(j)"
```

### Check System Resources

```bash
# Check memory
free -h  # Linux
top  # macOS

# Check disk space
df -h

# Check Chrome processes
ps aux | grep chrome
```

### Clean Installation

If all else fails:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove cache
rm -rf __pycache__ src/__pycache__ src/*/__pycache__

# Start fresh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install setuptools>=68.0.0
pip install -r requirements.txt

# Verify
python test_setup.py
```

---

## Getting Help

If you still have issues:

1. **Run diagnostics:**
   ```bash
   python test_setup.py > diagnostics.txt 2>&1
   ```

2. **Collect information:**
   - Python version: `python --version`
   - OS version: `uname -a` (macOS/Linux) or `ver` (Windows)
   - Chrome version: `google-chrome --version`
   - Error message from `scraper.log`

3. **Search existing issues:**
   https://github.com/yourusername/linkedin-job-scrapper/issues

4. **Create new issue** with:
   - Clear description
   - Steps to reproduce
   - Error message
   - Diagnostic output
   - Your environment details

---

## Quick Reference

| Error | Quick Fix |
|-------|-----------|
| `distutils` not found | `pip install setuptools>=68.0.0` |
| Can't find Chrome | Install from https://www.google.com/chrome/ |
| Import errors | `pip install -r requirements.txt --force-reinstall` |
| No jobs found | Use broader keywords, check location |
| Bot detection | Increase delays, use `--no-headless` |
| PDF errors | `pip install --upgrade reportlab matplotlib` |
| Timeout errors | Increase `PAGE_LOAD_TIMEOUT` in .env |

---

**Still stuck?** Create an issue with full error details!
