import os
import json
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

headers = {"X-API-Key": API_KEY, "User-Agent": "MyApp/1.0"}


def fetch_and_store_data():
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    data = response.json().get("results", [])
    if not data:
        print("No data found.")
        return

    df = pd.json_normalize(data)

    # Convert list/dict columns to JSON strings
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            df[col] = df[col].apply(
                lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x
            )

    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    df.to_sql("air_quality_data", conn, if_exists="replace", index=False)
    conn.close()

    print("Data fetch and saved to SQLite DB.")


if __name__ == "__main__":
    fetch_and_store_data()
