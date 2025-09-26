from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import sys
from urllib.parse import urljoin, urlparse


def download_pdf_from_url(url, download_dir="downloads"):
    """
    Navigate to a URL, select English from dropdown, and download the PDF.
    
    Args:
        url (str): URL to navigate to
        download_dir (str): Directory to save downloaded PDFs
    """
    print(f"Processing URL: {url}")
    
    # Create download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)
    
    # Set up Safari options for headless browsing
    safari_options = Options()
    safari_options.add_argument("--headless")
    
    # Initialize the Safari driver
    driver = webdriver.Safari(options=safari_options)
    
    try:
        # Navigate to the URL
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Give the page a moment to fully load dynamic content
        time.sleep(3)
        
        # Look for the download dropdown with class=chosen-single
        print("Looking for download dropdown with class='chosen-single'...")
        try:
            download_dropdown = driver.find_element(
                By.XPATH, 
                "//a[contains(text(), 'Download') and contains(@class, 'chosen-single')]"
            )
            
            print("Found download dropdown, clicking it...")
            download_dropdown.click()
            
            # Wait a moment for dropdown to appear
            time.sleep(2)
            
            # Look for and click "English" option
            print("Looking for 'English' option in dropdown...")
            english_option = driver.find_element(
                By.XPATH,
                "//li[contains(text(), 'English')]"
            )
            
            print("Clicking 'English' option...")
            english_option.click()
            
            # Wait for the selection to take effect
            time.sleep(2)
            
            print("Successfully selected English from dropdown!")
            
            # Now look for the actual download link/button
            print("Looking for PDF download link...")
            
            # Try to find download links - could be various patterns
            download_selectors = [
                "//a[contains(@href, '.pdf')]",
                "//a[contains(text(), 'Download') and contains(@href, '.pdf')]",
                "//a[contains(text(), 'PDF')]",
                "//a[contains(@class, 'download')]",
                "//button[contains(text(), 'Download')]"
            ]
            
            pdf_url = None
            for selector in download_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        href = element.get_attribute('href')
                        if href and '.pdf' in href.lower():
                            pdf_url = href
                            break
                    if pdf_url:
                        break
                except:
                    continue
            
            if pdf_url:
                # Make sure it's an absolute URL
                if not pdf_url.startswith('http'):
                    pdf_url = urljoin(url, pdf_url)
                
                print(f"Found PDF URL: {pdf_url}")
                
                # Download the PDF using requests
                print("Downloading PDF...")
                response = requests.get(pdf_url, stream=True)
                response.raise_for_status()
                
                # Extract filename from URL or create one
                parsed_url = urlparse(pdf_url)
                filename = os.path.basename(parsed_url.path)
                if not filename or not filename.endswith('.pdf'):
                    filename = f"document_{int(time.time())}.pdf"
                
                filepath = os.path.join(download_dir, filename)
                
                # Save the PDF
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"Successfully downloaded PDF to: {filepath}")
                return filepath
            else:
                print("No PDF download link found on the page")
                return None
                
        except Exception as e:
            print(f"Error processing download dropdown: {e}")
            return None
    
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return None
    
    finally:
        # Close the browser
        driver.quit()


def process_links_file(filename, download_dir="downloads"):
    """
    Process all URLs from a file and download PDFs.
    
    Args:
        filename (str): File containing URLs, one per line
        download_dir (str): Directory to save downloaded PDFs
    """
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        return
    
    # Read URLs from file
    with open(filename, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(urls)} URLs to process")
    
    downloaded_files = []
    for i, url in enumerate(urls, 1):
        print(f"\n--- Processing URL {i}/{len(urls)} ---")
        filepath = download_pdf_from_url(url, download_dir)
        if filepath:
            downloaded_files.append(filepath)
    
    print(f"\nDownload complete! Downloaded {len(downloaded_files)} PDFs:")
    for filepath in downloaded_files:
        print(f"  - {filepath}")


def main():
    """Main function to run the PDF downloader."""
    if len(sys.argv) < 2:
        print("Usage: python pdf_downloader.py <links_file> [download_directory]")
        print("Example: python pdf_downloader.py access_document_links.txt downloads")
        sys.exit(1)
    
    links_file = sys.argv[1]
    download_dir = sys.argv[2] if len(sys.argv) > 2 else "downloads"
    
    process_links_file(links_file, download_dir)


if __name__ == "__main__":
    main()