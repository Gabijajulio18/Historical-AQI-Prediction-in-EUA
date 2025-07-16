import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.features_pipeline import features_data_pipeline


def test_features_data_pipeline_creates_columns():
    data = {
        'Date Local': ['2016-01-01', '2016-01-02'],
        'NO2 Mean': [10, 12],
        'O3 Mean': [20, 21],
        'SO2 Mean': [5, 6],
        'CO Mean': [0.4, 0.5],
        'Site Num': [1, 1],
    }
    df = pd.DataFrame(data)
    result = features_data_pipeline(df)
    expected_cols = {
        'year', 'month', 'day', 'weekday', 'is_weekend',
        'NO2_to_SO2', 'CO_to_SO2', 'O3_to_CO',
        'NO2 Mean_roll_3', 'O3 Mean_roll_3',
        'SO2 Mean_roll_3', 'CO Mean_roll_3'
    }
    assert expected_cols.issubset(result.columns)
