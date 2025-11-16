"""Setup script for LinkedIn Job Scraper."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='linkedin-job-scraper',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A powerful tool to scrape LinkedIn job postings and generate detailed reports',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/linkedin-job-scrapper',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires='>=3.8',
    install_requires=[
        'setuptools>=68.0.0',  # Required for Python 3.12+
        'selenium>=4.15.0',
        'undetected-chromedriver>=3.5.5',
        'beautifulsoup4>=4.12.0',
        'lxml>=5.0.0',
        'pandas>=2.1.0',
        'pydantic>=2.5.0',
        'pydantic-settings>=2.1.0',
        'reportlab>=4.0.0',
        'matplotlib>=3.8.0',
        'Pillow>=10.1.0',
        'click>=8.1.7',
        'rich>=13.7.0',
        'tqdm>=4.66.0',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'fake-useragent>=1.4.0',
        'tenacity>=8.2.0',
        'python-dateutil>=2.8.2',
    ],
    entry_points={
        'console_scripts': [
            'linkedin-scraper=main:main',
        ],
    },
    include_package_data=True,
    keywords='linkedin jobs scraper selenium automation pdf csv json',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/linkedin-job-scrapper/issues',
        'Source': 'https://github.com/yourusername/linkedin-job-scrapper',
    },
)
