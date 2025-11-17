# LinkedIn Job Scraper - Documentation

Welcome to the documentation for the LinkedIn Job Scraper project!

## 📚 Documentation Index

### Getting Started
- **[Main README](../README.md)** - Project overview and quick start guide

### MCP Integration (New!)
- **[MCP Integration Guide](./MCP_INTEGRATION_GUIDE.md)** - Complete guide to setting up Selenium MCP server
- **[MCP Example Commands](./MCP_EXAMPLE_COMMANDS.md)** - 20+ example commands for AI-assisted scraping

### Configuration Files
- **[Claude Desktop Config Example](../claude_desktop_config.example.json)** - MCP configuration template
- **[MCP Requirements](../requirements-mcp.txt)** - Optional MCP dependencies

## 🎯 Quick Links

### Installation

**Standard Installation (Production):**
```bash
pip install -r requirements.txt
```

**With MCP Server (Development/Testing):**
```bash
pip install -r requirements-mcp.txt
# or
./setup_mcp.sh
```

### Usage Modes

| Mode | File | Purpose | Command |
|------|------|---------|---------|
| **CLI Tool** | `main.py` | Production scraping | `python main.py -k "Python Developer"` |
| **Direct Selenium** | `src/scraper/linkedin_scraper.py` | Programmatic scraping | Import and use in code |
| **MCP Server** | Via Claude/AI | Interactive development | Natural language commands |

## 🔧 Architecture Overview

```
linkedin-job-scrapper/
├── src/
│   ├── scraper/
│   │   ├── linkedin_scraper.py      # Direct Selenium scraper (Production)
│   │   ├── linkedin_api_scraper.py  # API-based scraper
│   │   └── browser_manager.py       # Browser automation utilities
│   ├── models/
│   │   └── job.py                   # Job and SearchParameters models
│   ├── exporters/
│   │   ├── pdf_exporter.py          # Stunning PDF reports
│   │   ├── csv_exporter.py          # CSV exports
│   │   └── json_exporter.py         # JSON exports
│   └── utils/
│       ├── logger.py                # Logging configuration
│       └── rate_limiter.py          # Rate limiting
├── config/
│   └── settings.py                  # Application settings
├── main.py                          # CLI interface
└── docs/                            # Documentation (you are here!)
```

## 🚀 Workflow Examples

### 1. Production Scraping
```bash
# Use the CLI for production job scraping
python main.py -k "Data Scientist" -l "New York" -m 100 -f pdf
```

### 2. AI-Assisted Development
```
# Use MCP server through Claude
"Use the Selenium MCP server to explore LinkedIn's job page structure
and tell me what selectors work for extracting job titles"
```

### 3. Hybrid Approach (Recommended)
```
1. Use MCP to explore and test → Find working selectors
2. Update linkedin_scraper.py → Implement in production code
3. Use MCP for debugging → When LinkedIn changes layout
```

## 🤖 MCP Server Features

The Selenium MCP server enables AI-driven browser automation:

### Key Capabilities
- ✅ **Natural Language Control**: "Navigate to LinkedIn and search for jobs"
- ✅ **Interactive Debugging**: "What selector gets the job title?"
- ✅ **Screenshot Capture**: Visual documentation and verification
- ✅ **Element Discovery**: Find CSS/XPath selectors automatically
- ✅ **Multi-Browser**: Chrome and Firefox support
- ✅ **Headless/Windowed**: Choose display mode

### When to Use
- 🔍 **Exploration**: Understanding new page structures
- 🧪 **Testing**: Validating scraping strategies
- 🐛 **Debugging**: Finding why selectors broke
- 📝 **Documentation**: Generating screenshots
- 🎓 **Learning**: Understanding web scraping

### When NOT to Use
- ⚡ **Production**: Use direct Selenium for speed
- 📊 **Batch Processing**: Use linkedin_scraper.py
- 🎯 **Critical Workflows**: Direct code is more reliable

## 📖 Detailed Guides

