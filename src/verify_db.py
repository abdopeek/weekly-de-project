from pathlib import Path
from sqlalchemy import create_engine, text

db_user = "postgres"
db_pw = "123456789"
db_host = "localhost"
db_port = "5432"
db_name = "olist_db"

db_url = f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"
tables = ["customers", "orders", "order_reviews", "order_items", "products", "sellers", "order_payments"]

def verify_db():
    engine = create_engine(db_url)
    with engine.connect() as conn:
        for table in tables:
            query = f"SELECT COUNT(*) FROM {table}"
            result = conn.execute(text(query))
            print(f"Table {table} has {result.fetchone()[0]} columns")

if __name__ == "__main__":
    verify_db()