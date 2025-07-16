from fastapi import FastAPI
from src.api.schema import AQIRequest
from src.api.predictor import predict_aqi_from_df
import pandas as pd
import json

with open("./models/X_cols.json", "r") as f:
    X_cols = json.load(f)

app = FastAPI()


@app.get("/")
def root():

    return {
        "message": "Historical AQI Prediction API is running",
        "endpoints": {
            "POST /predict": "Send air quality data to receive AQI predictions"
        },
        "example_payload": "/api/sample_payload.json",
    }


@app.post("/predict")
def predict(request: AQIRequest):

    df = pd.DataFrame([item.dict(by_alias=True) for item in request.data])

    df = df.reindex(columns=X_cols)

    preds = predict_aqi_from_df(df)

    results = [
        {
            "NO2 AQI": float(round(p[0], 2)),
            "O3 AQI": float(round(p[1], 2)),
            "SO2 AQI": float(round(p[2], 2)),
            "CO AQI": float(round(p[3], 2)),
        }
        for p in preds
    ]

    return {"predictions": results}