### Setup Guides
1. **[MCP Integration Guide](./MCP_INTEGRATION_GUIDE.md)**
   - Installation instructions
   - Configuration for Claude Desktop/Cursor
   - Available tools and features
   - Troubleshooting

### Example Commands
2. **[MCP Example Commands](./MCP_EXAMPLE_COMMANDS.md)**
   - 20+ ready-to-use commands
   - LinkedIn-specific examples
   - Debugging scenarios
   - Testing strategies

## 🔄 Comparison: MCP vs Direct Selenium

| Aspect | MCP Server | Direct Selenium |
|--------|-----------|----------------|
| **Interface** | Natural language | Python code |
| **Speed** | Moderate (AI overhead) | Fast |
| **Flexibility** | Very high | Medium |
| **Reliability** | Variable (AI-dependent) | Very high |
| **Learning Curve** | Low (conversational) | Medium (coding required) |
| **Best For** | Exploration, testing | Production, automation |
| **Code Control** | AI-driven | Full manual control |
| **Documentation** | Auto-generates insights | Manual |

## 🛠️ Configuration

### Environment Variables
Create a `.env` file (see `.env.example`):
```env
# Scraper settings
HEADLESS_MODE=true
MAX_JOBS=50

# Output settings
OUTPUT_DIR=./output
DEFAULT_OUTPUT_FORMAT=pdf

# Rate limiting
MIN_DELAY=2
MAX_DELAY=5

# Scraper method
SCRAPER_METHOD=api  # or 'selenium'
```

### MCP Server Config
Location: `~/.config/claude-desktop/config.json`

See [claude_desktop_config.example.json](../claude_desktop_config.example.json) for template.

## 📊 Output Formats

The scraper supports multiple export formats:

### PDF Reports (Recommended)
- 📈 Beautiful charts and analytics
- 🏢 Company logos (auto-fetched)
- 🎨 Vibrant, professional design
- 📊 Statistics and insights

### CSV Export
- 📑 Spreadsheet-compatible
- 📊 Data analysis ready
- 🔄 Easy to import/export

### JSON Export
- 🔌 API-friendly
- 🔄 Easy to parse
- 📝 Full data preservation

## 🔍 Troubleshooting

### Common Issues

**"No module named 'selenium'"**
```bash
# Activate virtual environment first
source venv/bin/activate
pip install -r requirements.txt
```

**"ChromeDriver not found"**
```bash
# Install ChromeDriver or it will be auto-downloaded
# by undetected-chromedriver
```

**"MCP Server shows 0 tools"**
```bash
# Verify installation
python -c "import selenium_mcp_server; print('OK')"

# Restart Claude Desktop after config changes
```

**"SSL Certificate Error"**
```bash
# Run the SSL fix script
python fix_ssl_certificates.py
```

## 📚 Additional Resources

### External Documentation
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [ReportLab (PDF) Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)

### Project-Specific
- [Setup Script](../setup_mcp.sh) - Automated MCP installation
- [Requirements](../requirements.txt) - Python dependencies
- [Main CLI](../main.py) - CLI interface code

## 🤝 Contributing

When contributing, please:
1. Test with both Selenium modes (direct and MCP)
2. Update documentation as needed
3. Add example commands for new features
4. Maintain backward compatibility

## 📝 Notes

- **MCP Server is Optional**: The core scraper works without it
- **Hybrid Approach**: Use both MCP and direct code for best results
- **Production Ready**: The main scraper is production-ready
- **AI-Enhanced**: MCP adds AI capabilities for development

## 🎯 Next Steps

1. **New Users**: Start with [MCP Integration Guide](./MCP_INTEGRATION_GUIDE.md)
2. **Developers**: Check [MCP Example Commands](./MCP_EXAMPLE_COMMANDS.md)
3. **Production**: Use `main.py` CLI directly

---

**Need Help?**
- Check the troubleshooting sections in each guide
- Review example commands
- Test with simple MCP commands first
