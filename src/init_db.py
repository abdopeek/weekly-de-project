from pathlib import Path
from sqlalchemy import create_engine, text

base_dir = Path(__file__).resolve().parent.parent
schema_file = base_dir / "src" / "schema.sql"

db_user = "postgres"
db_pw = "123456789"
db_host = "localhost"
db_port = "5432"
db_name = "olist_db"

db_url = f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"

def initialize_schema():
    engine = create_engine(db_url)

    with open(schema_file, "r") as file:
        sql_script = file.read()
    with engine.begin() as conn:
        conn.execute(text(sql_script))

    print("Database schema created")

if __name__ == "__main__":
    initialize_schema()
