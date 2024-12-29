import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}

response = requests.get(url = URL, headers=headers)
"""
<article class="product_pod">
    <div class="image_container">
        <a href="catalogue/a-light-in-the-attic_1000/index.html"><img alt="A Light in the Attic" class="thumbnail" src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"/></a>
    </div>
    <p class="star-rating Three">
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>
    </p>
    <h3>
	<a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a>
	</h3>
    <div class="product_price">
        <p class="price_color">£51.77</p>
        <p class="instock availability">
            <i class="icon-ok"></i>
            In stock
        </p>
        <form>
            <button class="btn btn-primary btn-block" data-loading-text="Adding..." type="submit">Add to basket</button>
        </form>
    </div>
</article>
"""
# we are extracting the information of book title,price and its link from the above tags
if response.status_code == 200:
    page_source = response.content

    soup = BeautifulSoup(page_source, "html5lib")
    #print(soup.prettify())
    print("_"*80)
    print("Top Title:\t",soup.find("title").text)
    articles = soup.find_all("article",class_ = "product_pod")
    # Extract the title from the h3 > a tag
    if articles:
        for article in articles:
            title = article.find("h3").a['title']
            link =  article.find("h3").a['href']
            price = article.find("p", class_="price_color").text.strip()
            print("Title:\t", title)
            print("Link:\t", link)
            print("Price:\t", price)




