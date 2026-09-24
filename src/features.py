import pandas as pd


FEATURE_COLUMNS = [
    "estimated_delivery_days",
    "item_count",
    "total_items_price",
    "total_freight_value",
    "unique_products",
    "unique_sellers",
    "payment_count",
    "total_payment_value",
    "payment_types",
    "max_installments",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",
    "purchase_year",
    "purchase_month",
    "purchase_dayofweek",
    "purchase_hour",
]


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["purchase_dt"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    df["estimated_delivery_dt"] = pd.to_datetime(
        df["order_estimated_delivery_date"]
    )

    df["estimated_delivery_days"] = (
        df["estimated_delivery_dt"] - df["purchase_dt"]
    ).dt.total_seconds() / (24 * 3600)

    df["purchase_hour"] = df["purchase_dt"].dt.hour
    df["purchase_year"] = df["purchase_dt"].dt.year
    df["purchase_month"] = df["purchase_dt"].dt.month
    df["purchase_dayofweek"] = df["purchase_dt"].dt.dayofweek

    return df[FEATURE_COLUMNS]