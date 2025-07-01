import os
import requests
import pandas as pd
import sqlite3
from dotenv import load_dotenv
from time import sleep, time
from datetime import datetime, timedelta

# Load API Key
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("No API_KEY found. Please set it in your .env file")

# Constants
DB_FILE = "data/air_quality.db"
ZIP_CODES = ["90001", "10001", "60601"]  # Example: Los Angeles, New York, Chicago
PARAMETERS = ["PM2.5", "PM10", "O3", "NO2"]  # AirNow parameter names
START_DATE = datetime(2020, 7, 1)
END_DATE = datetime(2025, 7, 1)
BASE_URL = "https://www.airnowapi.org/aq/observation/zipCode/historical/"


def fetch_airnow_data(zip_code, start_date, end_date):
    all_data = []
    date = start_date
    request_count = 0
    while date <= end_date:
        if request_count >= 500:
            print("Hit 500 requests. Sleeping for 1 hour to respect rate limit...")
            sleep(3600)
            request_count = 0
        params = {
            "format": "application/json",
            "zipCode": zip_code,
            "date": date.strftime("%Y-%m-%dT00-0000"),
            "distance": "25",
            "API_KEY": API_KEY,
        }
        try:
            res = requests.get(BASE_URL, params=params)
            if res.status_code == 429:
                print("Rate limit hit unexpectedly. Sleeping for 10 minutes...")
                sleep(600)
                continue  # retry the same date
            res.raise_for_status()
            data = res.json()
            # Filter for desired parameters
            filtered = [d for d in data if d.get("ParameterName") in PARAMETERS]
            if filtered:
                all_data.extend(filtered)
        except Exception as e:
            print(f"[!] Error fetching {zip_code} for {date.date()}: {e}")
        date += timedelta(days=1)
        request_count += 1
        sleep(1)  # 1 second between requests
    return all_data


def store_to_sqlite(data):
    if not data:
        print("No data to store.")
        return
    df = pd.DataFrame(data)
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        conn = sqlite3.connect(DB_FILE)
        df.to_sql("air_quality_measurements", conn, if_exists="replace", index=False)
        conn.close()
        print(f"DB created and data saved at {DB_FILE}")
        print(f"✅ Stored {len(df)} rows to DB.")
    except Exception as e:
        print(f"Error writing to DB: {e}")


def main():
    start_time = time()
    for zip_code in ZIP_CODES:
        for year in range(START_DATE.year, END_DATE.year + 1):
            year_start = datetime(year, 1, 1)
            year_end = datetime(year, 12, 31)
            # Clamp to overall start/end
            if year == START_DATE.year:
                year_start = START_DATE
            if year == END_DATE.year:
                year_end = END_DATE
            print(f"\n📦 Fetching data for ZIP: {zip_code}, Year: {year}")
            data = fetch_airnow_data(zip_code, year_start, year_end)
            print(f"   ↳ {len(data)} records fetched for {zip_code} in {year}")
            store_to_sqlite(data)  # Or save to a CSV per ZIP/year
    print(f"\n🏁 Done in {round(time() - start_time, 2)} seconds.")


if __name__ == "__main__":
    main()
