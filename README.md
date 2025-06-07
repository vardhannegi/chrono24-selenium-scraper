# Chrono24 Pre-Owned Watches Scraper

This project is a Python-based web scraper designed to collect detailed information about pre-owned watches listed on [Chrono24](https://www.chrono24.in). It uses Selenium for browser automation and BeautifulSoup for HTML parsing. The scraper navigates through thousands of paginated listings, extracts links to individual watch pages, and then collects structured data from each listing.

---

## Features

- **Automated Browsing:** Uses Selenium to navigate Chrono24's paginated listings.
- **Data Extraction:** Extracts all watch listing URLs and then scrapes detailed information from each listing.
- **Multithreading:** Fetches data from multiple listings in parallel for efficiency.
- **Data Storage:** Saves all collected data in a structured JSON file.
- **Analysis:** Counts the frequency of alphabets in listing keys for basic data analysis.

---

## Requirements

- Python 3.7+
- Google Chrome browser
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (compatible with your Chrome version)
- The following Python packages:
  - selenium
  - beautifulsoup4

Install dependencies using pip:

```bash
pip install selenium beautifulsoup4
```

---

## Usage

1. **Download ChromeDriver:**
   - Download the appropriate version of ChromeDriver for your OS and Chrome version.
   - Place the `chromedriver` executable in your system PATH or in the project directory.

2. **Run the Script:**
   - You can run the script as a standalone Python file or as a Jupyter Notebook cell.
   - The script is organized with a `main()` function and can be executed directly.

   ```bash
   python final.py
   ```

   Or, if using Jupyter Notebook, run all cells.

3. **Output Files:**
   - `allEndPoins.txt`: Contains all extracted watch listing URLs.
   - `chrono24_watch_data.json`: Contains the structured data for each watch listing.

---

## How It Works

### 1. Collect All Listing URLs

- The script starts by visiting the main pre-owned watches page.
- It iterates through all paginated result pages (over 2,300 pages).
- On each page, it extracts all links to individual watch listings and saves them to a list.

### 2. Scrape Data from Each Listing

- For each listing URL, a new Selenium driver is launched.
- The script parses the watch details table, organizing data into sections (e.g., "Basic Info", "General", etc.).
- Each watch's data is stored in a dictionary, keyed by its unique listing code.

### 3. Multithreading

- Data extraction for each listing is performed in parallel using Python's `Thread` class, speeding up the scraping process.

### 4. Save and Analyze Data

- All collected data is saved as a JSON file.
- The script also performs a simple analysis: counting the most and least frequent alphabets in the listing keys.

---

## Code Structure

- **setup_driver()**: Configures and returns a headless Chrome WebDriver.
- **accept_cookies(driver)**: Handles cookie consent pop-ups.
- **get_all_href_pages(html_doc)**: Extracts all listing URLs from a page.
- **collect_all_hrefs()**: Iterates through all result pages to collect listing URLs.
- **save_hrefs_to_file()**: Saves all collected URLs to a text file.
- **get_data(i)**: Scrapes data from a single listing.
- **fetch_all_data()**: Runs `get_data` for all listings in parallel.
- **save_data_to_json()**: Saves the final data dictionary to a JSON file.
- **analyze_keys()**: Analyzes the frequency of alphabets in the listing keys.
- **main()**: Orchestrates the entire scraping process.

---

## Notes & Tips

- **Performance:** Scraping thousands of pages and listings is resource-intensive and may take several hours.
- **Ethics:** Respect the website's robots.txt and terms of service. Do not overload the server.
- **Error Handling:** Failed indices are tracked and can be retried if needed.
- **Customization:** You can adjust the number of pages or add more data fields as needed.

---

## Example Output

- `chrono24_watch_data.json` will look like:

```json
{
  "AB12345": {
    "Basic Info": {
      "Listing code": "AB12345",
      "Brand": "Rolex",
      ...
    },
    "General": {
      ...
    }
  },
  ...
}
```

---

## License

This project is for educational and personal use only. Please do not use it for commercial purposes or violate Chrono24's terms of service.

---

## Author

- [Your Name]
- [Your Contact Information]

---