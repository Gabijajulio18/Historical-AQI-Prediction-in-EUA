import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels as sm


@st.cache_data
def load_data():
    y_true = np.load("./models/preds/y_val.npy")
    y_pred = np.load("./models/preds/y_val_pred.npy")
    pollutants = ["NO2 AQI", "O3 AQI", "SO2 AQI", "CO AQI"]
    df = pd.DataFrame(y_true, columns=[f"{p} True" for p in pollutants])
    for i, p in enumerate(pollutants):
        df[f"{p} Pred"] = y_pred[:, i]
    return df, pollutants


df, pollutants = load_data()

st.title("AQI Prediction Dashboard")

for p in pollutants:
    fig = px.scatter(
        df,
        x=f"{p} True",
        y=f"{p} Pred",
        trendline="ols",
        labels={f"{p} True": "Actual", f"{p} Pred": "Predicted"},
        title=f"{p} - Actual vs Predicted",
    )
    # Add actual values as a separate trace (e.g., diagonal line for reference)
    fig.add_scatter(
        x=df[f"{p} True"],
        y=df[f"{p} True"],
        mode="lines",
        name="Ideal (True = Pred)",
        line=dict(color="green", dash="dash"),
    )
    st.plotly_chart(fig, use_container_width=True)
