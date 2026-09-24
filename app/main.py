import logging
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

from src.predict import predict, MODEL_VERSION
from src.logging_config import setup_logging
from src.validation import validate_input

app = FastAPI(title="Olist ML API")
setup_logging()
logger = logging.getLogger(__name__)

class PredictionRequest(BaseModel):
    order_purchase_timestamp: str
    order_estimated_delivery_date: str
    item_count: int
    total_items_price: float
    total_freight_value: float
    unique_products: int
    unique_sellers: int
    payment_count: int
    total_payment_value: float
    payment_types: int
    max_installments: int
    customer_zip_code_prefix: int
    customer_city: str
    customer_state: str


class BatchPredictionRequest(BaseModel):
    orders: list[PredictionRequest]


@app.get("/")
def root():
    return {"message": "Olist ML API is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_version": MODEL_VERSION
    }


@app.get("/model")
def model_info():
    return {
        "model_version": MODEL_VERSION,
        "model_type": "LogisticRegression"
    }


@app.post("/predict")
def make_prediction(data: PredictionRequest):
    start_time = time.perf_counter()

    input_data = data.model_dump()
    df = pd.DataFrame([input_data])

    try:
        validate_input(df)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    result = predict(df)

    output = result.to_dict(orient="records")[0]

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "Prediction completed | input=%s | output=%s | latency_ms=%.2f | model_version=%s",
        input_data,
        output,
        latency_ms,
        MODEL_VERSION,
    )

    return output


@app.post("/predict/batch")
def make_batch_prediction(data: BatchPredictionRequest):
    start_time = time.perf_counter()

    input_data = [order.model_dump() for order in data.orders]
    df = pd.DataFrame(input_data)

    try:
        validate_input(df)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    result = predict(df)

    predictions = result.to_dict(orient="records")

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "Batch prediction completed | records=%d | latency_ms=%.2f | model_version=%s",
        len(predictions),
        latency_ms,
        MODEL_VERSION,
    )

    return {
        "predictions": predictions
    }
