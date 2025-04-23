import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime


def close_popup(driver):
    """Close the subscription popup on the page."""
    try:
        popup_locator = (By.CSS_SELECTOR, "span.subbox-close")
        if WebDriverWait(driver, 10).until(EC.presence_of_element_located(popup_locator)):  # Wait 10 seconds for popup
            close_button = driver.find_element(*popup_locator)
            close_button.click()
    except TimeoutException:
        print("Popup not found or already closed.")


def load_more_products(driver, page_count, wait_time=20):
    """Click the 'Load more products' button to load more items."""
    print(f"Attempting to load page {page_count + 1}...")
    try:
        print("Waiting for 'Load more products' button...")
        load_more_button = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[rel='next']"))
        )
        print("Clicking 'Load more products' button...")
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(2)  # Allow new products to load
        print(f"Successfully loaded page {page_count + 1}.")
        return True
    except TimeoutException:
        print("Failed to click 'Load more products' button or button not found.")
        return False


def get_product_links(driver):
    """Retrieve all product links from the main page."""
    product_elements = driver.find_elements(By.CSS_SELECTOR, "a.list-product-gallery")
    product_links = [product.get_attribute("href") for product in product_elements]
    print(f"Total product links found: {len(product_links)}")
    return product_links


def scrape_product_details(driver, url):
    """Scrape product details from an individual product page."""
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    product_data = {}

    # Scrape name
    try:
        product_data['name'] = driver.find_element(By.CSS_SELECTOR, "h1 > span").text
    except Exception:
        product_data['name'] = None

    # Scrape price
    try:
        price_currency = driver.find_element(By.CSS_SELECTOR, ".price-currency").text
        price_amount = driver.find_element(By.CSS_SELECTOR, ".price-amount").text
        product_data['price'] = f"{price_currency} {price_amount}"
    except Exception:
        product_data['price'] = None

    # Scrape color
    try:
        product_data['color'] = driver.find_element(By.CSS_SELECTOR, "h4.list-title span.selected-text").text
    except Exception:
        product_data['color'] = None

    # Scrape size
    try:
        product_data['size'] = driver.find_element(By.CSS_SELECTOR, "h4.list-title:nth-of-type(2) span.selected-text").text
    except Exception:
        product_data['size'] = None

    # Scrape description
    try:
        product_data['description'] = driver.find_element(By.CSS_SELECTOR, ".short-summary").text
    except Exception:
        product_data['description'] = None

    # Scrape image URL
    try:
        product_data['image'] = driver.find_element(By.CSS_SELECTOR, "img[data-zoom-url]").get_attribute("src")
    except Exception:
        product_data['image'] = None

    product_data['url'] = url  # Add the product URL for tracking
    return product_data


def save_to_csv(data, filename):
    """Save scraped data to a CSV file."""
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "price", "color", "size", "description", "image", "url"])
        if not file_exists:
            writer.writeheader()  # Write header only if file does not exist
        writer.writerows(data)

    print(f"Data saved to {filename}")


def load_existing_urls(filename):
    """Load existing product URLs from the CSV file."""
    if not os.path.isfile(filename):
        return set()

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {row['url'] for row in reader}


def reopen_browser(service, options, url):
    """Close and reopen the browser, then return the new driver."""
    print("Reopening the browser...")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(3)  # Allow the page to load
    close_popup(driver)
    return driver


def scrape_muji_products(country, product_type, url):
    """Main function to scrape products data."""
    service = Service("/usr/local/bin/chromedriver")
    options = webdriver.ChromeOptions()

    # Enable headless mode and optimize resource usage
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    filename = f"{datetime.now().strftime('%Y%m%d')}_{country}_{product_type}.csv"
    scraped_urls = load_existing_urls(filename)
    page_count = 0  # Initialize page count

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Allow the page to load

        close_popup(driver)

        while True:
            print(f"Working on page {page_count + 1}...")

            # Get product links
            product_links = get_product_links(driver)
            new_products = [link for link in product_links if link not in scraped_urls]
            print(f"Found {len(new_products)} new products to scrape.")

            page_scraped = False  # Flag to track if current page was scraped

            if not new_products:
                print("No new products found on this page. Checking if there are more pages...")
                if not load_more_products(driver, page_count, wait_time=20):
                    print("No more pages to load. Exiting.")
                    break
                page_count += 1
                continue

            # Scrape new product details
            all_products = []
            for idx, link in enumerate(new_products):
                print(f"Scraping product {idx + 1}/{len(new_products)}: {link}")
                product_details = scrape_product_details(driver, link)
                all_products.append(product_details)
                scraped_urls.add(link)  # Add to the set of scraped URLs

            # Save scraped data
            save_to_csv(all_products, filename)
            page_scraped = True  # Mark the page as scraped

            # Close and reopen browser if the page was scraped
            if page_scraped:
                driver.quit()  # Close the browser
                driver = reopen_browser(service, options, url)  # Reopen the browser
                # Navigate back to the last page
                for _ in range(page_count):
                    if not load_more_products(driver, page_count, wait_time=20):
                        print("Failed to navigate to the correct page after reopening the browser.")
                        break

            # Try to load the next page
            if not load_more_products(driver, page_count, wait_time=20):
                print("No more pages to load. Exiting.")
                break
            page_count += 1

    except WebDriverException as e:
        print(f"Browser error occurred: {e}. Restarting browser...")
        driver.quit()
        driver = reopen_browser(service, options, url)
        scrape_muji_products(country, product_type, url)  # Resume scraping

    finally:
        driver.quit()


# Start scraping
if __name__ == "__main__":
    scrape_muji_products(
        country="uae",
        product_type="stationery",
        url="https://www.muji.ae/en/shop-stationery-all-stationery/"
    )