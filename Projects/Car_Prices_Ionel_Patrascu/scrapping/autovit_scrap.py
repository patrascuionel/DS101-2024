import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging

"""
This script scrapes data from the Autovit website for BMW Series 3 cars.
It extracts information such as model, engine size, horsepower, year, location,
mileage, fuel type, price, and URL.
It handles pagination and saves the data to a CSV file.
It also includes error handling for unexpected subtitle formats.
It uses BeautifulSoup for HTML parsing and Pandas for data manipulation.

Important Notes:
- Although the script proved to be working at the time of writing, there seems to
    be some randomly generated class names in the HTML structure of the website,
    which may change over time. This could lead to the script breaking in the future.
    If that happens, you may need to inspect the HTML structure of the website
    and update the class names in the `process_search_results` function accordingly.
- Sample std output is available in the `autovit_sample.out` file.
- Sample CSV output is available in the `autovit_sample.csv` file.
"""

# Global configuration
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL of the website to scrape
BASE_URL = "https://www.autovit.ro/autoturisme/bmw/seria-3?search%5Border%5D=filter_float_price%3Aasc"

# Define headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Set the number of pages to scrape - manually adjust this if needed
PAGES_TO_SCRAPE = 1

def add_page_to_url(url, page_number):
    """
    Add the page number to the URL for pagination.

    Args:
        url (str): The base URL to which the page number will be added.
        page_number (int): The page number to add to the URL.

    Returns:
        str: The URL with the page number appended.
    """
    if page_number > 1:
        return f"{url}&page={page_number}"
    return url

def process_search_results(search_results):
    """
    Process the search results and extract relevant data.

    Args:
        search_results (list): A list of BeautifulSoup objects representing the search results.
    Returns:
        list: A list of dictionaries containing the extracted data.
    Raises:
        ValueError: If the subtitle format is unexpected.
    """
    data = []

    
    for result in search_results:
        title_box = result.find('h2', class_='etydmma0 ooa-16c293i')
        print(title_box)
        model = title_box.find('a').text.split('\n')[0]
        url = title_box.find('a')['href']
        
        subtitle = result.find('p', class_='e1afgq2j0 ooa-w3crlp').text
        if '\xe2\\x80\\xa2' in subtitle:
            subtitle = subtitle.split('\\xe2\\x80\\xa2')
        elif '•' in subtitle:
            subtitle = subtitle.split('•')
        else:
            print(f"Unexpected subtitle format: {subtitle}")
            print(f"Current result: {result}")
            raise ValueError(f"Unexpected subtitle format while processing {url}")

        engine_size = subtitle[0].strip().replace('cm3', '').replace(' ', '')
        horse_power = subtitle[1].strip().replace('CP', '').replace(' ', '')
        mileage = result.find('dd', {'data-parameter': 'mileage'}).text.strip().replace('km', '').replace(' ', '')
        year = result.find('dd', {'data-parameter': 'year'}).text.strip()
        fuel_type = result.find('dd', {'data-parameter': 'fuel_type'}).text.strip()
        location = result.find('p', class_='ooa-oj1jk2').text.split('(')[1].split(')')[0].strip()
        price = result.find('h3', class_='efzkujb1 ooa-1d59yzt').text.strip().replace(' ', '').split(',')[0]

        data.append({
            'Model': model,
            'Engine Size (cm3)': engine_size,
            'Horse Power (HP)': horse_power,
            'Year': year,
            'Location': location,
            'Kilometers': mileage,
            'Fuel Type': fuel_type,
            'Price (EUR)': price,
            'URL': url
        })
    return data


if __name__ == "__main__":
    logging.info("Starting the scraping process...")
    logging.info(f"Scraping {PAGES_TO_SCRAPE} pages from {BASE_URL}")
    # Create a Pandas DataFrame
    df = pd.DataFrame()

    # Loop through the specified number of pages
    for page in range(1, PAGES_TO_SCRAPE + 1):
        url = add_page_to_url(BASE_URL, page)
        logging.info(f"Scraping page {page}: {url}")

        # Send a GET request to the URL
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        search_results = soup.find_all('article', class_='ooa-16cop2i eg9746i0')
        data = process_search_results(search_results)

        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

        # Check if DataFrame is empty
        if df.empty:
            logging.warning(f"No data found on page {page}.")
            raise ValueError(f"No data found on page {page}.")
        else:
            logging.info(f"Scraped {len(data)} records from page {page}.")

        # Wait for a short period to avoid being flagged as a bot
        if page < PAGES_TO_SCRAPE:
            wait_time = random.uniform(60, 120)
            logging.info(f"Waiting for {wait_time:.2f} seconds before the next request.")
            # Sleep for a random time between 60 to 120 seconds
            time.sleep(wait_time)

    # Print the DataFrame
    logging.info("Scraping complete. DataFrame created.")
    print(df.head())
    logging.info(f"Total records scraped: {len(df)}")

    # Save the DataFrame to a CSV file
    time_str = time.strftime("%Y%m%d_%H%M%S")
    csv_file_path = f'../csvs/seria3_{time_str}.csv'
    df.to_csv(csv_file_path, index=False, encoding='utf-8')

    logging.info(f"Data saved to {csv_file_path}")