from fastapi import FastAPI
from src.api.schema import AQIRequest
from src.api.predictor import predict_aqi_from_df
import pandas as pd

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

app = FastAPI()


@app.get("/")
def root():

    return {
        "message": "Historical AQI Prediction API is running",
        "endpoints": {
            "POST /predict": "Send air quality data to received AQI predictions"
        },
        "example_payload": "/api/sample_payload.json",
    }


@app.post("/predict")
def predict(request: AQIRequest):

    df = pd.DataFrame([item.model_dump(by_alias=True) for item in request.data])

    df = df.reindex(columns=X_cols)

    preds = predict_aqi_from_df(df)

    results = [
        {
            "N02 AQI": round(p[0], 2),
            "O3 AQI": round(p[1], 2),
            "SO2 AQI": round(p[2], 2),
            "CO AQI": round(p[3], 2),
        }
        for p in preds
    ]

    return {"predictions": results}
