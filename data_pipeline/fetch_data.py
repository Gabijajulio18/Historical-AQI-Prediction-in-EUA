import os
from dotenv import load_dotenv
import requests
import pandas as pd
import sqlite3

# Load enviroment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("No API_KEY found. Pleaseset it in your .env file")


# API endpoint
API_URL = "https://api.openaq.org/v3/locations"

DB_FILE = "data/air_quality.db"


def fetch_and_store_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()["results"]

    df = pd.json_normalize(data)

    conn = sqlite3.connect(DB_FILE)
    df.to_sql("air_quality_data", conn, if_exists="append", index=False)
    conn.close()

    print("Data fetch and saved to SQLite DB.")


if __name__ == "__main__":
    fetch_and_store_data()
