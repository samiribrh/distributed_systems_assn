import joblib
import pandas as pd

# Model loading function
def load_model(model_path):
    with open(model_path, "rb") as f:
        model = joblib.load(f)
    return model

# Prediction function
def predict(model, request):
    """
    Expects request as a dict with the same structure as used for model input in training.
    """
    data = request["data"]
    # Encode status as in training
    status_map = {"submitted": 0, "accepted": 1, "rejected": 2}
    # For timestamp, convert to unix timestamp as in training
    timestamp = pd.to_datetime(data["timestamp"]).value / 10**9
    # Order must match what model expects
    features = [
        timestamp,
        status_map[data["status"]],
        data["vendor_id"],
        data["amount"]
    ]

    prediction = model.predict([features])[0]
    return {
        "transaction_id": request["transaction_id"],
        "prediction": int(prediction)
    }
