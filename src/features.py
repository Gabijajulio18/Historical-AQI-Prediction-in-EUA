import pandas as pd


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df["Date Local"] = pd.to_datetime(df["Date Local"])
    df["year"] = df["Date Local"].dt.year
    df["month"] = df["Date Local"].dt.month
    df["day"] = df["Date Local"].dt.day
    df["weekday"] = df["Date Local"].dt.weekday
    df["is_weekend"] = df["weekday"].isin([5, 6]).astype(int)
    return df


def add_pollutant_interactions(df: pd.DataFrame) -> pd.DataFrame:
    df["NO2_to_SO2"] = df["NO2 Mean"] / (df["SO2 Mean"] + 1e-6)
    df["CO_to_SO2"] = df["CO Mean"] / (df["SO2 Mean"] + 1e-6)
    df["O3_to_CO"] = df["O3 Mean"] / (df["CO Mean"] + 1e-6)
    return df


def add_rolling_means(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    df = df.sort_values(by="Date Local")
    pollutants = ["NO2 Mean", "O3 Mean", "SO2 Mean", "CO Mean"]
    for pollutant in pollutants:
        df[f"{pollutant}_roll_{window}"] = df.groupby("Site Num")[pollutant].transform(
            lambda x: x.rolling(window, min_periods=1).mean()
        )
    return df


def features_pipeline(df: pd.DataFrame, rolling_window: int = 3) -> pd.DataFrame:
    df = add_time_features(df)
    df = add_pollutant_interactions(df)
    df = add_rolling_means(df, rolling_window)
    return df
