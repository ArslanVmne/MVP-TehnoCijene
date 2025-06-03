from flask import Flask, render_template, request
import pandas as pd
from math import ceil
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/pretraga")
def pretraga():
    df = pd.read_csv("uporedjeni_laptopovi.csv")
    query = request.args.get("q", "").lower()
    min_price = request.args.get("min", type=float)
    max_price = request.args.get("max", type=float)

    if query:
        df = df[df["Model"].str.lower().str.contains(query)]
    if min_price is not None:
        df = df[df["Najniža cijena (€)"] >= min_price]
    if max_price is not None:
        df = df[df["Najniža cijena (€)"] <= max_price]

    # Sortiranje po cijeni rastuće
    df = df.sort_values("Najniža cijena (€)")

    per_page = 20
    page = int(request.args.get("page", 1))
    total = len(df)
    start = (page - 1) * per_page
    end = start + per_page
    pages = ceil(total / per_page)
    df_page = df.iloc[start:end]

    return render_template(
        "index.html",
        laptops=df_page.to_dict(orient="records"),
        page=page,
        pages=pages,
        query=query,
        max=max,  
        min=min,
        min_price=min_price if min_price is not None else "",
        max_price=max_price if max_price is not None else ""
    )

if __name__ == "__main__":
    print("Ažuriranje podataka...")
    subprocess.run(["python", "scrape_tehnomax.py"])
    subprocess.run(["python", "scrape_tehnoplus.py"])
    subprocess.run(["python", "scrape_pcgamer.py"])
    subprocess.run(["python", "uporedjivanje.py"])
    print("Završeno. Pokrećem aplikaciju...")
    app.run(debug=True, use_reloader=False)
