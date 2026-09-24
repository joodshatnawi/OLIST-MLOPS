import json
import os
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "artifacts" / "final_model.joblib"
RESULTS_PATH = BASE_DIR / "artifacts" / "final_test_results.csv"
CONFIG_PATH = BASE_DIR / "config" / "config.json"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def load_test_metrics():
    results = pd.read_csv(RESULTS_PATH)

    row = results.iloc[0]

    metrics = {
        "accuracy": float(row["accuracy"]),
        "precision": float(row["precision"]),
        "recall": float(row["recall"]),
        "f1": float(row["f1"]),
        "roc_auc": float(row["roc_auc"]),
    }

    return metrics


def log_final_model():
    config = load_config()
    metrics = load_test_metrics()

    mlflow.set_tracking_uri(
        os.getenv(
            "MLFLOW_TRACKING_URI",
            "http://127.0.0.1:5000"
        )
    )

    client = mlflow.MlflowClient()

    model_name = config["mlflow"]["model_name"]
    model_alias = config["mlflow"]["model_alias"]

    # Check whether the champion alias already exists
    try:
        client.get_model_version_by_alias(
            name=model_name,
            alias=model_alias
        )
        print(
            f"Model '{model_name}' already has "
            f"alias '{model_alias}'."
        )
        print("MLflow initialization skipped.")
        return

    except Exception:
        pass

    mlflow.set_experiment("Olist Late Delivery")

    with mlflow.start_run(run_name="final_logistic_regression"):

        mlflow.log_params({
            "model_type": "LogisticRegression",
            "C": 0.01,
            "class_weight": "balanced",
            "max_iter": 1000,
            "random_state": 42,
            "threshold": config["prediction"]["threshold"],
        })

        mlflow.log_metrics(metrics)

        mlflow.log_artifact(
            str(RESULTS_PATH),
            artifact_path="evaluation"
        )

        mlflow.log_artifact(
            str(CONFIG_PATH),
            artifact_path="config"
        )

        model = joblib.load(MODEL_PATH)

        mlflow.sklearn.log_model(
            sk_model=model,
            name="final_model",
            serialization_format="pickle"
        )

        run_id = mlflow.active_run().info.run_id
        model_uri = f"runs:/{run_id}/final_model"

        registered_model = mlflow.register_model(
            model_uri=model_uri,
            name=model_name
        )

        client.set_registered_model_alias(
            name=model_name,
            alias=model_alias,
            version=registered_model.version
        )

        print("MLflow run completed successfully!")
        print("Metrics:", metrics)
        print(f"Registered model: {model_name}")
        print(f"Version: {registered_model.version}")
        print(f"Alias: {model_alias}")


if __name__ == "__main__":
    log_final_model()