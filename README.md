# scrape_muji

This script is designed to scrape product data from Muji's online shop. It is specifically configured to extract product details such as name, price, color, size, description, and image from a specified country and product type.

The script is written in Python and uses Selenium for web scraping and the `csv` module for saving scraped data into a CSV file.

## Features

- Scrape product data including:
  - **Name**
  - **Price** (amount and currency)
  - **Color**
  - **Size**
  - **Description**
  - **Image URL**
- Automatically handle pop-ups on the website.
- Loads all products by simulating clicks on the "Load more products" button.
- Saves data in a CSV file with the format `YYYYMMDD_country_type.csv`.

## Prerequisites

### Google Chrome:
- Ensure Google Chrome is installed on your system. Check the version:

  ```bash
  google-chrome --version
  ```

### ChromeDriver:
- Install ChromeDriver and ensure it matches the version of Google Chrome.
- On Arch Linux, install ChromeDriver:

  ```bash
  sudo pacman -S chromedriver
  ```

- Move ChromeDriver to `/usr/local/bin/` if necessary:

  ```bash
  sudo mv /path/to/chromedriver /usr/local/bin/
  ```

### Python:
- Install Python 3.7+ and pip.

### Selenium:
- Install Selenium:

  ```bash
  pip install selenium
  ```

## Setup and Usage

1. **Download the Script**: Save the script as `scrape_muji_stationery.py`.

2. **Run the Script**: Execute the script to scrape stationery products for the UAE:

   ```bash
   python scrape_muji_stationery.py
   ```

3. **CSV Output**:
   - The scraped data will be saved as a CSV file in the current directory.
   - **Filename format**: `YYYYMMDD_country_type.csv` (e.g., `20250423_uae_stationery.csv`).

## Updates

1. **Fix for Browser Crashes**:
   - Added logic to periodically close and reopen the browser after scraping a page. This ensures memory is freed and prevents crashes during long scraping sessions.

2. **Handling Tab Crashes**:
   - Implemented a recovery mechanism to detect and handle browser tab crashes. The script now restarts the browser and resumes scraping from the last scraped page.

3. **Improved Logging**:
   - Enhanced logging to track the current page being scraped, whether the page was skipped, and the status of the browser.

## Known Issues

- The script currently encounters issues when scraping new pages after successfully reloading the browser. This needs further investigation to ensure the "Load more products" functionality works as intended. See the open issue for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under NONE.