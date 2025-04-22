# scrape_muji

This script is designed to scrape product data from Muji's online shop. It is specifically configured to extract product details such as name, price, color, size, description, and image from a specified country and product type. 

The script is written in Python and uses Selenium for web scraping and the `csv` module for saving scraped data into a CSV file.

---

## Features

- Scrape product data including:
  - Name
  - Price (amount and currency)
  - Color
  - Size
  - Description
  - Image URL
- Automatically handle pop-ups on the website.
- Loads all products by simulating clicks on the "Load more products" button.
- Saves data in a CSV file with the format `YYYYMMDD_country_type.csv`.

---

## Prerequisites

1. **Google Chrome**:
   - Ensure Google Chrome is installed on your system. Check the version:
     ```bash
     google-chrome --version
     ```

2. **ChromeDriver**:
   - Install ChromeDriver and ensure it matches the version of Google Chrome.
   - On Arch Linux, install ChromeDriver:
     ```bash
     sudo pacman -S chromedriver
     ```
   - Move ChromeDriver to `/usr/local/bin/` if necessary:
     ```bash
     sudo mv /path/to/chromedriver /usr/local/bin/
     ```

3. **Python**:
   - Install Python 3.7+ and `pip`.

4. **Selenium**:
   - Install Selenium:
     ```bash
     pip install selenium
     ```

---

## Setup and Usage

1. **Download the Script**:
   Save the script as `scrape_muji_stationery.py`.

2. **Run the Script**:
   Execute the script to scrape stationery products for the UAE:
   ```bash
   python scrape_muji_stationery.py
   ```

3. **CSV Output**:
   - The scraped data will be saved as a CSV file in the current directory.
   - Filename format: `YYYYMMDD_country_type.csv` (e.g., `20250422_uae_stationery.csv`).

---

## Known Issue

- The script currently scrapes only the first 36 items displayed on the page. It seems the "Load more products" functionality is not working as intended. This might be due to a delay in loading the button or an issue with how Selenium interacts with the page. See the open [issue](https://github.com/reypkn/scrape_muji/issues) for details.

---

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under NONE.