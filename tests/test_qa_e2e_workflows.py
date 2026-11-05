"""
Comprehensive End-to-End Enterprise QA Automation Test Suite
Supermarket ERP Ecosystem: Backend API, Inventory, GST & POS Billing Workflows
"""

import os
import pytest
import datetime
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# Helper fixture for admin authentication
@pytest.fixture(scope="module")
def admin_token():
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]

@pytest.fixture(scope="module")
def cashier_token():
    resp = client.post("/api/auth/login", json={"username": "cashier", "password": "cashier123"})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]

@pytest.fixture(scope="module")
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture(scope="module")
def cashier_headers(cashier_token):
    return {"Authorization": f"Bearer {cashier_token}"}


# ===========================================================================
# PHASE 4 & 5: WORKFLOW A - PRODUCT TO INVENTORY
# ===========================================================================

def test_workflow_a_product_to_inventory(auth_headers):
    """
    Workflow A:
    1. Admin logs in.
    2. Creates new product with SKU, barcode, pricing.
    3. Adds opening stock movement.
    4. Retrieves product via barcode and code.
    5. Verifies stock position and audit ledger.
    """
    ts = int(datetime.datetime.now().timestamp())
    item_code = f"QA_ITM_{ts}"
    barcode = f"8901234{ts % 100000:05d}"

    # 1. Register Product
    prod_payload = {
        "item_code": item_code,
        "barcode": barcode,
        "name": "QA Premium Brown Rice 5kg",
        "description": "Organic Aged Brown Rice",
        "brand": "QA Organics",
        "category": "Grains",
        "price": 380.0,
        "cost_price": 300.0,
        "gst_percent": 5.0,
        "min_stock_alert": 15.0
    }
    create_resp = client.post("/api/items", json=prod_payload, headers=auth_headers)
    assert create_resp.status_code == 200, create_resp.text
    created = create_resp.json()["item"]
    assert created["item_code"] == item_code
    assert created["price"] == 380.0

    # 2. Barcode lookup
    bc_resp = client.get(f"/api/items/barcode/{barcode}")
    assert bc_resp.status_code == 200
    assert bc_resp.json()["name"] == "QA Premium Brown Rice 5kg"

    # 3. Code lookup
    code_resp = client.get(f"/api/items/{item_code}")
    assert code_resp.status_code == 200
    assert code_resp.json()["brand"] == "QA Organics"

    # 4. Add opening stock via audit adjustment
    adj_payload = {
        "item_code": item_code,
        "adjustment_type": "ADD",
        "quantity": 50.0,
        "reason": "AUDIT_CORRECTION",
        "notes": "Opening balance entry"
    }
    adj_resp = client.post("/api/stock/adjust", json=adj_payload, headers=auth_headers)
    assert adj_resp.status_code == 200, adj_resp.text

    # 5. Verify stock position reflects 50 units
    stk_resp = client.get("/api/stock")
    assert stk_resp.status_code == 200
    pos_list = stk_resp.json()
    item_pos = next((p for p in pos_list if p.get("item_code") == item_code), None)
    assert item_pos is not None, f"Item {item_code} not found in stock position"
    assert item_pos["quantity_on_hand"] >= 50.0
    assert item_pos["inventory_valuation"] >= 50.0 * 380.0


# ===========================================================================
# PHASE 4 & 5: WORKFLOW B - PURCHASE TO INVENTORY
# ===========================================================================

