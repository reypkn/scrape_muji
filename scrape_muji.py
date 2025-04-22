import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def close_popup(driver):
    """Close the subscription popup on the page."""
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.subbox-close"))
        )
        close_button.click()
    except Exception as e:
        print("Popup not found or already closed:", e)
    

def load_all_products(driver):
    """Click the 'Load more products' button until all products are displayed."""
    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[rel='next']"))
            )
            load_more_button.click()
            time.sleep(2)  # Allow products to load
        except Exception:
            print("No more products to load.")
            break


def get_product_links(driver):
    """Retrieve all product links from the main page."""
    product_elements = driver.find_elements(By.CSS_SELECTOR, "a.list-product-gallery")
    product_links = [product.get_attribute("href") for product in product_elements]
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

    return product_data


def save_to_csv(data, country, product_type):
    """Save scraped data to a CSV file."""
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{date_str}_{country}_{product_type}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "price", "color", "size", "description", "image"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {filename}")


def scrape_muji_products(country, product_type, url):
    """Main function to scrape products data."""
    # Use the Service class to specify the path to chromedriver
    service = Service("/usr/local/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run the browser in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Allow the page to load

        close_popup(driver)
        load_all_products(driver)

        product_links = get_product_links(driver)
        print(f"Found {len(product_links)} products.")

        all_products = []
        for link in product_links:
            product_details = scrape_product_details(driver, link)
            all_products.append(product_details)

        save_to_csv(all_products, country, product_type)

    finally:
        driver.quit()


# Start scraping for UAE stationery products
if __name__ == "__main__":
    scrape_muji_products(
        country="uae",
        product_type="stationery",
        url="https://www.muji.ae/en/shop-stationery-all-stationery/"
    )