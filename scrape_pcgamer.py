import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_pcgamer_laptops():
    base_url = "https://pc-gamer.me/c/Laptop?sort=&discounts=&price_min=&price_max=&price_min_mob=&price_max_mob=&page={}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    products = []

    for page in range(1, 11): 
        url = base_url.format(page)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"[Greška] Status kod: {response.status_code} na stranici {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("div.card-footer.card-price-section")

        for block in items:
            wrapper = block.find_parent("div", class_="card")
            if not wrapper:
                continue

            name_tag = wrapper.select_one("h5.text-black")
            price_tag = block.select_one("h4")
            link_tag = wrapper.select_one("a.text-decoration-none")

            if name_tag and price_tag and link_tag:
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True).replace("euro", "").replace("€", "").replace(".", "").replace(",", ".").strip()
                link = "https://pc-gamer.me" + link_tag["href"]

                try:
                    cijena = float(price)
                except ValueError:
                    cijena = None

                if cijena is not None:
                    products.append({
                        "Naziv": name,
                        "Cijena": cijena,
                        "Link": link,
                        "Izvor": "PC-Gamer"
                    })

    df = pd.DataFrame(products)
    df.to_csv("laptopovi_pcgamer.csv", index=False)
    print(f"[PC-Gamer] Spašeno {len(df)} laptopova.")
    return df

if __name__ == "__main__":
    scrape_pcgamer_laptops()
