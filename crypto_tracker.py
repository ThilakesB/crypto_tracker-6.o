import os
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
CSV_FILE = 'crypto_prices.csv'
TARGET_URL = 'https://coinmarketcap.com/'
TOP_N = 10

def setup_driver():
    """
    Sets up the Chrome WebDriver with headless options for background execution.
    Uses webdriver_manager to automatically handle driver installation.
    """
    print("Setting up Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Automatic driver management
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_data(driver):
    """
    Scrapes the top cryptocurrency data from the loaded page.
    """
    print(f"Navigating to {TARGET_URL}...")
    driver.get(TARGET_URL)

    # Wait for the table body to be present to ensure dynamic content is loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table tbody tr"))
        )
    except Exception as e:
        print(f"Error waiting for table: {e}")
        return []

    # Scroll down slightly to trigger lazy loading if necessary (usually top 10 are visible)
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2) # Brief pause for stability

    print("Extracting data...")
    data = []
    # Identify rows in the main table
    rows = driver.find_elements(By.CSS_SELECTOR, "table.cmc-table tbody tr")

    # Limit to top N coins
    count = 0
    for row in rows:
        if count >= TOP_N:
            break
        try:
            # Use column indices which are more stable than random class names
            cols = row.find_elements(By.TAG_NAME, "td")
            
            # Ensure we have enough columns (standard CMC table has > 10 columns)
            if len(cols) < 8:
                continue

            # Column 3: Name (contains Name and Symbol in separate elements usually)
            # We explicitly look for the <p> tags for name and symbol usually present here
            # Or just take the text, split by newline
            name_text = cols[2].text.replace('\n', ' ')
            
            # Column 4: Price
            price_text = cols[3].text
            
            # Column 5: 1h, Column 6: 24h
            change_24h_text = cols[5].text
            
            # Column 8: Market Cap (sometimes 7 depends on window size, but 8 is standard desktop)
            market_cap_text = cols[7].text

            # Timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data.append({
                "Timestamp": timestamp,
                "Name": name_text,
                "Price": price_text,
                "24h Change": change_24h_text,
                "Market Cap": market_cap_text
            })
            print(f"Scraped: {name_text} - {price_text}")
            count += 1

        except Exception as e:
            # Skip executing rows that might be ads or malformed
            # print(f"Skipping row due to: {e}") # Optional debug
            continue

    return data

def save_to_csv(data):
    """
    Saves the list of dictionaries to a CSV file.
    Appends if file exists, creates new if not.
    """
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    
    # Check if file exists to determine if header is needed
    header_needed = not os.path.exists(CSV_FILE)
    
    try:
        df.to_csv(CSV_FILE, mode='a', header=header_needed, index=False)
        print(f"Data successfully saved to {CSV_FILE}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    driver = None
    try:
        driver = setup_driver()
        data = scrape_data(driver)
        save_to_csv(data)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if driver:
            print("Closing driver...")
            driver.quit()

if __name__ == "__main__":
    main()
