import pandas as pd
import os
from utils import estimate_missing_aqi
from sklearn.impute import SimpleImputer


input_path = "data/raw/pollution_us_2000_2016.csv"
output_path = "data/processed/cleaned_pollutants_sorted.csv"
pollutants = ["NO2 AQI", "O3 AQI", "SO2 AQI", "CO AQI"]


def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV file into a Dataframe."""
    return pd.read_csv(filepath)


def inspect_data(df: pd.DataFrame) -> None:
    """Print basic info and missing summary"""
    print(df.info())
    print("\nMissing values per column: \n", df.isnull().sum())
    print("\nDuplicated rows:", df.duplicated().sum())


def analyze_coverage_by_state(df: pd.DataFrame, pollutants: list[str]) -> None:
    """
    Analyze and print data coverage (non-missing ratio) per pollutant by state.
    This helps indentify if missing data is due to lack of measurements.
    """
    print("\nData coverage per pollutant by State (ratio of non-missing values:")
    coverage = df.groupby("State")[pollutants].apply(lambda x: x.notna().mean())
    print(coverage)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, handle missing dates, and sort by State and Date Local"""
    df = df.drop_duplicates()
    df["Date Local"] = pd.to_datetime(df["Date Local"], errors="coerce")
    df = df.sort_values(by=["State", "Date Local"])

    # Fill missing AQI values by estimation
    df = estimate_missing_aqi(df)
    return df


def clean_negative_concentrations(df: pd.DataFrame) -> pd.DataFrame:
    """Replace negative SO2 and CO concentrations with NaN."""
    df.loc[df["SO2 Mean"] < 0, "SO2 Mean"] = pd.NA
    df.loc[df["CO Mean"] < 0, "CO Mean"] = pd.NA
    return df


def impute_missing_aqi(df: pd.DataFrame) -> pd.DataFrame:
    df["SO2_Mean_Imputed"] = df["SO2 AQI"].isna().astype(int)
    df["CO_Mean_Imputed"] = df["CO AQI"].isna().astype(int)

    imputer = SimpleImputer(strategy="mean")
    df[["SO2 AQI", "CO AQI"]] = imputer.fit_transform(df[["SO2 AQI", "CO AQI"]])
    return df


def impute_missing_concentrations(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Input NaN values in specified concentration columns using mean strategy"""
    imputer = SimpleImputer(strategy="mean")
    df[columns] = imputer.fit_transform(df[columns])
    return df


def clean_data_pipeline(
    input_path: str, output_path: str, pollutants: list[str]
) -> None:
    df = load_data(input_path)
    inspect_data(df)
    analyze_coverage_by_state(df, pollutants)
    df = clean_negative_concentrations(df)
    df_cleaned = clean_data(df)
    df_cleaned = impute_missing_aqi(df_cleaned)
    # Impute concentrations after marking missingness
    concentration_cols = ["SO2 Mean", "CO Mean"]
    df_cleaned = impute_missing_concentrations(df_cleaned, concentration_cols)
    return df_cleaned
