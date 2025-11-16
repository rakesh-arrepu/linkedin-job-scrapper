# SSL Certificate Error Fix

## Problem

If you see this error:
```
ERROR: Failed to start browser: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]
certificate verify failed: unable to get local issuer certificate (_ssl.c:1028)>
```

This happens when Python can't verify SSL certificates, particularly common on macOS.

## Quick Fix (Choose One)

### Option 1: Run the Fix Script (Recommended)

```bash
python fix_ssl_certificates.py
```

This script will:
- Install/update `certifi` package
- Configure SSL environment variables
- Try to run Install Certificates.command (macOS)
- Test SSL connection

### Option 2: Manual Install (macOS)

```bash
# For macOS Python installed from python.org
cd "/Applications/Python 3.13/"  # Adjust version as needed
./Install Certificates.command
```

Or for system Python:
```bash
# Install certificates using pip
pip install --upgrade certifi

# Set environment variables
export SSL_CERT_FILE=$(python -m certifi)
export REQUESTS_CA_BUNDLE=$(python -m certifi)
```

### Option 3: Quick Command Line Fix

```bash
# Install/upgrade certifi
pip install --upgrade certifi

# Set environment variables (add to ~/.zshrc or ~/.bashrc for permanent fix)
export SSL_CERT_FILE=$(python -m certifi)
export REQUESTS_CA_BUNDLE=$(python -m certifi)

# Run the scraper
python main.py -k "Python Developer" -l "Remote" -m 5
```

## Permanent Fix

Add these lines to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# SSL Certificate Fix for Python
export SSL_CERT_FILE=$(python -m certifi)
export REQUESTS_CA_BUNDLE=$(python -m certifi)
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

## Why This Happens

1. **Python 3.6+** removed bundled SSL certificates
2. **macOS** doesn't automatically configure Python's SSL certificates
3. **undetected-chromedriver** needs to download ChromeDriver over HTTPS
4. **Without certificates**, Python can't verify the SSL connection

## Verification

After applying the fix, verify it works:

```bash
# Test SSL connection
python -c "import urllib.request; urllib.request.urlopen('https://www.google.com'); print('SSL works!')"

# Test the scraper
python main.py -k "Python Developer" -m 5
```

## Platform-Specific Instructions

### macOS (Homebrew Python)

```bash
# Install certifi
pip install --upgrade certifi

# Set in current session
export SSL_CERT_FILE=$(python -m certifi)
export REQUESTS_CA_BUNDLE=$(python -m certifi)

# Add to ~/.zshrc for permanent fix
echo 'export SSL_CERT_FILE=$(python -m certifi)' >> ~/.zshrc
echo 'export REQUESTS_CA_BUNDLE=$(python -m certifi)' >> ~/.zshrc
source ~/.zshrc
```

### macOS (python.org Python)

```bash
# Run the installer
cd "/Applications/Python 3.13/"  # Adjust version
open "Install Certificates.command"

# Or from command line
"/Applications/Python 3.13/Install Certificates.command"
```

### Linux

```bash
# Ubuntu/Debian
sudo apt-get install ca-certificates
pip install --upgrade certifi

# Fedora/RHEL
sudo yum install ca-certificates
pip install --upgrade certifi
```

### Windows

```bash
# Usually not needed, but if you get SSL errors:
pip install --upgrade certifi
set SSL_CERT_FILE=%USERPROFILE%\AppData\Local\Programs\Python\Python313\Lib\site-packages\certifi\cacert.pem
```

## Built-in Workaround

The scraper now includes automatic SSL error detection and will:
1. Try to use certifi certificates
2. Show a warning if SSL fails
3. Suggest running `fix_ssl_certificates.py`
4. Temporarily bypass SSL verification (⚠️ not recommended for production)

However, it's **strongly recommended** to properly fix SSL certificates using the methods above.

## Troubleshooting

### Still Getting SSL Errors?

1. **Check certifi is installed:**
   ```bash
   python -c "import certifi; print(certifi.where())"
   ```

2. **Verify environment variables:**
   ```bash
   echo $SSL_CERT_FILE
   echo $REQUESTS_CA_BUNDLE
   ```

3. **Reinstall certifi:**
   ```bash
   pip uninstall certifi
   pip install certifi
   ```

4. **Check Python version:**
   ```bash
   python --version
   which python
   ```

5. **Use absolute path:**
   ```bash
   export SSL_CERT_FILE=/full/path/to/certifi/cacert.pem
   ```

### Corporate Network / Firewall

If you're behind a corporate firewall:

```bash
# Set proxy (if needed)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Add corporate CA certificate
export REQUESTS_CA_BUNDLE=/path/to/corporate/ca-bundle.crt
```

## Security Note

⚠️ **Never disable SSL verification in production!**

The scraper includes an emergency fallback that disables SSL verification if all else fails, but this is:
- Only for development/testing
- Shows a warning when used
- Should be fixed properly using one of the methods above

## Additional Resources

- [Python SSL Documentation](https://docs.python.org/3/library/ssl.html)
- [Certifi Package](https://github.com/certifi/python-certifi)
- [macOS Python SSL](https://bugs.python.org/issue28150)

## Support

If none of these solutions work, please create an issue with:
- Your OS and version
- Python version (`python --version`)
- Output of `python -m certifi`
- Full error message
- Output of `python fix_ssl_certificates.py`

---

**TL;DR: Run `python fix_ssl_certificates.py` or `pip install --upgrade certifi && export SSL_CERT_FILE=$(python -m certifi)`**
