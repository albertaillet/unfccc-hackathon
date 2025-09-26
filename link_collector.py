from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys


def collect_access_document_links(output_file="access_document_links.txt"):
    """
    Collect all 'Access document' links from the UNFCCC COP-29 page and save them to a file.
    
    Args:
        output_file (str): File to save the links to, one per line
    """
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
        
        print(f"Found {len(access_document_links)} anchor elements containing 'Access document'")
        
        # Extract URLs and save to file
        urls = []
        for i, link in enumerate(access_document_links, 1):
            try:
                text = link.text.strip()
                href = link.get_attribute('href')
                if href:
                    urls.append(href)
                    print(f"{i}. Text: '{text}'")
                    print(f"   URL: {href}")
            except Exception as e:
                print(f"{i}. Error extracting link info: {e}")
        
        # Save URLs to file
        with open(output_file, 'w') as f:
            for url in urls:
                f.write(url + '\n')
        
        print(f"\nSaved {len(urls)} URLs to {output_file}")
        
        if len(urls) == 0:
            print("No 'Access document' links found. Checking for similar patterns...")
            
            # Check for similar links
            similar_links = driver.find_elements(
                By.XPATH, 
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'access') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'document')]"
            )
            
            print(f"Found {len(similar_links)} similar links:")
            similar_urls = []
            for i, link in enumerate(similar_links[:10], 1):  # Limit to first 10
                try:
                    text = link.text.strip()
                    href = link.get_attribute('href')
                    if href:
                        similar_urls.append(href)
                        print(f"{i}. Text: '{text}'")
                        print(f"   URL: {href}")
                except Exception as e:
                    print(f"{i}. Error extracting link info: {e}")
            
            if similar_urls:
                similar_file = "similar_links.txt"
                with open(similar_file, 'w') as f:
                    for url in similar_urls:
                        f.write(url + '\n')
                print(f"\nSaved {len(similar_urls)} similar URLs to {similar_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()
        print("Browser session closed.")


def main():
    """Main function to run the link collector."""
    output_file = "access_document_links.txt"
    
    # Check if output file is provided as command line argument
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    
    collect_access_document_links(output_file)


if __name__ == "__main__":
    main()