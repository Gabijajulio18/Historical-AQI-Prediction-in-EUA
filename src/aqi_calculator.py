import pandas as pd
import numpy as np

# AQI breakpoints for SO2 (24-hour avg, ppb)
SO2_BREAKPOINTS = [
    (0, 35, 0, 50),
    (36, 75, 51, 100),
    (76, 185, 101, 150),
    (186, 304, 151, 200),
    (305, 604, 201, 300),
    (605, 804, 301, 400),
    (805, 1004, 401, 500),
]

# AQI breakpoints for CO (8-hour avg, ppm)
CO_BREAKPOINTS = [
    (0.0, 4.4, 0, 50),
    (4.5, 9.4, 51, 100),
    (9.5, 12.4, 101, 150),
    (12.5, 15.4, 151, 200),
    (15.5, 30.4, 201, 300),
    (30.5, 40.4, 301, 400),
    (40.5, 50.4, 401, 500),
]


def compute_aqi(
    concentration: float | None, breakpoints: list[tuple[float, float, int, int]]
) -> int | None:
    """Compute AQI from concentration based on EPA breakpoints"""

    for C_low, C_high, I_low, I_high in breakpoints:
        if C_low <= concentration <= C_high:
            return round(
                (I_high - I_low) / (C_high - C_low) * (concentration - C_low) + I_low
            )
        return np.nan  # Outside known range


def estimate_missing_aqi(df: pd.DataFrame) -> pd.DataFrame:
    """Estimate missing AQI value for SO2 and CO based on mean concentration"""

    df["SO2 AQI"] = df.apply(
        lambda row: (
            compute_aqi(row["SO2 Mean"], SO2_BREAKPOINTS)
            if pd.isna(row["SO2 AQI"]) and not pd.isna(row["SO2 Mean"])
            else row["SO2 AQI"]
        ),
        axis=1,
    )

    df["CO AQI"] = df.apply(
        lambda row: (
            compute_aqi(row["CO Mean"], CO_BREAKPOINTS)
            if pd.isna(row["CO AQI"]) and not pd.isna(row["CO Mean"])
            else row["CO AQI"]
        ),
        axis=1,
    )

    return df
