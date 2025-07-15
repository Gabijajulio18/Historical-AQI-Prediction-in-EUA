import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
import json

from utils import load_data, time_series_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    BatchNormalization,
    Input,
    Normalization,
)
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2


def main():
    # Load data
    df = load_data()

    # Feature / target split
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
    y_cols = ["NO2 AQI", "O3 AQI", "SO2 AQI", "CO AQI"]

    # Temporal split
    train_df, val_df, test_df = time_series_split(df)

    X_train, y_train = train_df[X_cols].values, train_df[y_cols].values
    X_val, y_val = val_df[X_cols].values, val_df[y_cols].values
    X_test, y_test = test_df[X_cols].values, test_df[y_cols].values

    print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

    with open("./data/test_df.pkl", "wb") as f:
        pickle.dump(test_df, f)

    # Normalizer
    normalizer = Normalization()
    normalizer.adapt(X_train)

    # Build model
    model = Sequential(
        [
            Input(shape=(X_train.shape[1],)),
            normalizer,
            Dense(256, activation="relu", kernel_regularizer=l2(1e-4)),
            BatchNormalization(),
            Dropout(0.4),
            Dense(128, activation="relu", kernel_regularizer=l2(1e-4)),
            BatchNormalization(),
            Dropout(0.4),
            Dense(64, activation="relu", kernel_regularizer=l2(1e-4)),
            Dense(4, activation="linear"),  # Linear output for 4 AQI predictions
        ]
    )

    model.compile(optimizer=Adam(1e-3), loss="mae", metrics=["mae"])

    # Callbacks
    early_stop = EarlyStopping(patience=5, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(patience=3, factor=0.2, min_lr=1e-6)

    checkpoint_cb = ModelCheckpoint(
        "./models/best_aqi_model.keras",
        save_best_only=True,
        monitor="val_loss",
        mode="min",
        verbose=1,
    )

    # Train
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=1024,
        callbacks=[early_stop, reduce_lr, checkpoint_cb],
        verbose=1,
    )

    # Predictions for training and validation
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)

    # Save predictions and true values to file
    np.save("./models/preds/y_train_pred.npy", y_train_pred)
    np.save("./models/preds/y_val_pred.npy", y_val_pred)
    np.save("./models/preds/y_train.npy", y_train)
    np.save("./models/preds/y_val.npy", y_val)
    model.save("./models/best_aqi_model.keras")
    with open("./models/X_cols.json", "w") as f:
        json.dump(X_cols, f)
    print(model.input_shape)

    return history


if __name__ == "__main__":
    history = main()

    with open("./models/training_history.pkl", "wb") as f:
        pickle.dump(history.history, f)