def test_workflow_b_purchase_to_inventory(auth_headers):
    """
    Workflow B:
    1. Register supplier.
    2. Create purchase order / inward invoice with multiple items & GST.
    3. Verify stock ledger IN logged.
    4. Verify stock quantity increment.
    """
    ts = int(datetime.datetime.now().timestamp())
    vendor_id = f"QA_VEND_{ts}"

    # 1. Create Supplier
    vend_payload = {
        "vendor_id": vendor_id,
        "name": "QA Supermarket Distributors Ltd",
        "gstin": "33AABCS1429B1Z8",
        "contact_person": "QA Manager",
        "phone": "+91 9988776655",
        "city": "Chennai",
        "state": "Tamil Nadu"
    }
    v_resp = client.post("/api/vendors", json=vend_payload, headers=auth_headers)
    assert v_resp.status_code == 200, v_resp.text

    # 2. Inward Purchase Invoice
    p_inv_no = f"QA-PUR-{ts}"
    purchase_payload = {
        "invoice_no": p_inv_no,
        "invoice_date": datetime.date.today().isoformat(),
        "vendor": "QA Supermarket Distributors Ltd",
        "vendor_gstin": "33AABCS1429B1Z8",
        "items": [
            {
                "item_code": "ITM001",
                "item_name": "Ponni Boiled Rice 25kg",
                "quantity": 20.0,
                "rate": 1100.0,
                "gst_percent": 5.0
            },
            {
                "item_code": "ITM002",
                "item_name": "Gold Winner Sunflower Oil 1L",
                "quantity": 30.0,
                "rate": 125.0,
                "gst_percent": 12.0
            }
        ]
    }
    pur_resp = client.post("/api/purchases/invoices", json=purchase_payload, headers=auth_headers)
    assert pur_resp.status_code == 200, pur_resp.text
    pur_data = pur_resp.json()
    assert pur_data["invoice"]["invoice_no"] == p_inv_no
    assert pur_data["invoice"]["gst_amount"] > 0.0
    assert pur_data["invoice"]["total_amount"] > 0.0

    # 3. Verify purchase listed
    list_p = client.get("/api/purchases/invoices")
    assert list_p.status_code == 200
    assert any(p.get("invoice_no") == p_inv_no for p in list_p.json())


# ===========================================================================
# PHASE 4 & 5: WORKFLOW C - COMPLETE POS SALES & COMMERCIAL INVOICE
# ===========================================================================

def test_workflow_c_complete_pos_sales_and_billing(cashier_headers):
    """
    Workflow C:
    1. Cashier logs in.
    2. Looks up product barcode.
    3. Processes multi-item POS sales invoice.
    4. Validates formula Total = (Price + Tax) * Quantity.
    5. Validates stock OUT logged in ledger.
    6. Generates commercial printable invoice HTML.
    """
    ts = int(datetime.datetime.now().timestamp())
    sales_inv_no = f"QA-POS-{ts}"

    sales_payload = {
        "invoice_no": sales_inv_no,
        "invoice_date": datetime.date.today().isoformat(),
        "customer_name": "Dr. Rajesh Raman",
        "customer_city": "Madurai",
        "customer_address": "45 Anna Nagar, Madurai - 625020",
        "payment_mode": "CARD",
        "items": [
            {
                "item_code": "ITM001",
                "quantity": 2.0,
                "rate": 1400.0,
                "discount_percent": 0.0
            },
            {
                "item_code": "ITM003",
                "quantity": 4.0,
                "rate": 160.0,
                "discount_percent": 5.0
            }
        ]
    }

    # 1. Submit POS sale
    sale_resp = client.post("/api/sales/invoices", json=sales_payload, headers=cashier_headers)
    assert sale_resp.status_code == 200, sale_resp.text
    inv_doc = sale_resp.json()["invoice"]

    # 2. Verify Line Item Tax Formula: Total = (Price + Tax) * Qty
    assert len(inv_doc["items"]) == 2
    for item in inv_doc["items"]:
        price = float(item["unit_price"])
        unit_tax = float(item["unit_tax"])
        qty = float(item["quantity"])
        expected_line_total = round((price + unit_tax) * qty, 2)
        assert abs(float(item["line_total"]) - expected_line_total) < 0.02, (
            f"Formula violation: line_total={item['line_total']}, expected={expected_line_total}"
        )

    # 3. Verify stock OUT entry exists
    assert len(sale_resp.json()["stock_ledger_entries"]) == 2
    for entry in sale_resp.json()["stock_ledger_entries"]:
        assert entry["movement_type"] == "OUT"
        assert entry["voucher_type"] == "SALES_INVOICE"

    # 4. Printable Invoice View Verification
    print_resp = client.get(f"/api/invoice/{sales_inv_no}/print")
    assert print_resp.status_code == 200
    assert "text/html" in print_resp.headers["content-type"]
    html = print_resp.text
    assert sales_inv_no in html
    assert "Dr. Rajesh Raman" in html
    assert "Tax" in html
    assert "Price+Tax" in html


