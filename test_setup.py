#!/usr/bin/env python3
"""
Test script to verify all imports and basic functionality.
Run this to ensure the project is set up correctly.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports."""
    print("=" * 60)
    print("Testing LinkedIn Job Scraper - Import Verification")
    print("=" * 60)
    print(f"\nPython version: {sys.version}")
    print(f"Python executable: {sys.executable}\n")

    tests_passed = 0
    tests_failed = 0

    # Test core dependencies
    print("Testing core dependencies...")

    try:
        import selenium
        try:
            version = selenium.__version__
        except AttributeError:
            from importlib.metadata import version as get_version
            try:
                version = get_version('selenium')
            except:
                version = "installed"
        print(f"✅ selenium ({version})")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ selenium - {e}")
        tests_failed += 1

    try:
        import undetected_chromedriver as uc
        print(f"✅ undetected_chromedriver")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ undetected_chromedriver - {e}")
        tests_failed += 1

    try:
        from bs4 import BeautifulSoup
        print(f"✅ beautifulsoup4")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ beautifulsoup4 - {e}")
        tests_failed += 1

    try:
        import lxml
        try:
            from lxml import etree
            version = etree.LXML_VERSION
            version_str = ".".join(map(str, version))
        except:
            from importlib.metadata import version as get_version
            try:
                version_str = get_version('lxml')
            except:
                version_str = "installed"
        print(f"✅ lxml ({version_str})")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ lxml - {e}")
        tests_failed += 1

    # Test data handling
    print("\nTesting data handling libraries...")

    try:
        import pandas
        try:
            version = pandas.__version__
        except AttributeError:
            from importlib.metadata import version as get_version
            try:
                version = get_version('pandas')
            except:
                version = "installed"
        print(f"✅ pandas ({version})")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ pandas - {e}")
        tests_failed += 1

    try:
        import pydantic
        try:
            version = pydantic.__version__
        except AttributeError:
            from importlib.metadata import version as get_version
            try:
                version = get_version('pydantic')
            except:
                version = "installed"
        print(f"✅ pydantic ({version})")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ pydantic - {e}")
        tests_failed += 1

    # Test PDF generation
    print("\nTesting PDF generation libraries...")

    try:
        import reportlab
        try:
            version = reportlab.Version
        except AttributeError:
            from importlib.metadata import version as get_version
            try:
                version = get_version('reportlab')
            except:
                version = "installed"
        print(f"✅ reportlab ({version})")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ reportlab - {e}")
        tests_failed += 1

    try:
        import matplotlib
        try:
            version = matplotlib.__version__
        except AttributeError:
            from importlib.metadata import version as get_version
            try:
                version = get_version('matplotlib')
            except:
                version = "installed"
        print(f"✅ matplotlib ({version})")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ matplotlib - {e}")
        tests_failed += 1

    # Test CLI libraries
    print("\nTesting CLI libraries...")

    try:
        import click
        try:
            version = click.__version__
        except AttributeError:
            from importlib.metadata import version as get_version
            try:
                version = get_version('click')
            except:
                version = "installed"
        print(f"✅ click ({version})")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ click - {e}")
        tests_failed += 1

    try:
        import rich
        try:
            version = rich.__version__
        except AttributeError:
            # rich doesn't expose __version__ directly
            from importlib.metadata import version as get_version
            try:
                version = get_version('rich')
            except:
                version = "installed"
        print(f"✅ rich ({version})")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ rich - {e}")
        tests_failed += 1

    # Test project modules
    print("\nTesting project modules...")

    try:
        from config.settings import settings
        print(f"✅ config.settings")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ config.settings - {e}")
        tests_failed += 1

    try:
        from src.models.job import Job, SearchParameters
        print(f"✅ src.models.job")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ src.models.job - {e}")
        tests_failed += 1

    try:
        from src.scraper.browser_manager import BrowserManager
        print(f"✅ src.scraper.browser_manager")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ src.scraper.browser_manager - {e}")
        tests_failed += 1

    try:
        from src.scraper.linkedin_scraper import LinkedInScraper
        print(f"✅ src.scraper.linkedin_scraper")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ src.scraper.linkedin_scraper - {e}")
        tests_failed += 1

    try:
        from src.exporters.pdf_exporter import PDFExporter
        print(f"✅ src.exporters.pdf_exporter")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ src.exporters.pdf_exporter - {e}")
        tests_failed += 1

    try:
        from src.exporters.csv_exporter import CSVExporter
        print(f"✅ src.exporters.csv_exporter")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ src.exporters.csv_exporter - {e}")
        tests_failed += 1

    try:
        from src.exporters.json_exporter import JSONExporter
        print(f"✅ src.exporters.json_exporter")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ src.exporters.json_exporter - {e}")
        tests_failed += 1

    # Print summary
    print("\n" + "=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print("=" * 60)

    if tests_failed == 0:
        print("\n🎉 All imports successful! The project is ready to use.")
        print("\nTry running:")
        print("  python main.py --help")
        return True
    else:
        print("\n❌ Some imports failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        return False


def test_basic_functionality():
    """Test basic functionality without actually scraping."""
    print("\n" + "=" * 60)
    print("Testing Basic Functionality")
    print("=" * 60)

    try:
        from src.models.job import Job, SearchParameters
        from datetime import datetime

        # Test Job model
        print("\n1. Testing Job model...")
        job = Job(
            title="Senior Python Developer",
            company="Test Company",
            location="Remote",
            job_url="https://linkedin.com/jobs/view/123456",
            skills=["Python", "Django", "AWS"]
        )
        print(f"✅ Job model created: {job.title} at {job.company}")

        # Test SearchParameters
        print("\n2. Testing SearchParameters model...")
        search_params = SearchParameters(
            keywords="Python Developer",
            location="Remote",
            max_jobs=10
        )
        url = search_params.build_url()
        print(f"✅ Search URL built: {url[:80]}...")

        # Test SearchParameters.from_cli_args
        print("\n3. Testing SearchParameters.from_cli_args...")
        search_params = SearchParameters.from_cli_args(
            keywords="Data Scientist",
            location="New York",
            date_posted="week",
            max_jobs=50
        )
        print(f"✅ CLI args parsed: keywords='{search_params.keywords}'")

        # Test Job.to_dict
        print("\n4. Testing Job.to_dict...")
        job_dict = job.to_dict()
        print(f"✅ Job converted to dict with {len(job_dict)} fields")

        print("\n✅ All basic functionality tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_exporters():
    """Test exporters with sample data."""
    print("\n" + "=" * 60)
    print("Testing Exporters")
    print("=" * 60)

    try:
        from src.models.job import Job
        from src.exporters.csv_exporter import CSVExporter
        from src.exporters.json_exporter import JSONExporter
        from pathlib import Path
        import tempfile

        # Create sample jobs
        print("\n1. Creating sample job data...")
        jobs = [
            Job(
                title=f"Software Engineer {i}",
                company=f"Company {i}",
                location="Remote",
                job_url=f"https://linkedin.com/jobs/view/{i}",
                skills=["Python", "JavaScript"]
            )
            for i in range(1, 4)
        ]
        print(f"✅ Created {len(jobs)} sample jobs")

        # Test CSV export
        print("\n2. Testing CSV export...")
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "test_jobs.csv"
            result = CSVExporter.export(jobs, csv_path)
            if result and csv_path.exists():
                print(f"✅ CSV export successful: {csv_path.stat().st_size} bytes")
            else:
                print("❌ CSV export failed")
                return False

        # Test JSON export
        print("\n3. Testing JSON export...")
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = Path(tmpdir) / "test_jobs.json"
            result = JSONExporter.export(jobs, json_path)
            if result and json_path.exists():
                print(f"✅ JSON export successful: {json_path.stat().st_size} bytes")
            else:
                print("❌ JSON export failed")
                return False

        print("\n✅ All exporter tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Exporter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🔍 LinkedIn Job Scraper - System Check\n")

    # Run tests
    imports_ok = test_imports()

    if imports_ok:
        functionality_ok = test_basic_functionality()
        exporters_ok = test_exporters()

        if functionality_ok and exporters_ok:
            print("\n" + "=" * 60)
            print("🎉 ALL TESTS PASSED!")
            print("=" * 60)
            print("\nThe project is ready to use. Try:")
            print("  python main.py -k \"Python Developer\" -l \"Remote\" -m 5")
            print("\nNote: Actual scraping requires Chrome browser installed.")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed.")
            sys.exit(1)
    else:
        print("\n❌ Import tests failed. Please fix dependencies first.")
        sys.exit(1)
