import json
from time import sleep
from bs4 import BeautifulSoup
from collections import Counter
from threading import Thread, Lock
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

DOMAIN = 'https://www.chrono24.in'
ENDPOINT = '/watches/pre-owned-watches--64.htm?pageSize=120'
CUSTOM_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/92.0.4515.159 Safari/537.36"
)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f"user-agent={CUSTOM_USER_AGENT}")

lock = Lock()
allHrefs = []
finaldf = {}
faildIndex = []

def setup_driver():
    return webdriver.Chrome(options=chrome_options)

def accept_cookies(driver):
    try:
        click = driver.find_element(By.XPATH, '/html/body/dialog/div/div[2]/button')
        click.send_keys(Keys.ENTER)
    except Exception as e:
        print("Cookie dialog not found or already accepted:", e)

def get_all_href_pages(html_doc):
    hrefs = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    articles = soup.find_all('a', class_='js-article-item article-item block-item rcard')
    for article in articles:
        href = article.get('href')
        if href:
            hrefs.append(href)
    return hrefs

def collect_all_hrefs():
    global allHrefs
    driver = setup_driver()
    url = f'{DOMAIN}{ENDPOINT}'
    driver.get(url)
    sleep(1)
    accept_cookies(driver)
    for page in range(1, 2352):
        if page != 1:
            url = f'{DOMAIN}/watches/pre-owned-watches--64-{page}.htm?pageSize=120'
            driver.get(url)
        html = driver.page_source
        allHrefs += get_all_href_pages(html)
    driver.quit()

def save_hrefs_to_file():
    with open("allEndPoins.txt", 'w') as f:
        for href in allHrefs:
            f.write(f'{href}\n')

def get_data(i):
    endPoint = allHrefs[i]
    url1 = f'{DOMAIN}{endPoint}'
    driver = setup_driver()
    try:
        driver.get(url1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        sectioned_data = {}
        section = "General"
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 1 and cells[0].find('h3'):
                    section = cells[0].get_text(strip=True)
                    sectioned_data[section] = {}
                elif len(cells) == 2:
                    label = cells[0].get_text(strip=True)
                    value = cells[1].get_text(" ", strip=True)
                    if section not in sectioned_data:
                        sectioned_data[section] = {}
                    sectioned_data[section][label] = value
        reference_number = sectioned_data.get("Basic Info", {}).get("Listing code", None)
        listing_code = sectioned_data.get("Basic Info", {}).get("Listing code", None)
        url_id = endPoint.split('--')[-1].replace('.htm', '')
        if listing_code:
            key = f"{listing_code}"
        elif reference_number:
            key = f"{reference_number}"
        else:
            key = f"UNKNOWN_{url_id}"
        with lock:
            finaldf[key] = sectioned_data
        print(f"Fetched: {key} from {url1}")
    except Exception as e:
        with lock:
            faildIndex.append(i)
        print("ERROR", e)
    finally:
        driver.quit()

def fetch_all_data():
    threads = [Thread(target=get_data, args=(i,)) for i in range(len(allHrefs))]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def save_data_to_json():
    with open("chrono24_watch_data.json", "w") as f:
        json.dump(finaldf, f, indent=2)

def analyze_keys():
    all_keys = "".join(finaldf.keys())
    alphabet_counter = Counter(c for c in all_keys if c.isalpha())
    most_common = alphabet_counter.most_common(1)[0]
    least_common = alphabet_counter.most_common()[-1]
    print('Most repeating : ', most_common, "Least Repeating : ", least_common)

def main():
    print("Collecting all hrefs...")
    collect_all_hrefs()
    print(f"Total hrefs collected: {len(allHrefs)}")
    save_hrefs_to_file()
    print("Fetching data for all hrefs...")
    fetch_all_data()
    save_data_to_json()
    analyze_keys()

if __name__ == "__main__":
    main()