import os
import json
import datetime
from dateutil import parser
from pymongo import MongoClient
from google.cloud import bigquery

# Environment variables configured in Google Cloud Function
MONGO_URI = os.environ.get("MONGO_URI", "")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "jompoi_db")
BQ_PROJECT_ID = os.environ.get("GCP_PROJECT", os.environ.get("BQ_PROJECT_ID", ""))
BQ_DATASET_ID = os.environ.get("BQ_DATASET_ID", "jompoi_reporting")

COLLECTIONS_TO_SYNC = [
    "customers",
    "items",
    "sales_invoice",
    "purchase_invoice",
    "stock_ledger"
]

def flatten_document(doc):
    flat = {}
    if "_id" in doc:
        flat["_id"] = str(doc["_id"])
        
    for k, v in doc.items():
        if k == "_id":
            continue
        if isinstance(v, dict):
            # Flatten nested customer object as per client requirement
            if k == "customer":
                flat["customer_name"] = v.get("name")
                flat["customer_city"] = v.get("city")
            else:
                for sub_k, sub_v in v.items():
                    flat[f"{k}_{sub_k}"] = str(sub_v) if isinstance(sub_v, dict) else sub_v
        elif isinstance(v, datetime.datetime):
            flat[k] = v.isoformat()
        else:
            flat[k] = v
    return flat

def sync_to_bigquery(request):
    """
    Cloud Function HTTP Entry Point.
    Triggered via HTTP request or Cloud Scheduler.
    """
    if not MONGO_URI:
        return ("Error: MONGO_URI environment variable is missing", 500)

    try:
        mongo_client = MongoClient(MONGO_URI)
        mongo_db = mongo_client[MONGO_DB_NAME]
        bq_client = bigquery.Client(project=BQ_PROJECT_ID)
    except Exception as e:
        return (f"Connection failed: {str(e)}", 500)

    results = {}

    for collection_name in COLLECTIONS_TO_SYNC:
        coll = mongo_db[collection_name]
        # Query all records or modified records
        cursor = coll.find({})
        
        rows = []
        for doc in cursor:
            rows.append(flatten_document(doc))

        if not rows:
            results[collection_name] = "0 rows found"
            continue

        # Map collection name to BQ table name (e.g. sales_invoice -> sales)
        table_name = "sales" if collection_name == "sales_invoice" else collection_name
        table_id = f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.{table_name}"

        try:
            errors = bq_client.insert_rows_json(table_id, rows)
            if not errors:
                results[collection_name] = f"Successfully inserted {len(rows)} rows into {table_name}"
            else:
                results[collection_name] = f"BQ Insert Errors: {errors}"
        except Exception as e:
            results[collection_name] = f"Error: {str(e)}"

    return (json.dumps(results, indent=2), 200, {"Content-Type": "application/json"})
