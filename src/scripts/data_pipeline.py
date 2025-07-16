import os
from src.pipelines.clean_pipeline import clean_data_pipeline
from src.pipelines.features_pipeline import features_data_pipeline


def ensure_dir_exists(path: str) -> None:
    """Ensure the directory for the given file path exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)


def main():
    input_path = "data/raw/pollution_us_2000_2016.csv"
    cleaned_path = "data/processed/cleaned_pollutants_sorted.csv"
    featured_path = "data/processed/pollutants_with_features.csv"
    pollutants = ["NO2 AQI", "O3 AQI", "SO2 AQI", "CO AQI"]

    # Clean the data and save to cleaned_path inside the pipeline
    df_cleaned = clean_data_pipeline(input_path, cleaned_path, pollutants)

    # Add features
    df_features = features_data_pipeline(df_cleaned)

    # Save featured data
    ensure_dir_exists(featured_path)
    df_features.to_csv(featured_path, index=False)

    print("Processing and feature engineering complete.")


if __name__ == "__main__":
    main()
