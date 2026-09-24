import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://olist:olist123@localhost:5432/olist")

df = pd.read_csv(r"C:\Users\USER\Desktop\olist-mlops\data\olist_order_reviews_dataset.csv")
print("Rows:", len(df))
print("Columns:", df.columns.to_list())

df.to_sql(
    "orders_reviews",
    engine,
    if_exists="replace",
    index=False
)

print("orders_reviews table loaded successfully!")