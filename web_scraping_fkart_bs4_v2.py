import pandas as pd
import requests
from bs4 import BeautifulSoup
import re



def extracting_data(total_page):
    df = pd.DataFrame(columns=["product_title", "product_price", "product_ratings"])

    for i in range(1, total_page + 1):
        URL = "https://www.flipkart.com/search?q=mobiles&page=" + str(i)
        print(f"page=={i}")
        response = requests.get(url=URL, headers=headers)
        page_source = response.content
        soup = BeautifulSoup(page_source, "html5lib")
        # print(soup.title.text.strip())
        container = soup.find_all("div", class_="yKfJKb row")
        # print(len(container))
        for box in container:
            product_title = box.find("div", class_="KzDlHZ")
            # print("product_title:\t",product_title.text)
            product_price = box.find("div", class_="Nx9bqj _4b5DiR")
            # print("product_price:\t",product_price.text)
            product_ratings = box.find("div", class_="XQDdHH")
            # print("product_ratings:\t", product_ratings.text)
            row = [product_title.text, product_price.text, product_ratings.text]
            df.loc[len(df)] = row
    df.to_csv("fk_extracted.csv", index=False)
    return True

URL = "https://www.flipkart.com/search?q=mobiles&page=1"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}

response = requests.get(url = URL, headers=headers)

if response.status_code == 200:
    page_source = response.content
    page_text = response.text
    #print("page_text\n", page_text)
    #Page 1 of 435
    pagenum_pattern = r"(Page 1 of )(\d+)"
    result = re.search(pagenum_pattern,page_text)
    total_page = 1
    if result:
        total_page = int(result.group(2))
    print("total_page:\t", total_page)
    output = extracting_data(10)
    if output is True:
        print("Successfully extracted!")


