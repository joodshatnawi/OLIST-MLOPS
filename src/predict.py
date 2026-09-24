import json
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
import os

from src.features import create_features


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.json"


with open(CONFIG_PATH, "r") as f:
    config = json.load(f)


THRESHOLD = config["prediction"]["threshold"]
MODEL_VERSION = config["model"]["version"]

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    config["mlflow"]["tracking_uri"]
)
MODEL_NAME = config["mlflow"]["model_name"]
MODEL_ALIAS = config["mlflow"]["model_alias"]


mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

MODEL_URI = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"

model = None


def load_model():
    global model

    if model is None:
        model = mlflow.sklearn.load_model(MODEL_URI)

    return model

def predict(df: pd.DataFrame) -> pd.DataFrame:
    features = create_features(df)

    loaded_model = load_model()
    probability = loaded_model.predict_proba(features)[:, 1]    
    prediction = (probability >= THRESHOLD).astype(int)

    return pd.DataFrame({
        "late_probability": probability,
        "predicted_late": prediction,
        "model_version": MODEL_VERSION
    })