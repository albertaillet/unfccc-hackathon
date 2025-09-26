from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

URL = os.getenv("URL", "https://unfccc.int/event/cop-29")

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

            # Find and click the "No Thanks" button if it exists
            # no_thanks_button = driver.find_element(By.XPATH, "//button[contains(text(), 'No Thanks')]")
            # it has id onesignal-slidedown-cancel-button
            no_thanks_button = driver.find_element(By.ID, "onesignal-slidedown-cancel-button")

            print("Found 'No Thanks' button, clicking it...")
            no_thanks_button.click()
            time.sleep(2)  # Wait for any potential modal to close
            
            # Wait for the page to load
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)
            
            print("Looking for download dropdown with class='chosen-single'...")
            download_dropdown = driver.find_element(By.CLASS_NAME, "chosen-single")
            
            print("Found download dropdown, clicking it...")
            download_dropdown.click()
            
            # Wait a moment for dropdown to appear
            time.sleep(2)
            
            # Look for and click "English" option
            print("Looking for 'English' option in dropdown...")
            english_option = driver.find_element(By.XPATH, "//li[contains(text(), 'English')]")
            
            print("Clicking 'English' option...")
            english_option.click()
            
        print("Successfully selected English from dropdown!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        breakpoint()
    
    finally:
        # Close the browser
        driver.quit()
        print("Browser session closed.")


if __name__ == "__main__":
    main()
