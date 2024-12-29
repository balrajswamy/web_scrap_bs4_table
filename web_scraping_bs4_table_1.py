import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://ticker.finology.in/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}

response = requests.get(url = URL, headers=headers)

if response.status_code == 200:
    page_source = response.content
    soup = BeautifulSoup(page_source, "html5lib")
    print(soup.title.text.strip())
    table = soup.find("table",class_ = "table table-sm table-hover screenertable")
    colNames = []
    if table:
        print("Table found!")
        theaders = table.find_all("th")
        print("theaders:\t", theaders)
        for colName in theaders:
            colName = colName.get_text(separator= " ", strip=True)
            colNames.append(colName)
    print("colNames:\t",colNames)
    df = pd.DataFrame(columns=colNames)

    #find_all ("tr")
    rows = table.find_all("tr")

    for row in rows[1:]:
        tds = row.find_all("td")
        row = [td.text.strip() for td in tds]
        L = len(df)
        df.loc[L] = row

    #print(df)
    df.to_csv("extracted_table.csv", index=False)