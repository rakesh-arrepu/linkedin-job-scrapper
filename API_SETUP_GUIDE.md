# LinkedIn Job Scraper - API Setup Guide

## Overview

The LinkedIn Job Scraper now supports **two methods** for fetching job data:

1. **API-based** (Recommended) ⭐
   - Faster and more reliable
   - No browser required
   - Better success rate for multiple jobs
   - Returns comprehensive data (description, skills, salary, etc.)
   - Requires API key (free and paid tiers available)

2. **Selenium-based** (Browser automation)
   - Uses browser automation
   - No API key needed
   - Can be blocked by LinkedIn
   - Slower performance
   - Limited success with multiple jobs

---

## Configuration

The scraper method is configured in your `.env` file:

```bash
# Choose scraper method: 'api' or 'selenium'
SCRAPER_METHOD=api
```

You can also override this from the command line:

```bash
python main.py -k "Python Developer" --scraper api
python main.py -k "Data Scientist" --scraper selenium
```

---

## API Setup (Recommended)

### Option 1: RapidAPI LinkedIn Data API

**Best for:** Most users, comprehensive LinkedIn data

#### Steps:

1. **Create RapidAPI Account**
   - Go to: https://rapidapi.com/
   - Sign up for free account

2. **Subscribe to LinkedIn Data API**
   - Visit: https://rapidapi.com/letscrape-6bRBa3QguO5/api/linkedin-data-api
   - Click "Subscribe to Test"
   - Choose a pricing plan:
     - **Basic (Free)**: 100 requests/month
     - **Pro ($9.99/month)**: 1,000 requests/month
     - **Ultra ($49.99/month)**: 10,000 requests/month

3. **Get Your API Key**
   - After subscribing, go to "Endpoints" tab
   - Your API key will be shown in the code snippets
   - Copy the value after `X-RapidAPI-Key:`

4. **Configure Your .env File**
   ```bash
   # .env file
   SCRAPER_METHOD=api
   RAPIDAPI_KEY=your_actual_api_key_here
   RAPIDAPI_HOST=linkedin-data-api.p.rapidapi.com
   ```

---

### Option 2: JSSearch API (Free Tier Available)

**Best for:** Users who want a free option with generous limits

#### Steps:

1. **Create RapidAPI Account**
   - Go to: https://rapidapi.com/
   - Sign up for free account

2. **Subscribe to JSSearch API**
   - Visit: https://rapidapi.com/jsearch/api/jsearch
   - Click "Subscribe to Test"
   - Choose a pricing plan:
     - **Free**: 300 requests/month
     - **Basic ($9.99/month)**: 2,500 requests/month
     - **Pro ($29.99/month)**: 10,000 requests/month

3. **Get Your API Key**
   - After subscribing, go to "Endpoints" tab
   - Copy your API key from the code snippets

4. **Configure Your .env File**
   ```bash
   # .env file
   SCRAPER_METHOD=api
   JSEARCH_API_KEY=your_jsearch_api_key_here
   JSEARCH_API_HOST=jsearch.p.rapidapi.com
   ```

---

## Usage Examples

### Using API Scraper

```bash
# Basic API scraping (uses .env configuration)
python main.py -k "Software Engineer" -l "Remote" -m 20

# Force API mode from command line
python main.py -k "Data Scientist" -l "New York" --scraper api -m 50

# API scraping with all filters
python main.py -k "Python Developer" \
  -l "San Francisco" \
  -d week \
  -m 30 \
  --scraper api \
  -f pdf
```

### Using Selenium Scraper

```bash
# Force Selenium mode
python main.py -k "DevOps Engineer" --scraper selenium -m 10

# Selenium with headless browser
python main.py -k "Frontend Developer" \
  --scraper selenium \
  --headless \
  -m 15
```

---

## API vs Selenium Comparison

| Feature | API | Selenium |
|---------|-----|----------|
| **Speed** | ⚡ Very Fast | 🐌 Slow |
| **Reliability** | ✅ High | ⚠️ Medium |
| **Multiple Jobs** | ✅ Works perfectly | ❌ Limited (only 1-2 jobs) |
| **Data Quality** | ✅ Comprehensive | ⚠️ Limited |
| **Browser Required** | ❌ No | ✅ Yes |
| **API Key Required** | ✅ Yes | ❌ No |
| **Cost** | $ (free tier available) | Free |
| **Risk of Being Blocked** | ❌ None | ⚠️ Possible |
| **Fields Available** | All 12 fields | Varies (7-10 fields) |

---

## Field Availability by Method

### API Scraper (All Fields Available)

