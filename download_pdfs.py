#!/usr/bin/env -S uv run
"""
This script parses an HTML file downloaded from the UNFCCC documents page
and downloads all PDF links found in the page.
"""

import sys
import requests
from pathlib import Path
from bs4 import BeautifulSoup


def parse_html_file(html_file_path: Path) -> list[tuple[str, str]]:
    """Parse the HTML file and extract PDF URLs."""
    with html_file_path.open("r") as file:
        html_content = file.read()
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    pdf_urls = []
    for select in soup.find_all('select', class_='small-download form-select form-control'):
        options = select.find_all('option')
        for option in options:
            language = option.text  # e.g. "Arabic PDF 0.55 MB", "English PDF 0.55 MB"
            pdf_url = option.get('value')
            pdf_urls.append((language, pdf_url))
    
    return pdf_urls


def download_pdf(pdf_url: str, download_dir: Path):
    file_path = download_dir / Path(pdf_url).name
    if file_path.exists():
        print(f"File already exists, skipping: {file_path}")
        return
    try:
        print(f"Downloading: {pdf_url}")
        response = requests.get(pdf_url)
        response.raise_for_status()
        breakpoint()  # Debugging point since I am currently getting the following response:
        # b'<html>\r\n<head>\r\n<META NAME="robots" CONTENT="noindex,nofollow">\r\n<script src="/_Incapsula_Resource?SWJIYLWA=5074a744e2e3d891814e9a2dace20bd4,719d34d31c8e3a6e6fffd425f7e032f3">\r\n</script>\r\n<body>\r\n</body></html>\r\n'
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                file_path.write_bytes(chunk) if not file_path.exists() else None
        # file_path.write_bytes(response.content)
        print(f"Downloaded: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {pdf_url}: {e}")
    except Exception as e:
        print(f"Unexpected error downloading {pdf_url}: {e}")
        breakpoint()


def main():
    """Main function to run the PDF downloader."""
    if len(sys.argv) < 2:
        print("Usage: python download_pdfs.py <html_file_path> [download_directory]")
        print()
        print("Example:")
        print("  python download_pdfs.py downloaded_page.html")
        print("  python download_pdfs.py downloaded_page.html my_downloads")
        print()
        print("Instructions:")
        print("  1. Go to https://unfccc.int/documents")
        print("  2. Filter documents as needed")
        print("  3. Right-click -> Save As... to download the HTML")
        print("  4. Run this script with the path to the HTML file")
        exit(0)
    
    html_file_path = Path(sys.argv[1])
    download_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "downloads"

    assert html_file_path.exists(), f"HTML file does not exist: {html_file_path}"
    assert html_file_path.suffix in {".html", ".htm"}, f"File is not an HTML file: {html_file_path}"
    download_dir.mkdir(parents=True, exist_ok=True)
    
    pdf = parse_html_file(html_file_path)
    
    if not pdf:
        print("No PDF links found in the HTML file.")
        exit(0)
    
    print(f"Found {len(pdf)} PDF links to download")

    english_pdfs = [url for lang, url in pdf if "English" in lang]
    
    # Download each PDF
    for i, pdf_url in enumerate(english_pdfs, 1):
        print(f"--- Downloading PDF {i}/{len(pdf)} ---")
        download_pdf(pdf_url, download_dir)
        break

if __name__ == "__main__":
    main()