import urllib.request
import json
import time

timestamp = int(time.time())
test_item = {
    "item_code": f"ITM_{timestamp}",
    "name": f"Fresh Filter Coffee {timestamp}",
    "brand": "Narasus",
    "category": "Beverages",
    "price": 175.0,
    "cost_price": 130.0,
    "gst_percent": 5.0,
    "opening_stock": 25.0,
    "min_stock_alert": 10.0,
    "barcode": f"89012345{timestamp % 10000}"
}

print(f"Creating test item {test_item['item_code']} via ERP backend...")
req = urllib.request.Request(
    "http://localhost:8080/api/items",
    data=json.dumps(test_item).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    print("API Response:", json.dumps(data, indent=2))

print("\nVerifying immediate replication directly in BigQuery...")
time.sleep(2)

from src.config import BQ_PROJECT_ID, BQ_DATASET_ID
from src.etl.bq_loader import BigQueryLoader

bq = BigQueryLoader(BQ_PROJECT_ID, BQ_DATASET_ID)
bt = chr(96)
code = test_item["item_code"]
sql = f"SELECT item_code, name, price, created_at FROM {bt}{BQ_PROJECT_ID}.{BQ_DATASET_ID}.items{bt} WHERE item_code = '{code}'"
rows = bq.query(sql)

print(f"BigQuery Query returned {len(rows)} record(s):")
for r in rows:
    print(" -> SUCCESS IN BIGQUERY:", r)
