import argparse
import pandas as pd
from tensorflow.keras.models import load_model

# Columns used during training
X_COLS = [
    "NO2 Mean",
    "O3 Mean",
    "SO2 Mean",
    "CO Mean",
    "SO2_Mean_Imputed",
    "CO_Mean_Imputed",
    "NO2_to_SO2",
    "CO_to_SO2",
    "O3_to_CO",
    "NO2 Mean_roll_3",
    "O3 Mean_roll_3",
    "SO2 Mean_roll_3",
    "CO Mean_roll_3",
    "year",
    "month",
    "is_weekend",
]


def predict(input_csv: str, model_path: str = "models/best_aqi_model.keras") -> None:
    # Load input CSV
    df = pd.read_csv(input_csv)

    if not set(X_COLS).issubset(df.columns):
        missing = set(X_COLS) - set(df.columns)
        raise ValueError(f"Missing columns in input: {missing}")

    # Extract features
    X = df[X_COLS].values

    # Load trained model (Includes build-in Normalization Layer)
    model = load_model(model_path)

    # Predicts
    preds = model.predict(X)

    # Format results
    pred_df = pd.DataFrame(preds, columns=["AQI_NO2", "AQI_O3", "AQI_SO2", "AQI_CO"])
    output_df = pd.concat([df.reset_index(drop=True), pred_df], axis=1)

    # Save
    output_path = input_csv.replace(".csv", "_predicted.csv")
    output_df.to_csv(output_path, index=False)
    print(f"Predictions saved to: {output_path}")
    print(output_df[["AQI_NO2", "AQI_O3", "AQI_SO2", "AQI_CO"]].head())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AQI predictions on new data")
    parser.add_argument(
        "--input", type=str, required=True, help="Path to input CSV file"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="models/best_aqi_model.keras",
        help="Path to model",
    )
    args = parser.parse_args()

    predict(args.input, args.model)
