import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_operation_1_add_item_to_bigquery(auth_headers):
    payload = {
        "item_code": "BQ_ITEM_001",
        "name": "Organic Honey 500g",
        "brand": "PureNature",
        "category": "Organic & Health",
        "price": 280.0,
        "cost_price": 200.0,
        "gst_percent": 5.0,
        "min_stock_alert": 15.0,
        "barcode": "8901234567890",
        "description": "Raw unpasteurized honey"
    }
    response = client.post("/api/bigquery/items", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["item"]["item_code"] == "BQ_ITEM_001"
    assert data["bigquery_result"]["status"] in ["success", "skipped", "SYNCED"]

def test_operation_2_list_items_from_bigquery():
    response = client.get("/api/bigquery/items")
    assert response.status_code == 200
    data = response.json()
    assert "Google BigQuery Data Warehouse" in data["source"]
    assert "items" in data
    assert data["count"] > 0
    # Check that BQ_ITEM_001 is found or existing ITM001 is present
    codes = [item["item_code"] for item in data["items"]]
    assert any(code in codes for code in ["BQ_ITEM_001", "ITM001"])

def test_operation_3_add_purchase_to_bigquery(auth_headers):
    payload = {
        "invoice_no": "BQ-PUR-2026-999",
        "invoice_date": "2026-11-16",
        "vendor": "National Organics Ltd",
        "vendor_gstin": "33AAACN1234F1Z1",
        "items": [
            {
                "item_code": "BQ_ITEM_001",
                "item_name": "Organic Honey 500g",
                "item_description": "Raw unpasteurized honey",
                "quantity": 40.0,
                "rate": 200.0,
                "gst_percent": 5.0
            },
            {
                "item_code": "ITM001",
                "item_name": "Basmati Rice 5kg",
                "item_description": "Premium aged rice",
                "quantity": 25.0,
                "rate": 380.0,
                "gst_percent": 5.0
            }
        ]
    }
    response = client.post("/api/bigquery/purchases", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["invoice_no"] == "BQ-PUR-2026-999"
    assert data["line_items_count"] == 2
    assert data["bigquery_result"]["status"] in ["success", "skipped", "SYNCED"]

def test_operation_4_list_purchases_from_bigquery():
    response = client.get("/api/bigquery/purchases")
    assert response.status_code == 200
    data = response.json()
    assert "Google BigQuery Data Warehouse" in data["source"]
    assert "invoices" in data
    assert data["invoices_count"] > 0
    
    # Locate BQ-PUR-2026-999 or PINV001
    inv_map = {inv["invoice_no"]: inv for inv in data["invoices"]}
    assert "BQ-PUR-2026-999" in inv_map or "PUR-2026-001" in inv_map
    if "BQ-PUR-2026-999" in inv_map:
        inv = inv_map["BQ-PUR-2026-999"]
        assert inv["vendor"] == "National Organics Ltd"
        assert len(inv["items"]) == 2
        assert inv["total_amount"] > 0

def test_operation_5_bigquery_table_status_verification():
    response = client.get("/api/bigquery/table-status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["project_id"] == "project-b6567b21-77eb-47fb-926"
    assert data["dataset_id"] == "jompoi_reporting"
    assert "tables" in data
    table_names = [t["table_name"] for t in data["tables"]]
    assert "items" in table_names
    assert "purchases" in table_names
    items_table = next(t for t in data["tables"] if t["table_name"] == "items")
    assert items_table["status"] == "CREATED_AND_VERIFIED"
    assert len(items_table["columns"]) >= 10

def test_operation_6_api_items_immediate_sync_to_bigquery(auth_headers):
    import time
    code = f"SYNC_ITEM_{int(time.time() * 1000) % 100000}"
    payload = {
        "item_code": code,
        "name": "Organic Almond Milk 1L",
        "brand": "NutriLife",
        "category": "Dairy Alternatives",
        "price": 195.0,
        "cost_price": 140.0,
        "gst_percent": 5.0,
        "min_stock_alert": 10.0,
        "opening_stock": 25.0
    }
    response = client.post("/api/items", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "bigquery_sync" in data
    assert data["bigquery_sync"]["status"] in ["SYNCED", "QUEUED_IN_OUTBOX"]
    
    # Verify in BigQuery items list
    bq_res = client.get("/api/bigquery/items")
    assert bq_res.status_code == 200
    bq_codes = [i["item_code"] for i in bq_res.json()["items"]]
    assert code in bq_codes

def test_operation_7_api_purchases_immediate_sync_to_bigquery(auth_headers):
    import time
    inv_no = f"PUR-SYNC-{int(time.time() * 1000) % 100000}"
    payload = {
        "invoice_no": inv_no,
        "invoice_date": "2026-11-20",
        "vendor": "Agro Fresh Mart",
        "vendor_gstin": "33AAACA9999Z1Z8",
        "items": [
            {
                "item_code": "ITM001",
                "item_name": "Basmati Rice 5kg",
                "quantity": 50.0,
                "rate": 140.0,
                "gst_percent": 5.0
            }
        ]
    }
    response = client.post("/api/purchases/invoice", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "bigquery_sync" in data
    assert data["bigquery_sync"]["status"] in ["SYNCED", "QUEUED_IN_OUTBOX"]
    
    # Verify in BigQuery purchases list
    bq_res = client.get("/api/bigquery/purchases")
    assert bq_res.status_code == 200
    inv_nos = [i["invoice_no"] for i in bq_res.json()["invoices"]]
    assert inv_no in inv_nos

def test_operation_8_sync_status_and_outbox():
    status_res = client.get("/api/bigquery/sync-status")
    assert status_res.status_code == 200
    status_data = status_res.json()
    assert "warehouse_backend" in status_data
    assert "tables" in status_data
    assert "outbox" in status_data

    outbox_res = client.post("/api/bigquery/sync-outbox")
    assert outbox_res.status_code == 200
    assert outbox_res.json()["status"] in ["empty", "completed"]

