from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def main():
    print("Starting headless browser session to UNFCCC COP-29 event page...")
    
    # Set up Safari options for headless browsing
    safari_options = Options()
    safari_options.add_argument("--headless")
    
    # Initialize the Safari driver
    driver = webdriver.Safari(options=safari_options)
    
    try:
        # Navigate to the UNFCCC COP-29 event page
        url = "https://unfccc.int/event/cop-29"
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Give the page a moment to fully load dynamic content
        time.sleep(3)
        
        # Search for all anchor elements containing "Access document"
        print("Searching for anchor elements containing 'Access document'...")
        
        # Find all anchor elements that contain the text "Access document"
        access_document_links = driver.find_elements(
            By.XPATH, 
            "//a[contains(text(), 'Access document')]"
        )
        
        print(f"Found {len(access_document_links)} anchor elements containing 'Access document':")
        
        for i, link in enumerate(access_document_links, 1):
            try:
                text = link.text.strip()
                href = link.get_attribute('href')
                print(f"{i}. Text: '{text}'")
                print(f"   URL: {href}")
                print()
            except Exception as e:
                print(f"{i}. Error extracting link info: {e}")
        
        if len(access_document_links) == 0:
            print("No anchor elements containing 'Access document' were found on the page.")
            
            # Let's also check for any links that might be similar
            print("\nChecking for similar text patterns...")
            similar_links = driver.find_elements(
                By.XPATH, 
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'access') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'document')]"
            )
            
            print(f"Found {len(similar_links)} links containing 'access' or 'document':")
            for i, link in enumerate(similar_links[:10], 1):  # Limit to first 10
                try:
                    text = link.text.strip()
                    href = link.get_attribute('href')
                    print(f"{i}. Text: '{text}'")
                    print(f"   URL: {href}")
                    print()
                except Exception as e:
                    print(f"{i}. Error extracting link info: {e}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()
        print("Browser session closed.")


if __name__ == "__main__":
    main()
