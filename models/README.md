# Models Directory

This folder contains artifacts generated during model training. These are used to evaluate model performance and support inference workflows.

## Contents

- **`aqi_model.keras`**  
  The trained deep learning model saved in Keras `.keras` format.  
  Used for AQI predictions in scripts like `predict_aqi.py` or when deployed via FastAPI.

- **`training_history.pkl`**  
  A serialized Python object (typically from `model.fit()` in Keras) containing training and validation loss/metrics over epochs.  
  Useful for plotting learning curves or comparing training runs.

## When Are These Files Created?

They are saved automatically when running:

```bash
python src/model_train.py
```