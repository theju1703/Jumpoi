import urllib.request
import json
import time

timestamp = int(time.time())
inv_no = f"PUR-MULTI-{timestamp}"

payload = {
    "invoice_no": inv_no,
    "invoice_date": "2026-11-24",
    "vendor": "KR Agro Supplies",
    "vendor_gstin": "33AABCK1234A1Z5",
    "itc_eligible": True,
    "items": [
        {
            "item_code": "ITM001",
            "item_name": "Basmati Rice 5kg",
            "quantity": 20.0,
            "rate": 380.0,
            "gst_percent": 5.0
        },
        {
            "item_code": "ITM002",
            "item_name": "Sunflower Oil 1L",
            "quantity": 15.0,
            "rate": 110.0,
            "gst_percent": 5.0
        },
        {
            "item_code": "ITM003",
            "item_name": "Toor Dal 1kg",
            "quantity": 25.0,
            "rate": 130.0,
            "gst_percent": 0.0
        }
    ]
}

print(f"Creating Multi-Item Purchase Invoice {inv_no} with 3 line items...")
req = urllib.request.Request(
    "http://localhost:8080/api/purchases/invoice",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req) as res:
    res_data = json.loads(res.read().decode())
    print("API Response status:", res.status)
    print("BigQuery Sync result:", json.dumps(res_data.get("bigquery_sync"), indent=2))

time.sleep(2)

# Verify BigQuery direct retrieval
from src.config import BQ_PROJECT_ID, BQ_DATASET_ID
from src.etl.bq_loader import BigQueryLoader

bq = BigQueryLoader(BQ_PROJECT_ID, BQ_DATASET_ID)
bt = chr(96)
sql = f"SELECT invoice_no, vendor, net_amount, gst_amount, total_amount, created_at FROM {bt}{BQ_PROJECT_ID}.{BQ_DATASET_ID}.purchases{bt} WHERE invoice_no = '{inv_no}'"
rows = bq.query(sql)

print(f"\nDirect BigQuery Query Result for {inv_no}:")
for r in rows:
    print(" -> SUCCESS IN BIGQUERY:", r)
