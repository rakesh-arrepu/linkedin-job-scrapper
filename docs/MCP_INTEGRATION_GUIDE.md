# Selenium MCP Server Integration Guide

## Overview

This guide explains how to integrate Selenium MCP (Model Context Protocol) server with the LinkedIn Job Scraper project.

## What is MCP?

Model Context Protocol (MCP) is an open standard by Anthropic that enables AI assistants like Claude to interact with external tools, including browser automation via Selenium.

## When to Use MCP vs Direct Selenium

### Use MCP Server When:
- 🤖 You want AI-driven browser automation
- 🔍 Exploring and developing new scraping strategies
- 🧪 Testing and debugging scraping workflows
- 📝 Natural language instructions for browser actions

### Use Direct Selenium (Current Implementation) When:
- 🎯 Production-ready, deterministic scraping
- ⚡ Performance is critical
- 🔒 Full control over execution flow
- 📊 Batch processing of many jobs

## Installation

### Step 1: Install the MCP Server

```bash
# Activate your virtual environment
source venv/bin/activate

# Install Selenium MCP Server
pip install selenium-mcp-server
```

### Step 2: Verify Installation

```bash
python -c "import selenium_mcp_server; print('✅ MCP Server installed successfully!')"
```

## Configuration

### For Claude Desktop

1. **Locate Config File:**
   - macOS: `~/.config/claude-desktop/config.json`
   - Windows: `%APPDATA%\claude-desktop\config.json`
   - Linux: `~/.config/claude-desktop/config.json`

2. **Add Configuration:**

```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["-m", "selenium_mcp_server"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### For Cursor AI

Add to `~/.cursor/mcp_config.json`:

```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["-m", "selenium_mcp_server"]
    }
  }
}
```

## Available MCP Tools

Once configured, you can use these tools through AI instructions:

### Browser Management
- `start_browser` - Launch Chrome or Firefox (headless or windowed)
- `list_browsers` - Show active browser sessions
- `switch_browser` - Switch between multiple sessions
- `close_browser` - Close a specific session

### Navigation
- `navigate` - Go to a URL
- `reload_page` - Refresh current page
- `get_current_url` - Retrieve current URL
- `get_page_title` - Get page title
- `get_page_source` - Get HTML source

### Element Interaction
- `find_element` - Locate elements (CSS, XPath, ID, etc.)
- `click_element` - Click on an element
- `send_keys` - Type text into input fields
- `hover_element` - Hover over elements
- `drag_and_drop` - Drag and drop operations

### Advanced Features
- `execute_script` - Run JavaScript code
- `take_screenshot` - Capture page screenshots
- `upload_file` - Upload files to forms

## Usage Examples

### Example 1: AI-Assisted Scraping Development

Instead of writing code, you can instruct Claude:

```
"Use the Selenium MCP server to:
1. Start a Chrome browser
2. Navigate to linkedin.com/jobs
3. Search for 'Python Developer' jobs
4. Take a screenshot of the results
5. Extract the first 5 job titles"
```

### Example 2: Testing Scraping Strategies

```
"Test if LinkedIn's job search page:
1. Uses infinite scroll or pagination
2. What CSS selectors work for job cards
3. How popups appear and their selectors"
```

### Example 3: Debugging Selectors

```
"Navigate to this LinkedIn job page and tell me:
1. What selector gets the job title
2. What selector gets the company name
3. Take a screenshot of the page"
```

## Hybrid Approach (Recommended)

Keep both implementations:

### 1. **Direct Selenium (Production)**
   - File: `src/scraper/linkedin_scraper.py`
   - Use for: Automated job scraping
   - Pros: Fast, reliable, deterministic

### 2. **MCP Server (Development)**
   - Use for: Testing, exploring, debugging
   - Pros: AI-assisted, flexible, interactive

## Comparison Table

| Feature | Direct Selenium | MCP Server |
|---------|----------------|------------|
| **Speed** | ⚡⚡⚡ Fast | ⚡⚡ Moderate |
| **Control** | 🎯 Full control | 🤖 AI-driven |
| **Flexibility** | 📝 Code-based | 💬 Natural language |
| **Debugging** | 🔍 Manual | 🤖 AI-assisted |
| **Production** | ✅ Ideal | ⚠️ Not recommended |
| **Learning Curve** | 📚 Requires coding | 💬 Conversational |
| **Deterministic** | ✅ Yes | ⚠️ May vary |

## Workflow Example

```
1. Use MCP Server to explore LinkedIn's structure
   → "What selectors work for job listings?"

2. Test scraping strategies via AI
   → "Try scrolling to load more jobs"

3. Validate the approach
   → Screenshots, element checks

4. Implement in Direct Selenium
   → Update linkedin_scraper.py with findings

5. Use MCP for future debugging
   → When LinkedIn changes their layout
```

## Troubleshooting

### Issue: "0 tools enabled"

```bash
# Verify module exists
python -c "import selenium_mcp_server; print('Module found!')"

# Reinstall if needed
pip uninstall selenium-mcp-server
pip install selenium-mcp-server
```

### Issue: ChromeDriver not found

```bash
# The MCP server will use your existing ChromeDriver
# Ensure it's in PATH or installed via:
pip install webdriver-manager
```

### Issue: Config not loading

1. Restart Claude Desktop or Cursor
2. Check config file JSON syntax
3. Verify Python path in config matches your venv

## Benefits for Your Project

1. **Rapid Prototyping**: Test scraping strategies without writing code
2. **AI Debugging**: Let Claude identify issues and suggest fixes
3. **Selector Discovery**: Find working CSS/XPath selectors quickly
4. **Documentation**: Screenshot captures for documentation
5. **Future-Proofing**: Adapt quickly when LinkedIn changes

## Next Steps

1. ✅ Install MCP server: `pip install selenium-mcp-server`
2. ✅ Configure Claude Desktop (if using)
3. ✅ Test with simple navigation: "Open linkedin.com and take a screenshot"
4. ✅ Explore job search page structure
5. ✅ Update existing scraper based on findings

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Selenium MCP Server PyPI](https://pypi.org/project/selenium-mcp-server/)
- [Your Project's Selenium Implementation](../src/scraper/linkedin_scraper.py)

---

**Note**: The MCP server is a tool for AI-assisted development, not a replacement for your production scraper. Use it to enhance your development workflow!
