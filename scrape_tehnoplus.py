import requests
from bs4 import BeautifulSoup
import pandas as pd
from proxies import proxies

def scrape_tehnoplus_requests():
    base_url = "https://tehnoplus.me/racunar-laptop-tablet/laptop-racunari/?limit=40&sort=1&page={}&manufacturer=0&attr=0&price=0&category_checked=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    products = []

    for page in range(1, 4): 
        url = base_url.format(page)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"[Greška] Status kod: {response.status_code} na stranici {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.select("div.product.artikal"):
            name_tag = item.select_one("h2.woocommerce-loop-product__title")
            price_tag = item.select_one("span.amount.mpc-p")
            link_tag = item.select_one("a.woocommerce-LoopProduct-link")

            if name_tag and price_tag and link_tag:
                name = name_tag.get_text(strip=True)

                cijena_main = price_tag.contents[0].strip().replace("mpc:", "").strip()
                cijena_sup = price_tag.find("sup").get_text(strip=True) if price_tag.find("sup") else "00"
                price = f"{cijena_main}.{cijena_sup}"

                link = "https://tehnoplus.me" + link_tag['href'].strip()

                try:
                    cijena = float(price)
                except ValueError:
                    cijena = None

                if cijena is not None:
                    products.append({
                        "Naziv": name,
                        "Cijena": cijena,
                        "Link": link,
                        "Izvor": "Tehnoplus"
                    })

    df = pd.DataFrame(products)
    df.to_csv("laptopovi_tehnoplus.csv", index=False)
    print(f"[Tehnoplus] Requests: Spašeno {len(df)} laptopova.")
    return df

if __name__ == "__main__":
    scrape_tehnoplus_requests()
