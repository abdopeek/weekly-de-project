from pathlib import Path
from sqlalchemy import create_engine, text
import pandas as pd

base_dir = Path(__file__).parent.parent
db_user = "postgres"
db_pw = "123456789"
db_host = "localhost"
db_port = "5432"
db_name = "olist_db"
db_url = f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"


def run_analytics():
    engine = create_engine(db_url)

    # 1. Monthly Order Growth
    monthly_query = """
    SELECT 
        DATE_TRUNC('month', order_purchase_timestamp)::DATE AS order_month,
        COUNT(order_id) AS total_orders
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY 1
    ORDER BY 1 ASC;
    """

    # 2. Delivery SLA Analysis (Late Deliveries)
    sla_query = """
    SELECT 
        COUNT(order_id) AS total_delivered,
        SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 ELSE 0 END) AS late_deliveries,
        ROUND(
            (SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 ELSE 0 END)::NUMERIC / COUNT(order_id)) * 100, 2
        ) AS late_delivery_pct
    FROM orders
    WHERE order_status = 'delivered';
    """

    print("--- Monthly Order Volume ---")
    df_monthly = pd.read_sql(monthly_query, con=engine)
    print(df_monthly.head(10))
    print("\n--- Delivery SLA Metrics ---")
    df_sla = pd.read_sql(sla_query, con=engine)
    print(df_sla)


if __name__ == "__main__":
    run_analytics()