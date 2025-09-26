# UNFCCC PDF Downloader

## Overview
This project contains Python scripts that scrape the UNFCCC for pdf links and automatically download English PDFs from each document page.

## Project Structure
```
unfccc-hackathon/
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Setup Instructions

### Prerequisites
1. Web Browser
2. Python 3.13+
3. `uv` package manager

## Usage

1. Go to the page [https://unfccc.int/documents](https://unfccc.int/documents) and filter the documents as needed.
2. Download the HTML of the page (Right-click -> Save As...).
3. Copy the path of the downloaded HTML file.
4. Run the script with the path to the HTML file as an argument:
```bash
./download_pdfs.py path/to/downloaded_page.html
```