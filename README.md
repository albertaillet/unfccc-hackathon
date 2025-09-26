# UNFCCC Web Scraping Agent Documentation

## Overview
This project contains a Python script that uses Selenium with Safari WebDriver to scrape the UNFCCC COP-29 event page for anchor elements containing "Access document" text.

## Setup Instructions

### Prerequisites
1. macOS system (required for Safari WebDriver, another webdriver can be used on other OS)
2. Python 3.13+
3. `uv` package manager
4. Safari with "Allow Remote Automation" enabled:
   - Safari → Preferences → Advanced → Show Develop menu in menu bar
   - Develop → Allow Remote Automation

### How to Run

```bash
uv run main.py
```