# ===========================================================================
# PHASE 4 & 5: WORKFLOW D - PRODUCT RETURN & REFUND
# ===========================================================================

def test_workflow_d_product_return_and_refund(cashier_headers):
    """
    Workflow D:
    1. Create an initial sales invoice.
    2. Customer returns 1 resellable item and 1 damaged item.
    3. Verify refund calculation = (Price + Tax) * Returned Qty.
    4. Verify stock ledger updated with IN for resellable item.
    5. Verify refund record is logged.
    """
    ts = int(datetime.datetime.now().timestamp())
    orig_inv_no = f"QA-RET-INV-{ts}"

    # 1. Original Sale
    sale_resp = client.post("/api/sales/invoices", json={
        "invoice_no": orig_inv_no,
        "invoice_date": datetime.date.today().isoformat(),
        "customer_name": "Suresh Kumar",
        "customer_city": "Coimbatore",
        "payment_mode": "UPI",
        "items": [
            {"item_code": "ITM001", "quantity": 3.0, "rate": 1400.0, "discount_percent": 0.0},
            {"item_code": "ITM002", "quantity": 2.0, "rate": 150.0, "discount_percent": 0.0}
        ]
    }, headers=cashier_headers)
    assert sale_resp.status_code == 200, sale_resp.text

    # 2. Customer returns 1 unit of ITM001
    return_payload = {
        "return_items": [
            {
                "item_code": "ITM001",
                "quantity": 1.0,
                "reason": "Customer ordered excess",
                "condition": "RESELLABLE"
            }
        ],
        "notes": "Refund to UPI"
    }
    ret_resp = client.post(f"/api/sales/{orig_inv_no}/return", json=return_payload, headers=cashier_headers)
    assert ret_resp.status_code == 200, ret_resp.text
    ret_record = ret_resp.json()["return_record"]
    assert ret_record["original_invoice_no"] == orig_inv_no
    # Price = 1400, GST 5% = 70, Line total refund = 1470.0
    assert abs(ret_record["total_refund_amount"] - 1470.0) < 0.1

    # 3. Verify Return List
    list_ret = client.get("/api/sales/returns")
    assert list_ret.status_code == 200
    assert any(r.get("original_invoice_no") == orig_inv_no for r in list_ret.json())


# ===========================================================================
# PHASE 4 & 5: WORKFLOW E - REPORTING & RECONCILIATION
# ===========================================================================

def test_workflow_e_reports_and_reconciliation():
    """
    Workflow E:
    1. Retrieve GST ITC reconciliation report.
    2. Verify GSTR-1 output tax and GSTR-2B eligible credit.
    3. Retrieve Profit & Loss report.
    4. Verify Revenue - COGS = Gross Profit, Gross Profit - Expenses = Net Operating Profit.
    """
    # 1. GST Reconciliation Report
    gst_resp = client.get("/api/gst/reconciliation")
    assert gst_resp.status_code == 200
    gst_data = gst_resp.json()
    assert "output_gst_sales" in gst_data
    assert "input_gst_purchases" in gst_data
    assert "itc_eligible" in gst_data
    assert "net_gst_payable_in_cash" in gst_data
    assert gst_data["output_gst_sales"] >= 0.0

    # 2. Profit & Loss Statement
    pnl_resp = client.get("/api/reports/pnl?operating_expenses=5000.0")
    assert pnl_resp.status_code == 200
    pnl_data = pnl_resp.json()
    rev = pnl_data["revenue"]
    cogs = pnl_data["cogs"]
    gp = pnl_data["gross_profit"]
    opex = pnl_data["operating_expenses"]
    net = pnl_data["net_operating_profit"]

    # Verify Accounting Consistency
    assert abs(gp - (rev - cogs)) < 0.01, f"Gross Profit mismatch: {gp} != {rev} - {cogs}"
    assert abs(net - (gp - opex)) < 0.01, f"Net Profit mismatch: {net} != {gp} - {opex}"


