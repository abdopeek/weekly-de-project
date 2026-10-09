
# Brazilian E-Commerce (Olist) Data Engineering Pipeline

A reproducible, idempotent Data Engineering pipeline that ingests raw e-commerce transaction data, enforces explicit date/schema types, models a normalized relational database in PostgreSQL, and exposes business analytics.

---

## 🏗️ Architecture & Data Flow

```text
  [ Raw Layer ]           [ Transformation ]             [ Storage ]             [ Consumption ]
Olist CSV Datasets  --->  src/ingest.py            --->  PostgreSQL (olist_db) --->  src/analytics.py
(data/raw/*.csv)          • Type Casting                   • Star/Snowflake            • SLA Metrics
                          • Header Sanitization            • PK/FK Constraints         • Monthly Volume
                                 │                               │
                                 ▼                               │
                          src/load_data.py  ───────────────┘
                          • Idempotent Deduplication
                          • Tuple Masking (Composite PKs)
                                 │
                                 ▼
                          src/main.py (Orchestrator) & logs/pipeline.log

```

---

## 💡 Key Design Decisions & Engineering Trade-Offs

1. **Immutable Raw Layer:** Raw CSV datasets in `data/raw/` are treated as read-only. Ingestion transformations (e.g., datetime parsing for orders) occur in-memory using Pandas during load execution.
2. **Normalized Relational Schema:** Tables are organized with explicit `PRIMARY KEY` and `FOREIGN KEY` constraints in PostgreSQL (`schema.sql`). Foreign key dependency order is enforced during insertion.
3. **Idempotency via In-Memory Key Masking:**
* Standard `if_exists="append"` in `df.to_sql()` raises `UniqueViolation` errors on retries.
* To prevent duplicate inserts without wiping the database, `src/load_data.py` queries existing keys before insertion.
* **Single Primary Keys:** Checked using constant-time $O(1)$ set lookups (`df[~df[pk].isin(existing_keys)]`).
* **Composite Primary Keys:** Evaluated using tuple pairs (e.g., `(order_id, order_item_id)`) matched against existing tuple sets to prevent composite key collisions.


4. **Structured Logging & Orchestration:** Replaced raw `print()` statements with Python's native `logging` module (`logs/pipeline.log`) for auditability. Managed via `src/main.py` as a single execution entry point.

---

## 📊 Business Analytics Findings

Queries executed via `src/analytics.py` over the populated PostgreSQL warehouse yielded key operational insights:

* **Total Volume Processed:** 99,441 unique orders and 112,650 order items across 7 relational tables.
* **Delivery SLA Breach Rate:** **8.11%** of delivered orders (`7,826` out of `96,478`) breached their estimated delivery date (`order_delivered_customer_date > order_estimated_delivery_date`).
* **Growth Trend:** Monthly transaction volume grew consistently from ~265 orders in October 2016 to over 3,800 monthly orders in mid-2017.

---

## 📂 Repository Structure

```text
weekly-de-project/
├── data/
│   └── raw/                # Olist raw CSV files
├── logs/
│   └── pipeline.log        # Timestamped audit logs
├── src/
│   ├── analytics.py        # SQL queries for business metrics
│   ├── ingest.py           # CSV loading & timestamp type enforcement
│   ├── init_db.py          # DDL execution & schema creation
│   ├── load_data.py        # Idempotent database loader
│   ├── main.py             # Pipeline orchestrator (Entry point)
│   ├── schema.sql          # Relational DDL (PKs, FKs, constraints)
│   └── verify_db.py        # Row count auditor
├── README.md               # Architecture documentation
└── requirements.txt        # Python dependencies

```

---

## 🚀 Quickstart & Setup

### 1. Prerequisites

* Python 3.10+
* PostgreSQL server running locally on port `5432`
* Target database created: `olist_db`

### 2. Environment Setup

Clone the repository and install required dependencies:

```bash
git clone [https://github.com/abdopeek/weekly-de-project.git](https://github.com/abdopeek/weekly-de-project.git)
cd weekly-de-project
pip install -r requirements.txt

```

### 4. Execute the End-to-End Pipeline

Run the full orchestration flow via `src/main.py`:

```bash
python src/main.py

```

To wipe and re-initialize the PostgreSQL schema prior to loading, pass `reset_first=True` inside `src/main.py` or execute:

```bash
python src/init_db.py
python src/main.py

```

### 5. Inspect Audit Logs & Run Analytics

View step-by-step pipeline execution logs:

```bash
cat logs/pipeline.log

```

Run analytical reports directly against PostgreSQL:

```bash
python src/analytics.py

```

```