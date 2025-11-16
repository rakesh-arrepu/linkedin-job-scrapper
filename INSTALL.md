# Installation Guide

Complete installation instructions for LinkedIn Job Scraper.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Python 3.13+ Users](#python-313-users-important)
- [Troubleshooting](#troubleshooting)
- [Verification](#verification)

## Prerequisites

### Required Software

1. **Python 3.8 or higher** (Python 3.13 supported)
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Google Chrome Browser**
   - Download from: https://www.google.com/chrome/
   - ChromeDriver will be auto-downloaded by the scraper

3. **pip** (Python package manager)
   ```bash
   pip --version
   # or
   pip3 --version
   ```

## Installation Methods

### Method 1: Standard Installation (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/linkedin-job-scrapper.git
cd linkedin-job-scrapper

# 2. Create virtual environment (recommended)
python3 -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python test_setup.py
```

### Method 2: Development Installation

```bash
# After cloning and activating virtual environment
pip install -e .

# This installs the package in editable mode
# and adds the 'linkedin-scraper' command
```

### Method 3: Using pip (if published to PyPI)

```bash
pip install linkedin-job-scraper
```

## Python 3.13+ Users (IMPORTANT)

If you're using Python 3.13 or higher, you might encounter this error:

```
ModuleNotFoundError: No module named 'distutils'
```

### Solution

The `requirements.txt` file has been updated to include `setuptools`, which provides `distutils` compatibility:

```bash
# Make sure to install with the updated requirements.txt
pip install -r requirements.txt

# Or install setuptools separately first
pip install setuptools>=68.0.0
pip install -r requirements.txt
```

### Why This Happens

- Python 3.12+ removed the deprecated `distutils` module
- Some dependencies (like `undetected-chromedriver`) still rely on it
- Installing `setuptools` provides backward compatibility

## Step-by-Step Installation for Python 3.13

```bash
# 1. Clone repository
git clone https://github.com/yourusername/linkedin-job-scrapper.git
cd linkedin-job-scrapper

# 2. Create virtual environment with Python 3.13
python3.13 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install setuptools first (IMPORTANT for Python 3.12+)
pip install setuptools>=68.0.0

# 6. Install all dependencies
pip install -r requirements.txt

# 7. Verify installation
python test_setup.py

# 8. Test the CLI
python main.py --help
```

## Platform-Specific Instructions

### macOS

```bash
# Install Python 3 (if not installed)
brew install python@3.13

# Follow standard installation steps above
```

### Linux (Ubuntu/Debian)

```bash
# Install Python 3 and venv
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# Follow standard installation steps
```

### Windows

```powershell
# Install Python from python.org
# Make sure to check "Add Python to PATH" during installation

# Follow standard installation steps using PowerShell or CMD
```

## Troubleshooting

### Issue 1: `ModuleNotFoundError: No module named 'distutils'`

**Solution:**
```bash
pip install setuptools>=68.0.0
pip install -r requirements.txt
```

### Issue 2: `No module named 'lxml'`

**Solution (macOS):**
```bash
# Install libxml2
brew install libxml2 libxslt
pip install lxml>=5.0.0
```

**Solution (Linux):**
```bash
# Install development packages
sudo apt-get install python3-dev libxml2-dev libxslt1-dev
pip install lxml>=5.0.0
```

### Issue 3: ChromeDriver Issues

**Solution:**
```bash
# The scraper auto-downloads ChromeDriver
# If issues persist, ensure Chrome is installed and updated
google-chrome --version  # Linux/macOS
# or check in Applications on macOS / Program Files on Windows
```

### Issue 4: Permission Denied on macOS/Linux

**Solution:**
```bash
# Make scripts executable
chmod +x main.py
chmod +x test_setup.py
```

### Issue 5: SSL Certificate Errors

**Solution:**
```bash
# Upgrade pip and certificates
pip install --upgrade pip certifi
```

### Issue 6: Pandas Installation Fails

**Solution:**
```bash
# Install numpy first
pip install numpy
pip install pandas
```

### Issue 7: Virtual Environment Not Activating

**Solution:**

On macOS/Linux:
```bash
# Try with full path
source ./venv/bin/activate
```

On Windows:
```powershell
# If PowerShell execution policy blocks it
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

## Verification

### Step 1: Run the Test Script

```bash
python test_setup.py
```

Expected output:
```
🔍 LinkedIn Job Scraper - System Check

Testing LinkedIn Job Scraper - Import Verification
============================================================
Python version: 3.13.x
...
✅ All imports successful! The project is ready to use.
```

### Step 2: Test the CLI

```bash
python main.py --help
```

Expected output:
```
Usage: main.py [OPTIONS]

  LinkedIn Job Scraper - Find and export job listings from LinkedIn.
  ...
```

### Step 3: Run a Small Test Scrape

```bash
# Test with just 5 jobs
python main.py -k "Python Developer" -l "Remote" -m 5 --verbose
```

## Post-Installation

### Create Output Directory

```bash
mkdir -p output
```

### Configure Environment (Optional)

```bash
cp .env.example .env
# Edit .env with your preferences
nano .env  # or use any text editor
```

### Check Chrome Version

```bash
# Ensure Chrome is installed and updated
google-chrome --version
```

## Updating

To update the scraper to the latest version:

```bash
cd linkedin-job-scrapper
git pull origin main
pip install --upgrade -r requirements.txt
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove project (if desired)
cd ..
rm -rf linkedin-job-scrapper
```

## Getting Help

If you encounter issues:

1. Check this installation guide
2. Run `python test_setup.py` to diagnose problems
3. Check the main [README.md](README.md) troubleshooting section
4. Search existing GitHub issues
5. Create a new issue with:
   - Your Python version (`python --version`)
   - Your OS and version
   - Full error message
   - Output of `python test_setup.py`

## Quick Reference

```bash
# Installation
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install setuptools>=68.0.0  # For Python 3.12+
pip install -r requirements.txt

# Verification
python test_setup.py
python main.py --help

# Usage
python main.py -k "Job Title" -l "Location" -m 50

# Deactivate
deactivate
```

---

**Need more help?** Check [README.md](README.md) or create an issue on GitHub.
