import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_tehnomax_requests():
    base_url = "https://tehnomax.me/racunari-i-komponente/laptop-racunari/{}/?mod=catalog&op=browse&view=category&sef_name=racunari-i-komponente%2Flaptop-racunari&filters%5Bstock%5D%5B0%5D=dostupno"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    products = []

    for page in range(1, 9):  
        url = base_url.format(page)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"[Greška] Status kod: {response.status_code} na stranici {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for item in soup.select("div.product-wrap-grid.js-product-ga-wrap"):
            name_tag = item.select_one("div.product-name-grid")
            price_tag = item.select_one("div.price")
            link_tag = item.select_one("a.product-link")

            if name_tag and price_tag and link_tag:
                name = name_tag.get_text(strip=True)
                link = link_tag["href"].strip()
                price_text = price_tag.get_text(strip=True).replace("€", "").replace(".", "").replace(",", ".").strip()

                try:
                    cijena = float(price_text)
                except ValueError:
                    cijena = None

                if name and cijena:
                    products.append({
                        "Naziv": name,
                        "Cijena": cijena,
                        "Link": link,
                        "Izvor": "Tehnomax"
                    })

    df = pd.DataFrame(products, columns=["Naziv", "Cijena", "Link", "Izvor"])
    df.to_csv("laptopovi_tehnomax.csv", index=False)
    print(f"[Tehnomax] Spašeno {len(df)} laptopova.")
    return df

if __name__ == "__main__":
    scrape_tehnomax_requests()
