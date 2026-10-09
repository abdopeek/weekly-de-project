from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from ingest import load_raw_dataset
import logging

base_dir = Path(__file__).resolve().parent.parent
log_dir = base_dir / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "pipeline.log"),
        logging.StreamHandler() # prints log to terminal
    ]
)
logger = logging.getLogger("ETL_Loader")
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

pk_columns = {
    "customers": ("customer_id",),
    "products": ("product_id",),
    "sellers": ("seller_id",),
    "orders": ("order_id",),
    "order_items": ("order_id", "order_item_id"),
    "order_payments": ("order_id", "payment_sequential"),
    "order_reviews": ("review_id", "order_id")
}


def insert_new_records(df, table, pk_cols, engine):
    # get all keys already in the db
    cols_str = ", ".join(pk_cols)
    # get all new keys in the df
    try:
        existing_keys = (pd.read_sql(F"SELECT {cols_str} FROM {table}", con=engine))

    except Exception as e:
        logger.info(f"Error occurred while filtering new records for table '{table}': {e}")
        existing_keys = pd.DataFrame()


    if existing_keys.empty:
        logger.info(f"No existing records found in table '{table}'")
        new_records = df
    else:
        if len(pk_cols) == 1:
            pk = pk_cols[0]
            existing_keys_set = set(existing_keys[pk])
            new_records = df[~df[pk].isin(existing_keys_set)]
        else:
            existing_tuples = set(zip(*[existing_keys[col] for col in pk_cols]))
            incoming_tuples = zip(*[df[col] for col in pk_cols])
            mask = [tup not in existing_tuples for tup in incoming_tuples]
            new_records = df[mask]


    if new_records.empty:
        logger.info(f"No new records, leaving table '{table}' as is")
        return

    # return new records
    logger.info(f"Loading {len(new_records)} rows into postgres at table {table}")
    new_records.to_sql(
        name=table,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=2000,
        method="multi"
    )
    return


def load_all_datasets():
    engine = create_engine(db_url)
    logger.info("Starting loading stage of pipeline")

    for table in table_load_order:
        logger.info(f"Loading dataset: {table}")
        df = load_raw_dataset(table)
        
        insert_new_records(df, table, pk_columns[table], engine)
        logger.info(f"Successfully loaded {table} table")
    logger.info(f"Successfully ran loading level")

if __name__ == "__main__":
    load_all_datasets()