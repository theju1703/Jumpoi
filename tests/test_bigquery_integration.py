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
    assert data["bigquery_result"]["status"] in ["success", "skipped"]

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
    assert data["bigquery_result"]["status"] in ["success", "skipped"]

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
