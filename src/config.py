import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DUMMY_DATA_DIR = BASE_DIR / "dummy_data"

# MongoDB Config
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "jompoi_db")

# Google Cloud BigQuery Config
BQ_PROJECT_ID = os.environ.get("BQ_PROJECT_ID", "project-b6567b21-77eb-47fb-926")
BQ_DATASET_ID = os.environ.get("BQ_DATASET_ID", "jompoi_reporting")
BQ_LOCATION = os.environ.get("BQ_LOCATION", "US")

# State File Path
STATE_FILE = os.environ.get("STATE_FILE", str(BASE_DIR / "sync_state.json"))

# Collections & BigQuery Table Mapping
COLLECTION_TABLE_MAP = {
    "customers": "customers",
    "items": "items",
    "orders": "orders",
    "sales_invoice": "sales",
    "purchase_invoice": "purchases",
    "stock_ledger": "stock_ledger"
}

COLLECTIONS_TO_SYNC = list(COLLECTION_TABLE_MAP.keys())
