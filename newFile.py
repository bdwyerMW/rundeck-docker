print("Starting testScrape.py...")

print("testing the new git refreshes - it worked!")
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import platform
import tempfile
import os

# Configure Chrome options for cross-platform compatibility
chrome_options = Options()

print("Setting up Chrome options...")

# Create a unique temporary profile directory to avoid conflicts
temp_profile = tempfile.mkdtemp(prefix="chrome_profile_")
print(f"Using temporary profile: {temp_profile}")

# Essential options for all environments
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--disable-images")  # Faster loading
chrome_options.add_argument("--disable-javascript")  # Remove if you need JS
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

# Use unique temp directory to avoid conflicts
#chrome_options.add_argument(f"--user-data-dir={temp_profile}")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--remote-debugging-port=0")  # Use random port
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-renderer-backgrounding")

# Additional options for better compatibility
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-popup-blocking")

# Detect if running on Linux and likely in a headless environment
if platform.system() == "Linux":
    # Add headless mode for Linux (common for servers without display)
    # Comment out the next line if you want to see the browser on Linux desktop
    chrome_options.add_argument("--headless")
    # Additional Linux-specific options
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-crash-reporter")
    chrome_options.add_argument("--disable-in-process-stack-traces")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-tools")
    print("Running in Linux mode with headless browser")
else:
    print(f"Running on {platform.system()}")

# Use Chrome with automatic driver management (works better than Edge)
try:
    print("Initializing Chrome browser...")
    # Selenium 4+ automatically downloads and manages ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)
    print("Chrome browser initialized successfully")
except Exception as e:
    print(f"Failed to initialize Chrome: {e}")
    print("Make sure Google Chrome is installed and updated")
    if platform.system() == "Linux":
        print("On Linux: sudo apt-get install google-chrome-stable")
        print("Or try: sudo apt-get install chromium-browser")
    else:
        print("Windows: Make sure Chrome is installed from https://www.google.com/chrome/")
    
    # Clean up temp directory if browser failed to start
    try:
        import shutil
        shutil.rmtree(temp_profile, ignore_errors=True)
    except:
        pass
    exit(1)

try:
    # Open a webpage
    print("Navigating to https://example.com...")
    driver.get('https://example.com')
    
    # Wait a moment for the page to load
    time.sleep(3)
    
    # Optional: Interact with the page
    print(f"Page title: {driver.title}")  # Print the page title
    print(f"Current URL: {driver.current_url}")
    
    # Get some page content to verify it's working
    page_source_length = len(driver.page_source)
    print(f"Page source length: {page_source_length} characters")
    
    # Example: Find and interact with elements (even in headless mode)
    try:
        # Find a link on the page (example.com has a "More information..." link)
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "More information")
        print(f"Found link: {link.text}")
        print(f"Link URL: {link.get_attribute('href')}")
        
        # Click the link (this works in headless mode!)
        print("Clicking the 'More information' link...")
        link.click()
        
        # Wait for navigation
        time.sleep(2)
        
        # Check new page
        print(f"New page title: {driver.title}")
        print(f"New URL: {driver.current_url}")
        # Display the content of the new page (first 1000 characters for brevity)
        new_page_content = driver.page_source
        print("New page content (first 1000 chars):")
        print(new_page_content[500:1000])
        
        # Go back to previous page
        print("Going back to previous page...")
        driver.back()
        time.sleep(1)
        print(f"Back to: {driver.current_url}")
        
    except Exception as nav_error:
        print(f"Navigation example failed: {nav_error}")
        print("This is normal - the page structure might have changed")
    
    # On Linux headless mode, we won't see the browser, so shorter wait
    if platform.system() == "Linux":
        print("Headless mode - closing browser in 2 seconds...")
        time.sleep(2)
    else:
        print("Browser will close in 5 seconds...")
        time.sleep(5)
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Make sure to close the browser
    try:
        driver.quit()
        print("Browser closed successfully!")
    except:
        print("Browser was already closed or failed to close properly")
    
    # Clean up temporary directory
    try:
        import shutil
        shutil.rmtree(temp_profile, ignore_errors=True)
        print("Temporary files cleaned up")
    except Exception as cleanup_error:
        print(f"Note: Some temporary files may remain: {cleanup_error}")
