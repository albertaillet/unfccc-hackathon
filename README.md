# UNFCCC PDF Downloader

## Overview
This project contains Python scripts that use Selenium with Safari WebDriver to scrape the UNFCCC COP-29 event page for "Access document" links and automatically download English PDFs from each document page.

## Project Structure
```
unfccc-hackathon/
├── link_collector.py      # Collects Access document links
├── pdf_downloader.py      # Downloads PDFs from collected links
├── download_pdfs.sh       # Bash script for automated workflow
├── pyproject.toml         # Project dependencies
├── README.md              # This file
└── Agent.md               # Detailed documentation
```

## Setup Instructions

### Prerequisites
1. macOS system (required for Safari WebDriver)
2. Python 3.13+
3. `uv` package manager
4. Safari with "Allow Remote Automation" enabled:
   - Safari → Preferences → Advanced → Show Develop menu in menu bar
   - Develop → Allow Remote Automation

### Installation
```bash
# Install dependencies
uv sync
```

## Usage

### Automated Workflow (Recommended)
```bash
# Run the complete workflow
./download_pdfs.sh

# Or with custom parameters
./download_pdfs.sh my_links.txt my_downloads
```

### Manual Usage

#### 1. Collect Links Only
```bash
# Collect Access document links
uv run python link_collector.py

# With custom output file
uv run python link_collector.py my_links.txt
```

#### 2. Download PDFs Only
```bash
# Download PDFs from links file
uv run python pdf_downloader.py access_document_links.txt

# With custom download directory
uv run python pdf_downloader.py access_document_links.txt downloads
```

## How It Works

1. **Link Collection**: `link_collector.py` navigates to the UNFCCC COP-29 page and finds all anchor elements containing "Access document"
2. **PDF Download**: `pdf_downloader.py` processes each link by:
   - Navigating to the document page
   - Finding the download dropdown with class "chosen-single"
   - Selecting "English" option
   - Extracting the PDF URL and downloading it using `requests`

## Output Files

- **Links file**: Contains URLs of Access document pages (one per line)
- **Downloaded PDFs**: Saved to `downloads/` directory by default
- **Similar links**: If no exact matches found, saves similar links to `similar_links.txt`

## Features

- **Headless browsing**: Runs Safari in background without visible window
- **Automatic PDF detection**: Multiple strategies to find PDF download links
- **Error handling**: Comprehensive error handling and cleanup
- **Modular design**: Separate scripts for collection and downloading
- **Flexible configuration**: Custom filenames and directories supported