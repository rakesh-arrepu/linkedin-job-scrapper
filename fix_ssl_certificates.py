#!/usr/bin/env python3
"""
Fix SSL certificate issues for macOS Python installations.
Run this if you get SSL certificate verification errors.
"""

import os
import sys
import ssl
import certifi

def fix_ssl_certificates():
    """Install SSL certificates for Python on macOS."""
    print("🔧 Fixing SSL Certificates for Python\n")

    # Check if we're on macOS
    if sys.platform != 'darwin':
        print("ℹ️  This script is primarily for macOS systems.")
        print("If you're on Linux/Windows and getting SSL errors, try:")
        print("  pip install --upgrade certifi")
        return

    print("Detected macOS system")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}\n")

    # Method 1: Use certifi
    print("Method 1: Using certifi certificates...")
    try:
        import certifi
        print(f"✅ certifi is installed")
        print(f"   Certificate bundle: {certifi.where()}")

        # Set SSL_CERT_FILE environment variable
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
        print(f"✅ Set SSL_CERT_FILE={certifi.where()}")

    except ImportError:
        print("❌ certifi not found. Installing...")
        os.system(f"{sys.executable} -m pip install --upgrade certifi")
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
        print(f"✅ Installed and configured certifi")

    # Method 2: Check for Install Certificates command
    print("\nMethod 2: Checking for Install Certificates.command...")

    # Find Python framework path
    python_path = sys.executable
    python_dir = os.path.dirname(os.path.dirname(python_path))

    cert_command_paths = [
        os.path.join(python_dir, "Install Certificates.command"),
        f"/Applications/Python {sys.version_info.major}.{sys.version_info.minor}/Install Certificates.command",
        os.path.join(os.path.dirname(python_path), "Install Certificates.command"),
    ]

    cert_command = None
    for path in cert_command_paths:
        if os.path.exists(path):
            cert_command = path
            break

    if cert_command:
        print(f"✅ Found: {cert_command}")
        print(f"\n📋 You can also run this command manually:")
        print(f"   {cert_command}")

        # Ask user if they want to run it
        response = input("\nRun Install Certificates.command now? (y/n): ")
        if response.lower() == 'y':
            print("Running Install Certificates.command...")
            os.system(f'"{cert_command}"')
            print("✅ Done!")
    else:
        print("ℹ️  Install Certificates.command not found")
        print("   This is normal for some Python installations")

    # Method 3: Create .env with SSL settings
    print("\nMethod 3: Creating SSL configuration...")

    env_file = ".env"
    ssl_settings = f"""
# SSL Certificate Settings (added by fix_ssl_certificates.py)
SSL_CERT_FILE={certifi.where()}
REQUESTS_CA_BUNDLE={certifi.where()}
CURL_CA_BUNDLE={certifi.where()}
"""

    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()

        if 'SSL_CERT_FILE' not in content:
            with open(env_file, 'a') as f:
                f.write(ssl_settings)
            print(f"✅ Added SSL settings to {env_file}")
        else:
            print(f"ℹ️  SSL settings already in {env_file}")
    else:
        # Copy from .env.example
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
                f.write(ssl_settings)
            print(f"✅ Created {env_file} with SSL settings")
        else:
            with open(env_file, 'w') as f:
                f.write(ssl_settings)
            print(f"✅ Created {env_file} with SSL settings")

    # Test SSL connection
    print("\nTesting SSL connection...")
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        print("✅ SSL connection test: SUCCESS")
    except Exception as e:
        print(f"⚠️  SSL connection test failed: {e}")
        print("\nAdditional steps to try:")
        print("1. Restart your terminal")
        print("2. Run: pip install --upgrade certifi")
        print("3. Run the scraper again")

    print("\n" + "="*60)
    print("✅ SSL Certificate Fix Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Restart your terminal (or source your shell profile)")
    print("2. Reactivate your virtual environment")
    print("3. Run the scraper again:")
    print("   python main.py -k 'Python Developer' -l 'Remote' -m 5")
    print("\nIf you still get SSL errors, try:")
    print("  export SSL_CERT_FILE=$(python -m certifi)")
    print("  export REQUESTS_CA_BUNDLE=$(python -m certifi)")

if __name__ == "__main__":
    try:
        fix_ssl_certificates()
    except KeyboardInterrupt:
        print("\n\n⚠️ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
