import numpy as np
import pandas as pd
import json
from tensorflow.keras.models import load_model

with open("./models/X_cols.json", "r") as f:
    X_cols = json.load(f)

MODEL_PATH = "../models/best_aqi_model.keras"


# Load model
model = load_model(MODEL_PATH)


def predict_aqi_from_df(df: pd.DataFrame) -> np.ndarray:
    # Ensure input order matches training columns
    input_data = df[X_cols].values
    print(input_data.shape)
    preds = model.predict(input_data)

    return preds
