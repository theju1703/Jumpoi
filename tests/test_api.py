from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_list_items_endpoint():
    response = client.get("/api/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0

def test_gst_report_endpoint():
    response = client.get("/api/gst/report")
    assert response.status_code == 200
    report = response.json()
    assert "output_gst_sales" in report
    assert "input_gst_purchases" in report
    assert "net_gst_payable_in_cash" in report

def test_pnl_endpoint():
    response = client.get("/api/pnl")
    assert response.status_code == 200
    pnl = response.json()
    assert "revenue" in pnl
    assert "gross_profit" in pnl
    assert "net_profit" in pnl

def test_create_sales_invoice():
    payload = {
        "invoice_no": "INV-TEST-999",
        "invoice_date": "2026-08-26",
        "customer_name": "Test Supermarket",
        "customer_city": "Chennai",
        "item_code": "ITM001",
        "item_name": "Basmati Rice 5kg",
        "quantity": 2,
        "rate": 450.0,
        "gst_percent": 5.0
    }
    response = client.post("/api/sales/invoice", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["invoice"]["net_amount"] == 900.0
    assert data["invoice"]["gst_amount"] == 45.0
    assert data["invoice"]["total_amount"] == 945.0
    assert data["stock_ledger_entry"]["transaction_type"] == "OUT"
