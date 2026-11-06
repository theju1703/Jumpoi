from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

# --- AUTH TESTS ---

def test_auth_login_success():
    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "ADMIN"

def test_auth_login_invalid_password():
    response = client.post("/api/auth/login", json={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401

def test_auth_me_authenticated():
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["access_token"]
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["role"] == "ADMIN"

def test_auth_register_new_user():
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    payload = {
        "username": "cashier_test",
        "password": "cashierpwd123",
        "full_name": "Test Cashier User",
        "role": "CASHIER"
    }
    response = client.post("/api/auth/register", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "cashier_test"

# --- ITEM / CATALOG TESTS ---

def test_list_items_endpoint():
    response = client.get("/api/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0

def test_get_item_by_code():
    response = client.get("/api/items/ITM001")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Basmati Rice 5kg"

def test_barcode_lookup():
    response = client.get("/api/items/barcode/ITM001")
    assert response.status_code == 200
    assert response.json()["item_code"] == "ITM001"

def test_update_item():
    response = client.put("/api/items/ITM001", json={"price": 460.0})
    assert response.status_code == 200
    assert response.json()["item"]["price"] == 460.0

# --- INVENTORY & STOCK TESTS ---

def test_stock_position():
    response = client.get("/api/stock")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_stock_low_stock_alerts():
    response = client.get("/api/stock/low-stock")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_stock_adjustment():
    payload = {
        "item_code": "ITM001",
        "adjustment_type": "DEDUCT",
        "quantity": 1,
        "reason": "DAMAGE",
        "notes": "Damaged during warehouse transit"
    }
    response = client.post("/api/stock/adjust", json=payload)
    assert response.status_code == 200
    assert response.json()["entry"]["transaction_type"] == "OUT_ADJUSTMENT"

# --- VENDORS & PURCHASES ---

def test_vendors_list_and_create():
    response = client.get("/api/vendors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    vendor_payload = {
        "vendor_id": "VEND-NEW-01",
        "name": "Organic Agri Hub",
        "gstin": "33AAAFO9999A1Z2",
        "phone": "+91 9888877777",
        "city": "Salem"
    }
    create_res = client.post("/api/vendors", json=vendor_payload)
    assert create_res.status_code == 200
    assert create_res.json()["vendor"]["name"] == "Organic Agri Hub"

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
    assert data["purchase"]["net_amount"] == 4500.0
    assert data["purchase"]["gst_amount"] == 295.0
    assert data["purchase"]["total_amount"] == 4795.0
    assert len(data["stock_ledger_entries"]) == 2
    assert data["stock_ledger_entries"][0]["transaction_type"] == "IN"

# --- SALES & POS BILLING ---

def test_create_sales_invoice_single_item():
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

def test_create_sales_invoice_multi_item():
    payload = {
        "invoice_no": "INV-MULTI-001",
        "invoice_date": "2026-11-05",
        "customer_name": "Retail Shopper",
        "customer_city": "Chennai",
        "items": [
            {"item_code": "ITM001", "quantity": 3, "rate": 450.0},
            {"item_code": "ITM002", "quantity": 2, "rate": 135.0}
        ]
    }
    response = client.post("/api/sales/invoice", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Item 1: 3 * 450 = 1350, tax 5% = 67.50, total = 1417.50
    # Item 2: 2 * 135 = 270, tax 5% = 13.50, total = 283.50
    # Total = 1701.00
    assert data["invoice"]["total_amount"] == 1701.0
    assert len(data["stock_ledger_entries"]) == 2
    assert data["stock_ledger_entries"][0]["transaction_type"] == "OUT"

# --- CUSTOMER MANAGEMENT ---

def test_customer_create_and_search():
    payload = {
        "customer_id": "CUST-NEW-99",
        "name": "Lakshmi Stores",
        "city": "Tiruchirappalli",
        "phone": "+91 9444433333"
    }
    res = client.post("/api/customers", json=payload)
    assert res.status_code == 200
    
    search_res = client.get("/api/customers/search?phone=%2B91+9444433333")
    assert search_res.status_code == 200
    assert search_res.json()["name"] == "Lakshmi Stores"

# --- PRINT INVOICE TESTS ---

def test_print_invoice_custom():
    payload = {
        "invoice_no": "INV-PRINT-001",
        "invoice_date": "2026-11-05",
        "customer_name": "ABC Stores",
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
    assert "Print Invoice" in html
    assert "5,481.00" in html

def test_print_existing_sales_invoice():
    response = client.get("/api/invoice/INV-2026-001/print")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "INV-2026-001" in response.text
    assert "Print Invoice" in response.text

# --- GST & FINANCIAL REPORTS ---

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

def test_executive_summary_report():
    response = client.get("/api/reports/summary")
    assert response.status_code == 200
    data = response.json()
    assert "active_items_count" in data
    assert "gross_sales_revenue" in data
    assert data["status"] == "OPERATIONAL"

def test_etl_sync_trigger():
    response = client.post("/api/etl/sync")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ETL sync triggered successfully"
    assert "jompoi_reporting" in data["target_dataset"]
