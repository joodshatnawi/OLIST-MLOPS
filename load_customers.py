import pandas as pd 
from sqlalchemy import create_engine
# Connection to PostgreSQL
engine = create_engine("postgresql+psycopg2://olist:olist123@localhost:5432/olist")

# Read customers CSV
df=pd.read_csv(r"C:\Users\USER\Desktop\olist-mlops\data\olist_customers_dataset.csv")

print("Raws:",len(df))
print("Columns:",df.columns.to_list())

# Load into PostgreSQL
df.to_sql("customers",engine,if_exists="replace",index=False)

print("Customers table loaded successfully!")