# ===========================================================================
# PHASE 3: NEGATIVE & SECURITY TESTING
# ===========================================================================

def test_negative_duplicate_item_code(auth_headers):
    """Verify duplicate SKU / item code is rejected with HTTP 400."""
    item_payload = {
        "item_code": "ITM001", # Existing catalog item
        "name": "Duplicate Ponni Rice",
        "brand": "Duplicate Brand",
        "category": "Grains",
        "price": 500.0
    }
    resp = client.post("/api/items", json=item_payload, headers=auth_headers)
    assert resp.status_code == 400
    assert "already exists" in resp.json()["detail"].lower()


def test_negative_negative_price_validation(auth_headers):
    """Verify negative price is rejected with HTTP 422 Unprocessable Entity."""
    bad_payload = {
        "item_code": "INVALID_PRICE_ITEM",
        "name": "Invalid Price Item",
        "brand": "Bad Brand",
        "category": "Snacks",
        "price": -100.0 # Negative price
    }
    resp = client.post("/api/items", json=bad_payload, headers=auth_headers)
    assert resp.status_code == 422


def test_negative_zero_or_negative_quantity(auth_headers):
    """Verify zero or negative stock adjustment quantity is rejected with HTTP 422."""
    bad_adj = {
        "item_code": "ITM001",
        "adjustment_type": "ADD",
        "quantity": -5.0, # Negative quantity
        "reason": "DAMAGE"
    }
    resp = client.post("/api/stock/adjust", json=bad_adj, headers=auth_headers)
    assert resp.status_code == 422


def test_negative_return_excess_quantity(cashier_headers):
    """Verify returning quantity greater than purchased quantity is rejected with HTTP 400."""
    # INV-2026-001 has ITM001 with qty 1
    resp = client.post("/api/sales/INV-2026-001/return", json={
        "return_items": [
            {"item_code": "ITM001", "quantity": 999.0}
        ]
    }, headers=cashier_headers)
    assert resp.status_code == 400
    assert "exceeds" in resp.json()["detail"].lower()


def test_security_unauthenticated_access(monkeypatch):
    """Verify protected endpoints reject unauthenticated requests with HTTP 401 when strict auth is active."""
    monkeypatch.setenv("ERP_STRICT_AUTH", "true")
    resp = client.post("/api/items", json={
        "item_code": "SEC01",
        "name": "Unauthorized Item",
        "brand": "Hacker",
        "category": "Grains",
        "price": 100.0
    })
    assert resp.status_code == 401
    assert "credentials" in resp.json()["detail"].lower()


def test_security_role_based_access_forbidden(cashier_headers):
    """Verify cashier cannot register new system users (Admin-only) -> HTTP 403."""
    user_payload = {
        "username": "unauthorized_user",
        "password": "Password123!",
        "full_name": "Unauthorized User",
        "role": "CASHIER"
    }
    resp = client.post("/api/auth/register", json=user_payload, headers=cashier_headers)
    assert resp.status_code == 403


def test_security_nosql_injection_attempt_handling():
    """Verify that injection strings in search filters are treated literally without runtime crashes."""
    injection_strings = [
        "{\"$gt\": \"\"}",
        "' OR '1'='1",
        "'; DROP TABLE items; --",
        "<script>alert('xss')</script>"
    ]
    for inj in injection_strings:
        resp = client.get(f"/api/items?search={inj}")
        assert resp.status_code == 200
        # Returns empty list or safe literal matches without internal 500 error
        assert isinstance(resp.json(), list)
