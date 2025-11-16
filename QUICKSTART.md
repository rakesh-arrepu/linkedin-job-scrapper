# Quick Start Guide

Get started with LinkedIn Job Scraper in 5 minutes!

## 1️⃣ Install (2 minutes)

```bash
# Clone
git clone https://github.com/yourusername/linkedin-job-scrapper.git
cd linkedin-job-scrapper

# Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Got an error?

**`ModuleNotFoundError: No module named 'distutils'`** (Python 3.13+)
```bash
pip install setuptools>=68.0.0
pip install -r requirements.txt
```

**Other errors?** See [INSTALL.md](INSTALL.md)

## 2️⃣ Verify (30 seconds)

```bash
python test_setup.py
```

Expected: `🎉 ALL TESTS PASSED!`

## 3️⃣ Test Run (2 minutes)

```bash
python main.py -k "Python Developer" -l "Remote" -m 5
```

This will:
- Search for 5 Python Developer jobs
- Filter for remote positions
- Generate PDF, CSV, and JSON reports in `./output/`

## 4️⃣ Check Results

```bash
ls -la output/
```

You should see:
- `*.pdf` - Beautiful report with charts
- `*.csv` - Spreadsheet data
- `*.json` - Raw JSON data

## Common Commands

```bash
# Remote jobs, posted this week
python main.py -k "Data Scientist" -d week --remote-only -m 50

# Specific location
python main.py -k "Software Engineer" -l "San Francisco" -m 100

# With experience level (4 = Mid-Senior)
python main.py -k "DevOps" -e 4 -t F -m 75

# Full-time only
python main.py -k "Product Manager" -t F -m 50

# Multiple formats
python main.py -k "Designer" -f pdf -m 30
```

## Need More Details?

Run with `--help`:
```bash
python main.py --help
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `distutils` error | `pip install setuptools>=68.0.0` |
| No Chrome | Install from https://www.google.com/chrome/ |
| Import errors | `pip install -r requirements.txt --force-reinstall` |
| No jobs found | Try broader keywords or different location |

## Next Steps

- 📖 Read full [README.md](README.md)
- 🔧 See detailed [INSTALL.md](INSTALL.md)
- 💻 Check [API.md](docs/API.md) for programmatic usage
- 🐳 Try [Docker](docs/DOCKER.md) for containerized usage

---

**Happy job hunting! 🚀**
