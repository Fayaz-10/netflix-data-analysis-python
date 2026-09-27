import os
import sys
import urllib.request
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
CSV_PATH = os.path.join(RAW_DIR, "netflix_titles.csv")

URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv"

def download_data():
    os.makedirs(RAW_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        print(f"Downloading authentic Netflix dataset from {URL}...")
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response, open(CSV_PATH, "wb") as out_file:
            out_file.write(response.read())
        print(f"Downloaded dataset to {CSV_PATH}")
    else:
        print(f"Dataset already exists at {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("Columns:", df.columns.tolist())

if __name__ == "__main__":
    download_data()
