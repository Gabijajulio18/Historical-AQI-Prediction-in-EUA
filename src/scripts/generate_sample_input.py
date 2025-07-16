import pandas as pd
import numpy as np
import os


def generate_sample_input_csv(
    output_path: str = "./data/sample_input.csv", num_rows: int = 5
) -> None:
    np.random.seed(42)

    # Generate base features
    data = {
        "NO2 Mean": np.random.uniform(5, 30, num_rows),
        "O3 Mean": np.random.uniform(10, 60, num_rows),
        "SO2 Mean": np.random.uniform(1, 8, num_rows),
        "CO Mean": np.random.uniform(0.2, 1.5, num_rows),
    }

    # Add engineered features
    data["SO2_Mean_Imputed"] = data["SO2 Mean"]
    data["CO_Mean_Imputed"] = data["CO Mean"]
    data["NO2_to_SO2"] = data["NO2 Mean"] / data["SO2 Mean"]
    data["CO_to_SO2"] = data["CO Mean"] / data["SO2 Mean"]
    data["O3_to_CO"] = data["O3 Mean"] / data["CO Mean"]
    data["NO2 Mean_roll_3"] = data["NO2 Mean"]
    data["O3 Mean_roll_3"] = data["O3 Mean"]
    data["SO2 Mean_roll_3"] = data["SO2 Mean"]
    data["CO Mean_roll_3"] = data["CO Mean"]
    data["year"] = np.random.choice(
        [2010, 2011, 2012, 2013, 2014, 2015, 2016], num_rows
    )
    data["month"] = np.random.randint(1, 13, num_rows)
    data["is_weekend"] = np.random.randint(0, 2, num_rows)

    # Define column order
    X_COLS = [
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

    df = pd.DataFrame(data)[X_COLS]

    # Save CSV
    df.to_csv(output_path, index=False)
    print(f"✅ Sample input saved to: {output_path}")
    print(df.head())


if __name__ == "__main__":
    generate_sample_input_csv()
