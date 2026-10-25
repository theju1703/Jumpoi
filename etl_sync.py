import os
import sys
import json
import argparse
import datetime
import logging
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.config import (
    MONGO_URI, MONGO_DB_NAME, BQ_PROJECT_ID, BQ_DATASET_ID,
    STATE_FILE, COLLECTION_TABLE_MAP, COLLECTIONS_TO_SYNC, DUMMY_DATA_DIR
)
from src.etl.transformer import flatten_document, transform_records
from src.etl.sync_manager import SyncStateManager
from src.etl.bq_loader import BigQueryLoader

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("etl_sync")

def run_sync_for_collection(mongo_db, bq_loader, sync_manager, collection_name, dry_run=False, force_full=False):
    target_table = COLLECTION_TABLE_MAP.get(collection_name, collection_name)
    logger.info("--------------------------------------------------")
    logger.info("Syncing collection '%s' -> BigQuery table '%s'", collection_name, target_table)

    last_sync = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc) if force_full else sync_manager.get_last_sync_time(collection_name)
    sync_start = datetime.datetime.now(datetime.timezone.utc)
    logger.info("Last sync timestamp: %s", last_sync.isoformat())

    raw_docs = []
    if mongo_db is not None:
        try:
            coll = mongo_db[collection_name]
            query = {"updated_at": {"$gt": last_sync}} if not force_full else {}
            raw_docs = list(coll.find(query))
        except Exception as e:
            logger.error("Failed querying MongoDB for %s: %s", collection_name, e)
            return
    else:
        # Fallback to dummy data
        file_name = f"{collection_name}.json"
        json_path = DUMMY_DATA_DIR / file_name
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                raw_docs = json.load(f)
        else:
            logger.warning("No data file found for %s", collection_name)

    if not raw_docs:
        logger.info("No modified records found for %s.", collection_name)
        if not dry_run:
            sync_manager.update_last_sync_time(collection_name, sync_start)
        return

    logger.info("Found %d records to transform.", len(raw_docs))
    transformed_rows = transform_records(raw_docs)

    if dry_run or bq_loader is None:
        logger.info("[DRY-RUN] Sample transformed row for %s:\n%s", target_table, json.dumps(transformed_rows[0], indent=2))
        logger.info("[DRY-RUN] Transformed %d records successfully. (No BigQuery write performed).", len(transformed_rows))
        sync_manager.update_last_sync_time(collection_name, sync_start)
    else:
        result = bq_loader.insert_rows(target_table, transformed_rows)
        if result["status"] == "success":
            logger.info("Successfully streamed %d rows to BigQuery.", result["inserted_count"])
            sync_manager.update_last_sync_time(collection_name, sync_start)
        else:
            logger.error("BigQuery insert status: %s, errors: %s", result["status"], result.get("errors"))

def main():
    parser = argparse.ArgumentParser(description="Jompoi Grocery ETL Sync: MongoDB to Google Cloud BigQuery")
    parser.add_argument("--dry-run", action="store_true", help="Run transformations without writing to BigQuery")
    parser.add_argument("--offline", action="store_true", help="Run using local dummy data files without connecting to MongoDB")
    parser.add_argument("--force-full", action="store_true", help="Ignore sync_state.json and perform full synchronization")
    parser.add_argument("--reset-state", action="store_true", help="Reset sync_state.json file and exit")
    parser.add_argument("--mongo-uri", default=MONGO_URI, help="MongoDB connection URI")
    parser.add_argument("--db-name", default=MONGO_DB_NAME, help="MongoDB database name")
    parser.add_argument("--bq-project", default=BQ_PROJECT_ID, help="Google Cloud project ID")
    parser.add_argument("--bq-dataset", default=BQ_DATASET_ID, help="BigQuery dataset ID")

    args = parser.parse_args()
    sync_manager = SyncStateManager(STATE_FILE)

    if args.reset_state:
        sync_manager.reset_state()
        logger.info("Sync state cleared successfully.")
        return

    mongo_db = None
    if not args.offline:
        try:
            from pymongo import MongoClient
            client = MongoClient(args.mongo_uri, serverSelectionTimeoutMS=2000)
            client.admin.command("ping")
            mongo_db = client[args.db_name]
            logger.info("Connected to MongoDB at %s (%s)", args.mongo_uri, args.db_name)
        except Exception as e:
            logger.warning("Could not connect to MongoDB (%s). Falling back to offline dummy data mode.", e)
            mongo_db = None

    bq_loader = None
    if not args.dry_run and not args.offline:
        try:
            loader = BigQueryLoader(project_id=args.bq_project, dataset_id=args.bq_dataset)
            if loader.is_connected():
                bq_loader = loader
                logger.info("Authenticated to BigQuery for project: %s", args.bq_project)
            else:
                logger.warning("BigQuery client could not authenticate. Running in dry-run mode.")
        except Exception as e:
            logger.warning("BigQuery initialization failed: %s. Running in dry-run mode.", e)

    logger.info("Starting Jompoi MongoDB -> BigQuery ETL Pipeline...")
    for coll in COLLECTIONS_TO_SYNC:
        run_sync_for_collection(
            mongo_db=mongo_db,
            bq_loader=bq_loader,
            sync_manager=sync_manager,
            collection_name=coll,
            dry_run=(args.dry_run or bq_loader is None),
            force_full=args.force_full
        )

    logger.info("ETL Synchronization completed.")

if __name__ == "__main__":
    main()
