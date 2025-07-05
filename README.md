⚠️ Although this project uses a static dataset, code is included to support future data fetching from the OpenAQ API — currently disabled due to rate limits and long request times for historical data. Using a local dataset from Kaggle accelerates development and makes this project reproducible.

# Estimating Missing AQI Values for SO₂ and CO

## 📌 Background

During our exploratory data analysis of the [US Pollution Dataset](https://www.kaggle.com/datasets/sogun3/uspollution), we observed a consistent issue:

- **Over 50% of the AQI values for SO₂ and CO are missing**, even though the corresponding pollutant concentrations (`Mean`, `1st Max Value`, etc.) are available.

## 🔍 Problem Description

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

## 💡 Solution: Estimate AQI Using EPA Breakpoints

To address this, we are implementing a function that:

- Uses **EPA AQI breakpoint tables** to **recalculate the AQI** for SO₂ and CO from their corresponding mean concentration values.
- Ensures consistency with officially defined AQI ranges and pollutant-specific formulas.
- Produces a **complete AQI dataset**, allowing for fair comparisons and more accurate visualizations/forecasts.

We will apply these functions to fill in missing AQI values for SO₂ and CO where pollutant concentration data is available.

## ✅ Benefits

- Enables forecasting and modeling using AQI as a target variable.
- Maintains the integrity of time series and spatial analyses.
- Provides transparency and consistency in how AQI values are handled across the dataset.

---
✅ 1. NO₂ AQI

    Trend: The model follows the diagonal quite well, especially in the 0–60 AQI range.

    Bias: There is underestimation for higher NO₂ AQI values (>70).

    Outliers: A few predictions are way off (~100+ actuals with ~30 predicted).

    Conclusion: Reasonable performance; underprediction at higher levels suggests the model might need help capturing extreme pollution.

✅ 2. O₃ AQI

    Trend: Good alignment for 0–100 AQI. Beyond that, predictions become more dispersed.

    Bias: Again, underprediction for higher AQI values (>120).

    Density: Large volume of predictions in the 30–100 actual range, suggesting many test examples lie there.

    Conclusion: Acceptable performance, but high O₃ levels are underestimated — possibly due to class imbalance or data sparsity at the high end.

✅ 3. SO₂ AQI

    Trend: The model performs very well at low AQI levels (0–40).

    Bias: Strong underprediction for mid-to-high range (60–100+), and a strange band of low predictions for high actuals.

    Conclusion: Model likely learned a low variance pattern — this could mean:

        Not enough high SO₂ samples

        Over-regularized / underfitting

✅ 4. CO AQI

    Trend: Tight cluster, mostly below 30 AQI.

    Bias: Slight underprediction but minimal.

    Conclusion: Model performs best here. Low variance and low MAE likely reflect easier predictability or more consistent data patterns.