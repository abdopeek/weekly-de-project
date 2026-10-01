from pathlib import Path
import pandas as pd

base_dir = Path(__file__).resolve().parent.parent
raw_data_dir = base_dir / "data" / "raw"

date_time_columns = {
    "order_items": ["shipping_limit_date"],
    "order_reviews": ["review_answer_timestamp", "review_creation_date"],
    "orders": ["order_purchase_timestamp", "order_delivered_carrier_date", "order_delivered_customer_date",
               "order_estimated_delivery_date"]
}

def load_raw_dataset(dataset_name, data_dir=raw_data_dir):
    file_path = data_dir / f"olist_{dataset_name}_dataset.csv"

    if not file_path.exists():
        print("File path does not exist for dataset: " + dataset_name)

    parse_dates = date_time_columns.get(dataset_name, False)
    df = pd.read_csv(file_path, parse_dates=parse_dates)

    return df


print("Testing date parsing/ingestion for orders dataset")
orders_df = load_raw_dataset("orders")
print("Data types:")
print(orders_df.dtypes)
sample = orders_df["order_purchase_timestamp"].iloc[0]
print(f"Sample value: {sample} | Data type: {type(sample)}")