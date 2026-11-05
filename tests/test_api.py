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

def test_create_purchase_invoice_multi_item():
    payload = {
        "invoice_no": "PUR-TEST-888",
        "invoice_date": "2026-08-27",
        "vendor": "Agro Wholesale Suppliers",
        "items": [
            {
                "item_code": "ITM001",
                "item_name": "Basmati Rice 5kg",
                "quantity": 10,
                "rate": 350.0,
                "gst_percent": 5.0
            },
            {
                "item_code": "ITM002",
                "item_name": "Cold Pressed Coconut Oil 1L",
                "quantity": 5,
                "rate": 200.0,
                "gst_percent": 12.0
            }
        ]
    }
    response = client.post("/api/purchases/invoice", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["purchase"]["invoice_no"] == "PUR-TEST-888"
    assert len(data["purchase"]["items"]) == 2
    # Item 1: 3500 net, 175 gst
    # Item 2: 1000 net, 120 gst
    # Total net: 4500, Total gst: 295, Total: 4795
    assert data["purchase"]["net_amount"] == 4500.0
    assert data["purchase"]["gst_amount"] == 295.0
    assert data["purchase"]["total_amount"] == 4795.0
    assert len(data["stock_ledger_entries"]) == 2
    assert data["stock_ledger_entries"][0]["transaction_type"] == "IN"

def test_print_invoice():
    payload = {
        "invoice_no": "INV-PRINT-001",
        "invoice_date": "2026-11-05",
        "customer_name": "ABC Stores",
        "customer_address": "123, Anna Nagar, Chennai",
        "items": [
            {
                "item_name": "Basmati Rice 5kg",
                "item_description": "India Gate Premium Long Grain",
                "quantity": 10,
                "price": 450.0,
                "tax_percent": 5.0
            },
            {
                "item_name": "Sunflower Oil 1L",
                "quantity": 5,
                "price": 135.0,
                "tax_percent": 12.0
            }
        ]
    }
    response = client.post("/api/invoice/print", json=payload)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html = response.text
    assert "INV-PRINT-001" in html
    assert "Basmati Rice 5kg" in html
    assert "India Gate Premium Long Grain" in html
    assert "Sunflower Oil 1L" in html
    assert "ABC Stores" in html
    assert "Print Invoice" in html
    # Item 1: tax = 450 * 5% = 22.50, total = (450 + 22.50) * 10 = 4725.00
    assert "4,725.00" in html
    # Item 2: tax = 135 * 12% = 16.20, total = (135 + 16.20) * 5 = 756.00
    assert "756.00" in html
    # Grand total = 4725 + 756 = 5481
    assert "5,481.00" in html

