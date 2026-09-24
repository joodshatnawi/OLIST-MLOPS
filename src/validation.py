import pandas as pd
import great_expectations as gx

REQUIRED_COLUMNS = [
    "order_purchase_timestamp",
    "order_estimated_delivery_date",
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
]

def validate_with_great_expectations(df: pd.DataFrame) -> None:
    context = gx.get_context()

    data_source = context.data_sources.add_pandas(
        name="pandas_source"
    )

    data_asset = data_source.add_dataframe_asset(
        name="input_data"
    )

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "whole_dataframe"
    )

    batch = batch_definition.get_batch(
        batch_parameters={"dataframe": df}
    )

    validator = context.get_validator(
        batch=batch
    )

    validator.expect_table_columns_to_match_set(
        column_set=REQUIRED_COLUMNS,
        exact_match=False,
    )

    for column in REQUIRED_COLUMNS:
        validator.expect_column_values_to_not_be_null(
            column=column
        )

    numeric_columns = [
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
    ]

    for column in numeric_columns:
        validator.expect_column_values_to_be_in_type_list(
            column=column,
            type_list=["int64", "float64"],
        )



    non_negative_columns = [
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
    ]

    for column in non_negative_columns:
        validator.expect_column_values_to_be_between(
            column=column,
            min_value=0,
        )

    result = validator.validate()

    if not result.success:
        raise ValueError(
            "Great Expectations validation failed."
        )

def validate_input(df: pd.DataFrame) -> None:
    validate_with_great_expectations(df)

    try:
        pd.to_datetime(df["order_purchase_timestamp"])
        pd.to_datetime(df["order_estimated_delivery_date"])
    except (ValueError, TypeError):
        raise ValueError("Invalid date or timestamp format.")
