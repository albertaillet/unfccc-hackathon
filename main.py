import os
import time
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = os.getenv("URL", "https://unfccc.int/event/cop-29")
DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "./downloads"))

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("Starting headless browser session to UNFCCC COP-29 event page...")
    
    # Set up Safari options for headless browsing
    safari_options = Options()
    safari_options.add_argument("--headless")
    
    # Initialize the Safari driver
    driver = webdriver.Safari(options=safari_options)
    
    try:
        # Navigate to the UNFCCC COP-29 event page
        print(f"Navigating to: {URL}")
        driver.get(URL)
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Give the page a moment to fully load dynamic content
        time.sleep(3)
        
        print("Searching for anchor elements containing 'Access document'...")
        
        # Find all anchor elements that contain the text "Access document"
        access_document_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Access document')]")
        
        print(f"Found {len(access_document_links)} anchor elements containing 'Access document':")
        
        if len(access_document_links) == 0:
            print("No Access document links found to process.")
            return

        for link in access_document_links:
            print(f"- {link.text.strip()}: {link.get_attribute('href')}")
            text = link.text.strip()
            href = link.get_attribute('href')
            print(f"1. Text: '{text}'")
            print(f"   URL: {href}")
            
            # Navigate to the first Access document link
            print(f"Navigating to first Access document link: {href}")
            driver.get(href)

            # Find the English option in the dropdown and download that pdf
            # <div class="select-wrapper"><select class="small-download form-select form-control download" data-once="chosen" style="display:visible; position:absolute; width:0px; height: 0px; clip:rect(0,0,0,0)" tabindex="-1"><option value="https://unfccc.int/sites/default/files/resource/cp2024_01a02A.pdf">Arabic PDF 0.18 MB</option><option value="https://unfccc.int/sites/default/files/resource/cp2024_01a02C.pdf">Chinese PDF 0.22 MB</option><option value="https://unfccc.int/sites/default/files/resource/cp2024_01a02E.pdf">English PDF 0.12 MB</option><option value="https://unfccc.int/sites/default/files/resource/cp2024_01a02F.pdf">French PDF 0.16 MB</option><option value="https://unfccc.int/sites/default/files/resource/cp2024_01a02R.pdf">Russian PDF 0.20 MB</option><option value="https://unfccc.int/sites/default/files/resource/cp2024_01a02S.pdf">Spanish PDF 0.08 MB</option><option selected="" disabled="" class="hidden">Download</option><option selected="" disabled="" class="hidden">Download</option><option selected="" disabled="" class="hidden">Download</option></select><div class="chosen-container chosen-container-single small-download form-select form-control" title=""><a class="chosen-single">
            # <span>Download</span>
            # <div><b></b></div>
            # TODO
            
            # Look for and click "English" option
            select_element = driver.find_element(By.CSS_SELECTOR, "select.small-download")
            # options = select_element.find_elements(By.TAG_NAME, "option")
            # english_option = options.find_element(By.XPATH, ".//option[contains(text(), 'English')]")
            english_option = select_element.find_element(By.XPATH, ".//option[contains(text(), 'English')]")
            english_url = english_option.get_attribute("value")
            print(f"Found English PDF URL: {english_url}")
            print("Downloading the English PDF...")
            
            response = requests.get(english_url)
            if response.status_code == 200:
                file_path = DOWNLOAD_DIR / Path(english_url).name
                file_path.write_bytes(response.content)
                print(f"Downloaded and saved as: {file_path}")
            else:
                print(f"Failed to download the PDF. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        breakpoint()
    
    finally:
        # Close the browser
        driver.quit()
        print("Browser session closed.")


if __name__ == "__main__":
    main()
