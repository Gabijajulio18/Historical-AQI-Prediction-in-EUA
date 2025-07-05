import pandas as pd


def load_data() -> pd.DataFrame:
    data_path = "../data/processed/pollutants_with_features.csv"
    df = pd.read_csv(data_path, parse_dates="Date Local")
    return df


def time_series_split(
    df: pd.DataFrame,
    date_col: str = "Date Local",
    train_frac: float = 0.7,
    val_frac: float = 0.15,
):
    df = df.sort_values(by=date_col)
    n = len(df)
    train_end = int(n * train_frac)
    val_end = train_end + (int(n * val_frac))

    train = df.iloc[:train_end]
    val = df.iloc[train_end:val_end]
    test = df.iloc[val_end:]

    return train, val, test
