import pandas as pd


def load_data() -> pd.DataFrame:
    data_path = "../data/processed/pollutants_with_features.csv"
    df = pd.read_csv(data_path, parse_dates="Date Local")
    return df
