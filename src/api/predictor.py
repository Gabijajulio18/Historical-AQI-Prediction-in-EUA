import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model


MODEL_PATH = "../models/best_aqi_model.keras"

X_cols = [
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

# Load model
model = load_model(MODEL_PATH)


def predict_aqi_from_df(df: pd.DataFrame) -> np.ndarray:
    # Ensure input order matches training columns
    input_data = df[X_cols].values
    print(input_data.shape)
    preds = model.predict(input_data)

    return preds
