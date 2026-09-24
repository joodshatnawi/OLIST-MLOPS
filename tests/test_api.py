import numpy as np
from fastapi.testclient import TestClient

from app.main import app
import src.predict as predict_module


client = TestClient(app)


class FakeModel:
    def predict_proba(self, features):
        return np.array([
            [0.3, 0.7]
        ] * len(features))


def get_payload():
    return {
        "order_purchase_timestamp": "2018-01-01 10:00:00",
        "order_estimated_delivery_date": "2018-01-05",
        "item_count": 2,
        "total_items_price": 100.0,
        "total_freight_value": 20.0,
        "unique_products": 2,
        "unique_sellers": 1,
        "payment_count": 1,
        "total_payment_value": 120.0,
        "payment_types": 1,
        "max_installments": 2,
        "customer_zip_code_prefix": 12345,
        "customer_city": "Sao Paulo",
        "customer_state": "SP",
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "healthy"
    assert "model_version" in result


def test_model_endpoint():
    response = client.get("/model")

    assert response.status_code == 200

    result = response.json()

    assert result["model_version"] == "1.0.0"
    assert result["model_type"] == "LogisticRegression"


def test_predict_endpoint(monkeypatch):
    monkeypatch.setattr(
        predict_module,
        "load_model",
        lambda: FakeModel()
    )

    payload = get_payload()

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "late_probability" in result
    assert "predicted_late" in result
    assert "model_version" in result

    assert 0 <= result["late_probability"] <= 1
    assert result["predicted_late"] in [0, 1]


def test_batch_predict_endpoint(monkeypatch):
    monkeypatch.setattr(
        predict_module,
        "load_model",
        lambda: FakeModel()
    )

    payload = {
        "orders": [
            get_payload(),
            get_payload(),
        ]
    }

    response = client.post("/predict/batch", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "predictions" in result
    assert len(result["predictions"]) == 2

    for prediction in result["predictions"]:
        assert "late_probability" in prediction
        assert "predicted_late" in prediction
        assert "model_version" in prediction


def test_invalid_payload():
    payload = get_payload()

    del payload["customer_state"]

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_rejects_negative_item_count():
    payload = get_payload()
    payload["item_count"] = -1

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
    assert "Great Expectations validation failed" in response.json()["detail"]


def test_predict_rejects_invalid_numeric_type():
    payload = get_payload()
    payload["item_count"] = "two"

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_batch_predict_rejects_negative_item_count():
    payload = {
        "orders": [
            get_payload(),
            get_payload(),
        ]
    }

    payload["orders"][0]["item_count"] = -1

    response = client.post("/predict/batch", json=payload)

    assert response.status_code == 422
    assert "Great Expectations validation failed" in response.json()["detail"]