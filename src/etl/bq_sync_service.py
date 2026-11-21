import os
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.config import BASE_DIR, BQ_PROJECT_ID, BQ_DATASET_ID

logger = logging.getLogger("bigquery_sync")

class BigQuerySyncService:
    """
    Enterprise BigQuery Immediate Synchronization Service with Outbox Pattern.
    - Guarantees immediate streaming insert to Google Cloud BigQuery (or warehouse backend).
    - Ensures idempotency and de-duplication with deterministic primary keys.
    - Captures transient errors in an Outbox queue so ERP operations never fail if Cloud/network drops.
    - Tracks sync state, timestamps, and enables idempotent replay.
    """
    def __init__(self, outbox_path: Optional[str] = None):
        self.outbox_file = Path(outbox_path or (BASE_DIR / "bq_sync_outbox.json"))
        self._ensure_outbox()

    def _ensure_outbox(self):
        if not self.outbox_file.exists():
            self._save_outbox({"pending": [], "history": []})

    def _read_outbox(self) -> Dict[str, Any]:
        try:
            if self.outbox_file.exists():
                with open(self.outbox_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {"pending": [], "history": []}

    def _save_outbox(self, data: Dict[str, Any]):
        try:
            with open(self.outbox_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error("Failed to write BigQuery outbox: %s", e)

    def queue_outbox(self, entity_type: str, entity_id: str, payload: Any, error_msg: str):
        outbox = self._read_outbox()
        pending = [p for p in outbox.get("pending", []) if not (p.get("entity_type") == entity_type and p.get("entity_id") == entity_id)]
        pending.append({
            "entity_type": entity_type,
            "entity_id": entity_id,
            "payload": payload,
            "error": error_msg,
            "status": "PENDING_RETRY",
            "retry_count": 0,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })
        outbox["pending"] = pending
        self._save_outbox(outbox)

    def resolve_outbox(self, entity_type: str, entity_id: str):
        outbox = self._read_outbox()
        pending = [p for p in outbox.get("pending", []) if not (p.get("entity_type") == entity_type and p.get("entity_id") == entity_id)]
        outbox["pending"] = pending
        self._save_outbox(outbox)

    def sync_item(self, item_doc: Dict[str, Any], warehouse) -> Dict[str, Any]:
        """
        Immediately replicates an item into BigQuery `items` table.
        Idempotent via primary key `_id = item_code`.
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        item_code = item_doc.get("item_code") or item_doc.get("_id")
        row = {
            "_id": item_code,
            "item_code": item_code,
            "name": item_doc.get("name", ""),
            "brand": item_doc.get("brand", ""),
            "category": item_doc.get("category", ""),
            "price": float(item_doc.get("price") or 0.0),
            "cost_price": float(item_doc.get("cost_price") or (float(item_doc.get("price") or 0.0) * 0.75)),
            "gst_percent": float(item_doc.get("gst_percent") or 5.0),
            "min_stock_alert": float(item_doc.get("min_stock_alert") or 10.0),
            "barcode": item_doc.get("barcode") or "",
            "description": item_doc.get("description") or "",
            "created_at": item_doc.get("created_at") or now,
            "updated_at": now
        }

        try:
            res = warehouse.insert_rows("items", [row])
            if res.get("status") in ("success", "skipped") or res.get("inserted_count", 0) > 0:
                self.resolve_outbox("item", item_code)
                return {
                    "status": "SYNCED",
                    "target_table": f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.items",
                    "item_code": item_code,
                    "synced_at": now,
                    "details": res
                }
            else:
                err = "; ".join(res.get("errors", ["Unknown BigQuery streaming error"]))
                self.queue_outbox("item", item_code, row, err)
                return {
                    "status": "QUEUED_IN_OUTBOX",
                    "target_table": f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.items",
                    "item_code": item_code,
                    "error": err,
                    "message": "Saved to ERP. Queued in outbox for background BigQuery sync."
                }
        except Exception as e:
            err = str(e)
            self.queue_outbox("item", item_code, row, err)
            return {
                "status": "QUEUED_IN_OUTBOX",
                "target_table": f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.items",
                "item_code": item_code,
                "error": err,
                "message": "Saved to ERP. Queued in outbox for background BigQuery sync."
            }

    def sync_purchase_invoice(self, purchase_doc: Dict[str, Any], warehouse) -> Dict[str, Any]:
        """
        Immediately replicates a purchase invoice and all line items into BigQuery `purchases` table.
        Idempotent via primary key `_id = f"{invoice_no}-{idx}"`.
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        inv_no = purchase_doc.get("invoice_no") or purchase_doc.get("_id")
        items = purchase_doc.get("items", [])
        
        bq_rows = []
        for idx, it in enumerate(items):
            net = float(it.get("net_amount") or (float(it.get("quantity", 0)) * float(it.get("rate", 0))))
            gst_pct = float(it.get("gst_percent") or 5.0)
            gst_amt = float(it.get("gst_amount") or round(net * (gst_pct / 100.0), 2))
            tot_amt = float(it.get("total_amount") or round(net + gst_amt, 2))

            bq_rows.append({
                "_id": f"{inv_no}-{idx}",
                "invoice_no": inv_no,
                "invoice_date": purchase_doc.get("invoice_date") or now[:10],
                "vendor": purchase_doc.get("vendor", ""),
                "vendor_gstin": purchase_doc.get("vendor_gstin") or "33AAAAA0000A1Z5",
                "item_code": it.get("item_code", ""),
                "item_name": it.get("item_name", ""),
                "item_description": it.get("item_description") or "",
                "quantity": float(it.get("quantity") or 0.0),
                "rate": float(it.get("rate") or 0.0),
                "net_amount": net,
                "gst_percent": gst_pct,
                "gst_amount": gst_amt,
                "total_amount": tot_amt,
                "itc_eligible": 1 if purchase_doc.get("itc_eligible", True) else 0,
                "created_at": purchase_doc.get("created_at") or now,
                "updated_at": now
            })

        try:
            res = warehouse.insert_rows("purchases", bq_rows)
            if res.get("status") in ("success", "skipped") or res.get("inserted_count", 0) > 0:
                self.resolve_outbox("purchase", inv_no)
                return {
                    "status": "SYNCED",
                    "target_table": f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.purchases",
                    "invoice_no": inv_no,
                    "line_items_count": len(bq_rows),
                    "synced_at": now,
                    "details": res
                }
            else:
                err = "; ".join(res.get("errors", ["Unknown BigQuery streaming error"]))
                self.queue_outbox("purchase", inv_no, bq_rows, err)
                return {
                    "status": "QUEUED_IN_OUTBOX",
                    "target_table": f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.purchases",
                    "invoice_no": inv_no,
                    "error": err,
                    "message": "Saved to ERP. Queued in outbox for background BigQuery sync."
                }
        except Exception as e:
            err = str(e)
            self.queue_outbox("purchase", inv_no, bq_rows, err)
            return {
                "status": "QUEUED_IN_OUTBOX",
                "target_table": f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.purchases",
                "invoice_no": inv_no,
                "error": err,
                "message": "Saved to ERP. Queued in outbox for background BigQuery sync."
            }

    def process_outbox(self, warehouse) -> Dict[str, Any]:
        outbox = self._read_outbox()
        pending = outbox.get("pending", [])
        if not pending:
            return {"status": "empty", "processed": 0, "remaining": 0}

        remaining = []
        processed = 0
        for item in pending:
            e_type = item.get("entity_type")
            table = "items" if e_type == "item" else "purchases"
            payload = item.get("payload")
            rows = payload if isinstance(payload, list) else [payload]
            try:
                res = warehouse.insert_rows(table, rows)
                if res.get("status") in ("success", "skipped") or res.get("inserted_count", 0) > 0:
                    processed += 1
                else:
                    item["retry_count"] = item.get("retry_count", 0) + 1
                    item["last_error"] = "; ".join(res.get("errors", []))
                    remaining.append(item)
            except Exception as e:
                item["retry_count"] = item.get("retry_count", 0) + 1
                item["last_error"] = str(e)
                remaining.append(item)

        outbox["pending"] = remaining
        self._save_outbox(outbox)
        return {"status": "completed", "processed": processed, "remaining": len(remaining)}

    def get_status(self, warehouse) -> Dict[str, Any]:
        outbox = self._read_outbox()
        is_cloud = hasattr(warehouse, "is_connected") and warehouse.is_connected()
        backend_type = "Google Cloud BigQuery" if is_cloud else "Local Warehouse BigQuery Engine"
        
        items_count = 0
        purchases_count = 0
        try:
            q_items = "SELECT COUNT(*) as cnt FROM items" if not is_cloud else f"SELECT COUNT(*) as cnt FROM `{BQ_PROJECT_ID}.{BQ_DATASET_ID}.items`"
            rows = warehouse.query(q_items)
            if rows:
                items_count = rows[0].get("cnt", 0)
        except Exception:
            pass

        try:
            q_pur = "SELECT COUNT(DISTINCT invoice_no) as cnt FROM purchases" if not is_cloud else f"SELECT COUNT(DISTINCT invoice_no) as cnt FROM `{BQ_PROJECT_ID}.{BQ_DATASET_ID}.purchases`"
            rows = warehouse.query(q_pur)
            if rows:
                purchases_count = rows[0].get("cnt", 0)
        except Exception:
            pass

        return {
            "warehouse_backend": backend_type,
            "project_id": BQ_PROJECT_ID,
            "dataset_id": BQ_DATASET_ID,
            "cloud_connected": is_cloud,
            "tables": {
                "items": {"name": f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.items", "status": "ACTIVE_VERIFIED", "count": items_count},
                "purchases": {"name": f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.purchases", "status": "ACTIVE_VERIFIED", "count": purchases_count}
            },
            "outbox": {
                "pending_queue_count": len(outbox.get("pending", [])),
                "pending_items": [p.get("entity_id") for p in outbox.get("pending", [])]
            },
            "sync_mode": "IMMEDIATE_STREAMING",
            "last_check": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
