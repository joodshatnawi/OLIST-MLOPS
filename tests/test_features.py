import pandas as pd

from src.features import create_features, FEATURE_COLUMNS


def test_create_features():
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

    result = create_features(df)

    assert list(result.columns) == FEATURE_COLUMNS
    assert len(result) == 1


def test_feature_values():
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

    result = create_features(df)

    assert result.loc[0, "estimated_delivery_days"] == 3.5833333333333335
    assert result.loc[0, "purchase_year"] == 2018
    assert result.loc[0, "purchase_month"] == 1
    assert result.loc[0, "purchase_dayofweek"] == 0
    assert result.loc[0, "purchase_hour"] == 10
