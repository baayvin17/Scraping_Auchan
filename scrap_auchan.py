import pandas as pd
import requests
from bs4 import BeautifulSoup

rows = []

def scraping():
    for page in range(1, 5):
        page_url = f"https://www.auchan.fr/high-tech-audio-tv-telephonie/telephonie/smartphones/ca-9531857?page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_thumbnails = soup.find_all('a', class_='product-thumbnail__details-wrapper')

        for thumbnail in product_thumbnails:
            title_element = thumbnail.find('strong', itemprop='brand')
            title = title_element.text.strip() if title_element else "N/A"

            description_element = thumbnail.find('p', class_='product-thumbnail__description')
            description = description_element.text.strip() if description_element else "N/A"

            price_element = thumbnail.find('span', {'data-seller-type': 'ONLINE'})
            price = price_element.text.strip() if price_element else "N/A"

            seller_element = thumbnail.find('div', class_='product-thumbnail__seller-label')
            seller = seller_element.text.strip() if seller_element else "N/A"

            rating_element = thumbnail.find('meter', class_='gauge--star')
            rating = rating_element['value'] if rating_element else "N/A"

            rows.append((title + " " + description, price, seller, rating))

    df = pd.DataFrame(rows, columns=["title", "price", "seller", "rating"])
    df.to_csv(f"auchan_test4{page}.csv", index=False)
    # df.to_excel(f"auchan_test{page}.xlsx", index=False)

scraping()
