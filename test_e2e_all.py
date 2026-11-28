import urllib.request
import json
import time
import os

BASE_URL = "http://localhost:8080"

print("==========================================================")
print("RUNNING COMPREHENSIVE E2E PURCHASE INVOICE TEST SUITE")
print("==========================================================")

# 1. TEST A: SINGLE ITEM PURCHASE INVOICE
print("\n--- TEST A: Single Item Purchase Invoice ---")
inv_a = f"PUR-SINGLE-{int(time.time())}"
payload_a = {
    "invoice_no": inv_a,
    "invoice_date": "2026-11-24",
    "vendor": "KR Agro Supplies",
    "vendor_gstin": "33AABCK1234A1Z5",
    "itc_eligible": True,
    "items": [
        {
            "item_code": "ITM001",
            "item_name": "Basmati Rice 5kg",
            "quantity": 10.0,
            "rate": 380.0,
            "gst_percent": 5.0
        }
    ]
}

req_a = urllib.request.Request(
    f"{BASE_URL}/api/purchases/invoice",
    data=json.dumps(payload_a).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req_a) as res:
    res_a = json.loads(res.read().decode())
    print(f"Test A Status: {res.status}")
    assert res.status == 200, f"Expected 200, got {res.status}"
    inv_data = res_a.get("invoice", {})
    assert inv_data.get("invoice_no") == inv_a
    assert len(inv_data.get("items", [])) == 1
    assert inv_data["items"][0]["net_amount"] == 3800.0
    assert inv_data["items"][0]["gst_amount"] == 190.0
    assert inv_data["items"][0]["total_amount"] == 3990.0
    print(f"Test A PASSED: Created single-item invoice {inv_a} successfully.")

# 2. TEST B: MULTI-ITEM PURCHASE INVOICE (3 ITEMS)
print("\n--- TEST B: Multi-Item Purchase Invoice (3 Items) ---")
inv_b = f"PUR-MULTI-{int(time.time())}"
payload_b = {
    "invoice_no": inv_b,
    "invoice_date": "2026-11-24",
    "vendor": "Adani Wilmar Dist",
    "vendor_gstin": "33AABCA5678B1Z2",
    "itc_eligible": True,
    "items": [
        {
            "item_code": "ITM001",
            "item_name": "Basmati Rice 5kg",
            "quantity": 25.0,
            "rate": 380.0,
            "gst_percent": 5.0
        },
        {
            "item_code": "ITM002",
            "item_name": "Sunflower Oil 1L",
            "quantity": 40.0,
            "rate": 110.0,
            "gst_percent": 5.0
        },
        {
            "item_code": "ITM005",
            "item_name": "Chakki Atta 5kg",
            "quantity": 15.0,
            "rate": 200.0,
            "gst_percent": 5.0
        }
    ]
}

req_b = urllib.request.Request(
    f"{BASE_URL}/api/purchases/invoice",
    data=json.dumps(payload_b).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req_b) as res:
    res_b = json.loads(res.read().decode())
    print(f"Test B Status: {res.status}")
    assert res.status == 200, f"Expected 200, got {res.status}"
    inv_data_b = res_b.get("invoice", {})
    assert inv_data_b.get("invoice_no") == inv_b
    assert len(inv_data_b.get("items", [])) == 3
    print(f"Test B PASSED: Created multi-item invoice {inv_b} with 3 distinct items successfully.")

# 3. TEST C: DETAILED MATHEMATICAL CALCULATIONS
print("\n--- TEST C: Calculations Verification ---")
# Item 1: 25 * 380 = 9500 net, 5% gst = 475, total = 9975
# Item 2: 40 * 110 = 4400 net, 5% gst = 220, total = 4620
# Item 3: 15 * 200 = 3000 net, 5% gst = 150, total = 3150
# Expected invoice net = 9500 + 4400 + 3000 = 16900
# Expected invoice gst = 475 + 220 + 150 = 845
# Expected invoice total = 16900 + 845 = 17745
items_b = inv_data_b["items"]
assert items_b[0]["net_amount"] == 9500.0
assert items_b[0]["gst_amount"] == 475.0
assert items_b[0]["total_amount"] == 9975.0

assert items_b[1]["net_amount"] == 4400.0
assert items_b[1]["gst_amount"] == 220.0
assert items_b[1]["total_amount"] == 4620.0

assert items_b[2]["net_amount"] == 3000.0
assert items_b[2]["gst_amount"] == 150.0
assert items_b[2]["total_amount"] == 3150.0

assert inv_data_b["net_amount"] == 16900.0
assert inv_data_b["gst_amount"] == 845.0
assert inv_data_b["total_amount"] == 17745.0
print(f"Item 1: Net = ₹{items_b[0]['net_amount']}, GST = ₹{items_b[0]['gst_amount']}, Total = ₹{items_b[0]['total_amount']}")
print(f"Item 2: Net = ₹{items_b[1]['net_amount']}, GST = ₹{items_b[1]['gst_amount']}, Total = ₹{items_b[1]['total_amount']}")
print(f"Item 3: Net = ₹{items_b[2]['net_amount']}, GST = ₹{items_b[2]['gst_amount']}, Total = ₹{items_b[2]['total_amount']}")
print(f"Invoice Grand Totals: Net = ₹{inv_data_b['net_amount']}, ITC GST = ₹{inv_data_b['gst_amount']}, Total = ₹{inv_data_b['total_amount']}")
print("Test C PASSED: All line calculations and invoice grand totals match 100%.")

# 4. TEST D: PERSISTENCE AND RETRIEVAL
print("\n--- TEST D: Persistence and Retrieval Verification ---")
with urllib.request.urlopen(f"{BASE_URL}/api/purchases") as res:
    all_purchases = json.loads(res.read().decode())
    found_b = next((p for p in all_purchases if p.get("invoice_no") == inv_b), None)
    assert found_b is not None, f"Invoice {inv_b} not found in database!"
    assert len(found_b["items"]) == 3, f"Expected 3 items, found {len(found_b['items'])}"
    print(f"Retrieved {inv_b} from database: {len(found_b['items'])} items, Total ₹{found_b['total_amount']}.")
    print("Test D PASSED: Persistence and retrieval verified.")

# 5. TEST E: BIGQUERY SYNC VERIFICATION
print("\n--- TEST E: BigQuery Replication Verification ---")
bq_sync = res_b.get("bigquery_sync", {})
print(f"BigQuery Sync Status: {bq_sync.get('status')}")
print(f"BigQuery Target Table: {bq_sync.get('target_table')}")
print(f"BigQuery Line Items Synced: {bq_sync.get('line_items_count')}")
assert bq_sync.get("status") == "SYNCED"
assert bq_sync.get("line_items_count") == 3
print("Test E PASSED: BigQuery streaming replication verified.")

print("\n==========================================================")
print("ALL TESTS PASSED WITH 100% SUCCESS!")
print("==========================================================")
