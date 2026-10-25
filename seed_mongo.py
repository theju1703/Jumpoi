import os
import json
import argparse
from pathlib import Path
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent
DUMMY_DATA_DIR = BASE_DIR / "dummy_data"

COLLECTION_FILES = {
    "customers": "customers.json",
    "items": "items.json",
    "orders": "orders.json",
    "sales_invoice": "sales_invoice.json",
    "purchase_invoice": "purchase_invoice.json",
    "stock_ledger": "stock_ledger.json"
}

def seed_database(mongo_uri: str, db_name: str, drop_existing: bool = True):
    print(f"Connecting to MongoDB at {mongo_uri} (Database: {db_name})...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    try:
        # Test connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Ensure MongoDB service is running (e.g. via docker compose up -d or local mongod).")
        return False

    db = client[db_name]

    for collection_name, filename in COLLECTION_FILES.items():
        file_path = DUMMY_DATA_DIR / filename
        if not file_path.exists():
            print(f"[!] Warning: Data file {filename} not found. Skipping.")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        coll = db[collection_name]
        if drop_existing:
            coll.drop()

        if data:
            coll.insert_many(data)
            print(f"[OK] Seeded {len(data)} records into collection: '{collection_name}'")
        else:
            print(f"[--] Collection '{collection_name}' had 0 records.")

    print("\nDatabase seeding completed successfully!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed MongoDB with Jompoi grocery operational data.")
    parser.add_argument("--uri", default=os.environ.get("MONGO_URI", "mongodb://localhost:27017/"), help="MongoDB connection URI")
    parser.add_argument("--db", default=os.environ.get("MONGO_DB_NAME", "jompoi_db"), help="MongoDB database name")
    parser.add_argument("--no-drop", action="store_true", help="Do not drop existing collections before inserting")

    args = parser.parse_args()
    seed_database(args.uri, args.db, drop_existing=not args.no_drop)