| Field | Availability |
|-------|--------------|
| title | ✅ Always |
| company | ✅ Always |
| location | ✅ Always |
| job_url | ✅ Always |
| job_id | ✅ Always |
| description | ✅ ~95% |
| skills | ✅ ~80% |
| employment_type | ✅ ~90% |
| experience_level | ✅ ~85% |
| posted_date | ✅ ~95% |
| applicants_count | ✅ ~60% (RapidAPI) / ❌ Not available (JSSearch) |
| salary_range | ✅ ~40% |

### Selenium Scraper (Limited Fields)

| Field | Availability |
|-------|--------------|
| title | ✅ Always |
| company | ✅ Always |
| location | ✅ Always |
| job_url | ✅ Always |
| description | ⚠️ ~30% (when clicking works) |
| skills | ⚠️ ~20% |
| posted_date | ✅ ~80% |
| **Issue:** Only scrapes 1-2 jobs successfully |

---

## Troubleshooting

### Issue: "No API key configured"

**Solution:**
1. Add API key to your `.env` file
2. Make sure the file is named exactly `.env` (not `.env.example`)
3. Verify the API key is correct (no quotes needed)

```bash
# Correct
RAPIDAPI_KEY=abc123xyz789

# Incorrect
RAPIDAPI_KEY="abc123xyz789"  # Don't use quotes
```

---

### Issue: "API request failed: 401 Unauthorized"

**Solution:**
- Your API key is invalid or expired
- Check you've subscribed to the API on RapidAPI
- Copy the API key again from RapidAPI dashboard

---

### Issue: "API request failed: 429 Too Many Requests"

**Solution:**
- You've exceeded your API rate limit
- Wait for your quota to reset (usually monthly)
- Upgrade to a higher tier plan
- Use `--scraper selenium` as fallback

---

### Issue: Selenium only getting 1 job

**Cause:** This is a known limitation of the Selenium approach. LinkedIn's dynamic content loading makes it difficult to scrape multiple jobs reliably.

**Solution:**
- **Switch to API method** (recommended)
- Add API key to your `.env` file
- Use `SCRAPER_METHOD=api`

---

## Cost Breakdown

### Free Options

1. **JSSearch API (Free Tier)**
   - 300 requests/month
   - Good for ~300 jobs/month
   - **Cost:** $0/month ✅

2. **RapidAPI LinkedIn (Free Tier)**
   - 100 requests/month
   - Good for ~100 jobs/month
   - **Cost:** $0/month ✅

3. **Selenium Scraper**
   - Unlimited requests
   - **Limitation:** Only 1-2 jobs work
   - **Cost:** $0/month

### Paid Options (For Heavy Usage)

1. **JSSearch Pro**
   - 10,000 requests/month
   - **Cost:** $29.99/month
   - Best value for high-volume scraping

2. **RapidAPI LinkedIn Pro**
   - 1,000 requests/month
   - **Cost:** $9.99/month
   - Good for moderate usage

---

## Recommendations

### For Casual Users (1-50 jobs/week)
- ✅ Use **JSSearch Free Tier** (300 requests/month)
- Configure: `SCRAPER_METHOD=api` + `JSEARCH_API_KEY`

### For Regular Users (50-200 jobs/week)
- ✅ Use **RapidAPI LinkedIn Basic** ($9.99/month, 1,000 requests)
- Configure: `SCRAPER_METHOD=api` + `RAPIDAPI_KEY`

### For Heavy Users (500+ jobs/week)
- ✅ Use **JSSearch Pro** ($29.99/month, 10,000 requests)
- Configure: `SCRAPER_METHOD=api` + `JSEARCH_API_KEY`

### For Free Usage Only
- ⚠️ Use **Selenium** (but expect only 1-2 jobs to work)
- Configure: `SCRAPER_METHOD=selenium`
- Alternative: Use free API tier with monthly limits

---

## Quick Start

1. **Get API Key** (choose one):
   - JSSearch (free): https://rapidapi.com/jsearch/api/jsearch
   - RapidAPI LinkedIn: https://rapidapi.com/letscrape-6bRBa3QguO5/api/linkedin-data-api

2. **Configure .env**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   SCRAPER_METHOD=api
   RAPIDAPI_KEY=your_key_here
   ```

3. **Run Scraper**:
   ```bash
   python main.py -k "Python Developer" -l "Remote" -m 20
   ```

4. **Check Output**:
   - PDF report with company logos
   - CSV export
   - JSON export
   - All in `output/` directory

---

## Support

If you encounter issues:

1. Check this guide first
2. Verify your API key is correct
3. Check API quota limits
4. Try the alternative API provider
5. As a last resort, use `--scraper selenium` for 1-2 jobs

---

**Updated:** 2025-11-16
**Status:** API scraper fully implemented and tested ✅
