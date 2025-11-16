# Docker Usage Guide

This guide explains how to use LinkedIn Job Scraper with Docker.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)

## Quick Start

### Build the Docker Image

```bash
docker build -t linkedin-scraper .
```

### Run with Docker

```bash
# Basic usage
docker run --rm -v $(pwd)/output:/app/output linkedin-scraper \
  -k "Python Developer" -l "Remote" -m 50

# With all exports
docker run --rm -v $(pwd)/output:/app/output linkedin-scraper \
  -k "Data Scientist" -l "New York" -m 100 -f all

# Interactive mode (non-headless)
docker run --rm -v $(pwd)/output:/app/output \
  -e HEADLESS_MODE=false \
  linkedin-scraper \
  -k "DevOps Engineer" --no-headless
```

### Using Docker Compose

1. **Edit docker-compose.yml** to set your search parameters:

```yaml
command: ["-k", "Software Engineer", "-l", "San Francisco", "-m", "100"]
```

2. **Run the scraper**:

```bash
docker-compose up
```

3. **Check outputs** in `./output` directory

## Volume Mapping

The Docker container maps the following directories:

- `./output:/app/output` - Output files (PDF, CSV, JSON)
- `./.env:/app/.env` - Environment configuration (optional)

## Environment Variables

Pass environment variables using `-e` flag:

```bash
docker run --rm \
  -e HEADLESS_MODE=true \
  -e MAX_JOBS=100 \
  -e LOG_LEVEL=DEBUG \
  -v $(pwd)/output:/app/output \
  linkedin-scraper \
  -k "Python Developer"
```

## Examples

### Search for Remote Jobs

```bash
docker run --rm -v $(pwd)/output:/app/output linkedin-scraper \
  -k "Full Stack Developer" --remote-only -m 75
```

### Search with Filters

```bash
docker run --rm -v $(pwd)/output:/app/output linkedin-scraper \
  -k "Machine Learning Engineer" \
  -d week \
  -e 4 \
  -t F \
  -m 100
```

### Export Only CSV

```bash
docker run --rm -v $(pwd)/output:/app/output linkedin-scraper \
  -k "Product Manager" -l "Austin" -f csv -m 50
```

## Docker Compose Examples

### Example 1: Daily Job Scraping

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  scraper:
    build: .
    volumes:
      - ./output:/app/output
    environment:
      - HEADLESS_MODE=true
    command: [
      "-k", "Software Engineer",
      "-l", "Remote",
      "-d", "24h",
      "-m", "50",
      "-f", "all"
    ]
```

Run: `docker-compose up`

### Example 2: Multiple Searches

Create separate compose files for different searches:

**docker-compose.python.yml**:
```yaml
version: '3.8'
services:
  python-jobs:
    build: .
    volumes:
      - ./output/python:/app/output
    command: ["-k", "Python Developer", "-m", "100"]
```

**docker-compose.data.yml**:
```yaml
version: '3.8'
services:
  data-jobs:
    build: .
    volumes:
      - ./output/data:/app/output
    command: ["-k", "Data Scientist", "-m", "100"]
```

Run:
```bash
docker-compose -f docker-compose.python.yml up
docker-compose -f docker-compose.data.yml up
```

## Troubleshooting

### Permission Issues

If you get permission errors with output files:

```bash
# On Linux/Mac
sudo chown -R $USER:$USER output/

# Or run container with your user ID
docker run --rm --user $(id -u):$(id -g) \
  -v $(pwd)/output:/app/output \
  linkedin-scraper -k "Developer"
```

### Chrome/ChromeDriver Issues

The Docker image includes Chrome. If you encounter issues:

1. Rebuild the image:
```bash
docker build --no-cache -t linkedin-scraper .
```

2. Check Chrome version inside container:
```bash
docker run --rm linkedin-scraper /bin/bash -c "google-chrome --version"
```

### Out of Memory

If scraping large numbers of jobs:

```bash
docker run --rm -m 2g -v $(pwd)/output:/app/output \
  linkedin-scraper -k "Engineer" -m 500
```

## Advanced: Scheduled Scraping with Cron

### Using Docker + Cron on Linux

1. Create a script `scrape_jobs.sh`:

```bash
#!/bin/bash
docker run --rm -v /path/to/output:/app/output linkedin-scraper \
  -k "Python Developer" -l "Remote" -m 50
```

2. Make it executable:
```bash
chmod +x scrape_jobs.sh
```

3. Add to crontab:
```bash
crontab -e

# Add line to run daily at 9 AM
0 9 * * * /path/to/scrape_jobs.sh
```

## Cleanup

Remove containers and images:

```bash
# Remove containers
docker-compose down

# Remove image
docker rmi linkedin-scraper

# Remove all stopped containers and unused images
docker system prune -a
```

## Tips

1. **Use volume mounts** to persist output files
2. **Set resource limits** for large scrapes
3. **Use docker-compose** for repeated searches
4. **Schedule with cron** for automated scraping
5. **Check logs** with `docker logs <container_id>`
