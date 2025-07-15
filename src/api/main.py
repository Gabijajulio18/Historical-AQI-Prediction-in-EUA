from fastapi import FastAPI
from src.api.schema import AQIRequest
from src.api.predictor import predict_aqi_from_df
import pandas as pd

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
