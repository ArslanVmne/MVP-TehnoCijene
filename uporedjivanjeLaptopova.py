import pandas as pd
from difflib import get_close_matches

def normalize(text):
    return text.lower().replace("-", " ").replace("/", " ").replace(",", " ").replace(".", " ").strip()

def uporedi_laptopove(tehnomax_csv, tehnoplus_csv, pcgamer_csv):
    df_tehnomax = pd.read_csv(tehnomax_csv)
    df_tehnoplus = pd.read_csv(tehnoplus_csv)
    df_pcgamer = pd.read_csv(pcgamer_csv)

    svi_laptopovi = pd.concat([df_tehnomax, df_tehnoplus, df_pcgamer], ignore_index=True)
    svi_laptopovi["Naziv_norm"] = svi_laptopovi["Naziv"].apply(normalize)

    grupisano = {}

    for i, row in svi_laptopovi.iterrows():
        naziv = row["Naziv_norm"]
        grupa = None

        for kljuc in grupisano.keys():
            if get_close_matches(naziv, [kljuc], n=1, cutoff=0.85):
                grupa = kljuc
                break

        if grupa:
            grupisano[grupa].append(row)
        else:
            grupisano[naziv] = [row]

    rezultati = []
    for naziv, stavke in grupisano.items():
        ako = pd.DataFrame(stavke)
        najjeftinija = ako.loc[ako["Cijena"].idxmin()]
        rezultati.append({
            "Model": najjeftinija["Naziv"],
            "Najniža cijena (€)": najjeftinija["Cijena"],
            "Prodavnica": najjeftinija["Izvor"],
            "Link": najjeftinija["Link"]
        })

    df_rezultati = pd.DataFrame(rezultati)
    df_rezultati.to_csv("uporedjeni_laptopovi.csv", index=False)
    print(f"Spašeno {len(df_rezultati)} upoređenih modela u uporedjeni_laptopovi.csv")
    return df_rezultati

if __name__ == "__main__":
    uporedi_laptopove("laptopovi_tehnomax.csv", "laptopovi_tehnoplus.csv", "laptopovi_pcgamer.csv")
