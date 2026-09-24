import pandas as pd

from src.predict import predict


def test_predict():
    df = pd.DataFrame({
        "order_purchase_timestamp": [
            "2018-01-01 10:00:00"
        ],
        "order_estimated_delivery_date": [
            "2018-01-05"
        ],
        "item_count": [2],
        "total_items_price": [100.0],
        "total_freight_value": [20.0],
        "unique_products": [2],
        "unique_sellers": [1],
        "payment_count": [1],
        "total_payment_value": [120.0],
        "payment_types": [1],
        "max_installments": [2],
        "customer_zip_code_prefix": [12345],
        "customer_city": ["Sao Paulo"],
        "customer_state": ["SP"],
    })

    result = predict(df)

    assert "late_probability" in result.columns
    assert "predicted_late" in result.columns

    assert len(result) == 1

    assert 0 <= result.loc[0, "late_probability"] <= 1
    assert result.loc[0, "predicted_late"] in [0, 1]