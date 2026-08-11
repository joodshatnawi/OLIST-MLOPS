import pandas as pd 
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://olist:olist123@localhost:5432/olist")

df=pd.read_csv(r"C:\Users\USER\Desktop\olist-mlops\data\olist_orders_dataset.csv")

print("Rows:",len(df))
print("Columns:",df.columns.to_list())

df.to_sql("orders",engine,if_exists="replace",index=False)
print("Orders table loaded successfully!")