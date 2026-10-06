from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from ingest import load_raw_dataset

base_dir = Path(__file__).resolve().parent.parent

db_user = "postgres"
db_pw = '123456789'
db_host = "localhost"
db_port = "5432"
db_name = "olist_db"
db_url = f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"

# due to foreign keys, load tables in a specific order
table_load_order = [
    "customers", "products", "sellers", "orders" ,"order_items", "order_payments", "order_reviews"
]

def load_all_datasets():
    engine = create_engine(db_url)
    print("Starting ingestion and loading pipeline 1/3")

    for table in table_load_order:
        print(f"--> Ingesting dataset: {table}")
        df = load_raw_dataset(table)

        print(f"--> Loading {len(df):,} rows into postgers")

        df.to_sql(
            name=table,
            con=engine,
            if_exists="append",
            index=False,
            chunksize=2000,
            method="multi"
        )
        print(f"Successfully loaded '{table}'")
    print("Pipeline ingestion complete, all datasets loaded")

if __name__ == "__main__":
    load_all_datasets()