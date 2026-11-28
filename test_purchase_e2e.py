import urllib.request
import json
import time

timestamp = int(time.time())
test_purchase = {
    "invoice_no": f"PUR-TEST-{timestamp}",
    "invoice_date": "2026-11-22",
    "vendor": "KR Agro Supplies",
    "vendor_gstin": "33AABCK1234A1Z5",
    "itc_eligible": True,
    "items": [
        {
            "item_code": f"ITM_{timestamp}",
            "item_name": f"Fresh Filter Coffee {timestamp}",
            "quantity": 10.0,
            "rate": 130.0,
            "gst_percent": 5.0
        }
    ]
}

print(f"Creating purchase invoice {test_purchase['invoice_no']} via ERP backend...")
req = urllib.request.Request(
    "http://localhost:8080/api/purchases/invoice",
    data=json.dumps(test_purchase).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    print("API Response:", json.dumps(data, indent=2))

print("\nVerifying immediate replication directly in BigQuery purchases...")
time.sleep(2)

from src.config import BQ_PROJECT_ID, BQ_DATASET_ID
from src.etl.bq_loader import BigQueryLoader

bq = BigQueryLoader(BQ_PROJECT_ID, BQ_DATASET_ID)
bt = chr(96)
inv_no = test_purchase["invoice_no"]
sql = f"SELECT invoice_no, vendor, net_amount, gst_amount, total_amount FROM {bt}{BQ_PROJECT_ID}.{BQ_DATASET_ID}.purchases{bt} WHERE invoice_no = '{inv_no}'"
rows = bq.query(sql)

print(f"BigQuery Purchases Query returned {len(rows)} record(s):")
for r in rows:
    print(" -> SUCCESS IN BIGQUERY PURCHASES:", r)
