import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    # Fetch the first page to determine the total number of pages
    initial_url = "https://books.toscrape.com/catalogue/page-1.html"
    response = requests.get(url=initial_url, headers=headers)
    page_text = response.text

    # Extract total number of pages using regex
    pagenum_pattern = r"Page\s+(\d+)\s+of\s+(\d+)"
    total_pages = re.search(pagenum_pattern, page_text)
    if total_pages:
        total_pages = int(total_pages.group(2))
    else:
        print("Could not determine the total number of pages.")
        return []

    print(f"Total pages found: {total_pages}")

    books = []
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}...")
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        div_books = soup.find_all("article", class_="product_pod")

        for book in div_books:
            title = book.h3.a['title']
            price = book.find("p", class_="price_color").text
            relative_link = book.h3.a["href"]

            # Generate absolute link
            if relative_link.startswith("../"):
                absolute_link = "https://books.toscrape.com/catalogue/" + relative_link[9:]
            else:
                absolute_link = "https://books.toscrape.com/catalogue/" + relative_link

            books.append([title, price[1:], absolute_link])

    return books

# Extract data
books = extract_data()

# Convert to DataFrame and save to CSV
if books:
    col_names = ["Title", "Price", "Link"]
    df = pd.DataFrame(data=books, columns=col_names)

    # Display first few rows and save
    print(df.head())
    df.to_csv("extracted_data.csv", index=False)
    print("Data has been saved to 'extracted_data.csv'.")
else:
    print("No data was extracted.")
