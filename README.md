#  Historical AQI Prediction in the USA

This project uses deep learning to predict historical Air Quality Index (AQI) values for four major pollutants — **NO₂**, **O₃**, **SO₂**, **CO** — based on environmental and temporal features, using official US EPA data from **2000–2016**.

---

## Project Overview

- **Data**: [US EPA air quality measurements (2000–2016)](https://www.kaggle.com/datasets/sogun3/uspollution)
- **Preprocessing**: Imputation, feature engineering, and normalization  
- **Model**: Deep Neural Network (Keras)  
- **Evaluation**: MAE per pollutant + visualizations  
- **API**: FastAPI server to serve model predictions *(planned)*  
- **Dockerized**: Full deployment container *(planned)*  

---

## Problem Statement

The goal is to predict AQI values for key pollutants using other pollutant concentrations and contextual variables (e.g., month, weekend, ratios). The model is trained on historical data and evaluated on a held-out test set.

---

### Estimating Missing AQI Values for SO₂ and CO

####  Background

During our exploratory data analysis of the [US Pollution Dataset](https://www.kaggle.com/datasets/sogun3/uspollution), I observed a consistent issue:

- **Over 50% of the AQI values for SO₂ and CO are missing**, even though the corresponding pollutant concentrations (`Mean`, `1st Max Value`, etc.) are available.

###  Problem Description

While NO₂ and O₃ AQI values are fully present, SO₂ and CO AQI values show the following characteristics:

- The **raw pollutant data is present** — sensors have collected `SO2 Mean`, `CO Mean`, etc.
- However, the **AQI values themselves are missing** in about **half the rows**.
- The missingness appears **systematic**, not random:
  - It affects the same percentage of data per state, site, and date.
  - This likely suggests **AQI was not computed** or stored in the original dataset.

This poses a problem if we intend to:
- Compare AQI across pollutants,
- Forecast AQI for SO₂ and CO,
- Build dashboards using AQI data.

### Solution: Estimate AQI Using EPA Breakpoints

To address this, I've implemented a function that:

- Uses **EPA AQI breakpoint tables** to **recalculate the AQI** for SO₂ and CO from their corresponding mean concentration values.
- Ensures consistency with officially defined AQI ranges and pollutant-specific formulas.
- Produces a **complete AQI dataset**, allowing for fair comparisons and more accurate visualizations/forecasts.

We will apply these functions to fill in missing AQI values for SO₂ and CO where pollutant concentration data is available.

### Benefits

- Enables forecasting and modeling using AQI as a target variable.
- Maintains the integrity of time series and spatial analyses.
- Provides transparency and consistency in how AQI values are handled across the dataset.

---

## Project Structure

```
Historical-AQI-Prediction-in-EUA/
├── data/ # Raw and processed data 
│ ├── raw/ # Raw EPA data files
│ └── processed/ # Cleaned + transformed datasets 
│ 
├── models/ # Saved models and preprocessing artifacts 
│ 
├── notebooks/ # EDA and model development notebooks 
│ 
├── src/ # Source code
│ ├── api/ # FastAPI app
│ │   ├── main.py
│ │   ├── predictor.py
│ │   ├── schema.py
│ │   └── sample_payload.json
│ ├── pipelines/ # Data cleaning and feature engineering
│ │   ├── clean_pipeline.py
│ │   └── features_pipeline.py
│ ├── training/ # Model training
│ │   └── model_train.py
│ ├── scripts/ # Command line utilities
│ │   ├── data_pipeline.py
│ │   ├── generate_sample_input.py
│ │   └── predict_aqi.py
│ └── utils.py # Shared helper functions
│ 
├── Dockerfile # Docker image definition (WIP) 
├── requirements.txt # Python dependencies 
├── README.md # This file 
└── .gitignore
```

---

## Features

- **Feature Engineering**: pollutant ratios, rolling means, weekend flags  
- **Deep Learning Model**: MLP with dropout, batch norm, L2 regularization  
- **Evaluation Metrics**: MAE for each pollutant and overall  
- **Visualizations**: True vs predicted AQI plots  
- **API Ready**: FastAPI endpoint for real-time inference *(WIP)*  
- **Docker Deployment** *(WIP)*  

---

## Model Performance

| Pollutant | MAE   |
|-----------|-------|
| NO₂       | 3.32  |
| O₃        | 6.52  |
| SO₂       | 1.06  |
| CO        | 0.70  |
| **Overall** | **2.90** |

---

###  NO₂ AQI

**Trend**: The model follows the diagonal quite well, especially in the 0–60 AQI range.

**Bias**: There is underestimation for higher NO₂ AQI values (>70).

**Outliers**: A few predictions are way off (~100+ actuals with ~30 predicted).

**Conclusion**: Reasonable performance; underprediction at higher levels suggests the model might need help capturing extreme pollution.

---
###  O₃ AQI

**Trend**: Good alignment for 0–100 AQI. Beyond that, predictions become more dispersed.

**Bias**: Again, underprediction for higher AQI values (>120).

**Density**: Large volume of predictions in the 30–100 actual range, suggesting many test examples lie there.

**Conclusion**: Acceptable performance, but high O₃ levels are underestimated — possibly due to class imbalance or data sparsity at the high end.

---
### SO₂ AQI

**Trend**: The model performs very well at low AQI levels (0–40)

**Bias**: Strong underprediction for mid-to-high range (60–100+), and a strange band of low predictions for high actuals.

**Conclusion**: Model likely learned a low variance pattern — this could mean:
- Not enough high SO₂ samples
- Over-regularized / underfitting

---
### CO AQI

**Trend**: Tight cluster, mostly below 30 AQI.

**Bias**: Slight underprediction but minimal.

**Conclusion**: Model performs best here. Low variance and low MAE likely reflect easier predictability or more consistent data patterns.

---
## Overall Conclusion

Strong performance on low-to-mid AQI values.
Consistent underestimation at higher AQIs, especially for NO₂, O₃, and SO₂.
CO predictions are strong — likely due to lower variance or better signal in data.

---

## Getting Started
```bash
git clone https://github.com/Gabijajulio18/Historical-AQI-Prediction-in-EUA.git
cd Historical-AQI-Prediction-in-EUA
```

---

### Install dependencies
```bash
pip install -r requirements.txt
```

---

### Preprocess the data
```bash
python src/scripts/data_pipeline.py
```

---

### Train the model
```bash
python src/training/model_train.py
```

---

### Predict from saved model (WIP)
```bash
python src/scripts/predict_aqi.py --input data/sample_input.csv
```

---

### Run the API (WIP)
```bash
uvicorn src.api.main:app --reload
```

---

### Run the Dashboard
```bash
streamlit run dashboard.py
```

---

### Run Tests
```bash
pytest
```

---

### Dockerize the App (WIP)
```bash
docker build -t aqi-api .
docker run -p 8000:8000 aqi-api
```

### Deploy with Docker Compose
```bash
docker compose up --build
```

---

## Next Steps

- Expand `predict_aqi.py` for batch inference
- Deploy the API using a cloud service (e.g. AWS, Render)
- Set up continuous integration for automated testing
