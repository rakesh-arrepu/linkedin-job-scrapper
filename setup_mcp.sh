#!/bin/bash

# Selenium MCP Server Setup Script
# This script installs and configures the Selenium MCP server for the LinkedIn Job Scraper

set -e  # Exit on error

echo "🚀 Setting up Selenium MCP Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please create one first:"
    echo "   python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install selenium-mcp-server
echo "📥 Installing selenium-mcp-server..."
pip install selenium-mcp-server

# Verify installation
echo ""
echo "✅ Verifying installation..."
python -c "import selenium_mcp_server; print('✅ MCP Server installed successfully!')" || {
    echo "❌ Installation verification failed"
    exit 1
}

echo ""
echo "🎉 MCP Server installation complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Configure Claude Desktop (if using):"
echo "   File: ~/.config/claude-desktop/config.json"
echo ""
echo "   Add this configuration:"
echo '   {'
echo '     "mcpServers": {'
echo '       "selenium": {'
echo '         "command": "python",'
echo '         "args": ["-m", "selenium_mcp_server"],'
echo '         "env": {'
echo '           "PYTHONUNBUFFERED": "1"'
echo '         }'
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "2. Restart Claude Desktop or Cursor"
echo ""
echo "3. Test the server by asking Claude to:"
echo '   "Use the Selenium MCP server to open linkedin.com and take a screenshot"'
echo ""
echo "📚 Read the full guide: docs/MCP_INTEGRATION_GUIDE.md"
echo ""
