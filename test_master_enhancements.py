import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8080"

passed = 0
failed = 0

def test(name, condition, extra=""):
    global passed, failed
    if condition:
        print(f"[PASS] {name} {extra}")
        passed += 1
    else:
        print(f"[FAIL] {name} {extra}")
        failed += 1

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8")), resp.headers

def post_json(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8")), resp.headers

print("=" * 70)
print("RUNNING MASTER ENTERPRISE ERP ENHANCEMENT VERIFICATION SUITE")
print("=" * 70)

# 1. Security Headers Verification
status, health_data, headers = get_json(f"{BASE_URL}/api/health")
test("Security: X-Content-Type-Options nosniff", headers.get("X-Content-Type-Options") == "nosniff")
test("Security: X-Frame-Options SAMEORIGIN", headers.get("X-Frame-Options") == "SAMEORIGIN")
test("Security: X-XSS-Protection", "1" in (headers.get("X-XSS-Protection") or ""))
test("Security: Content-Security-Policy", "default-src 'self'" in (headers.get("Content-Security-Policy") or ""))
test("Security: Referrer-Policy", headers.get("Referrer-Policy") == "strict-origin-when-cross-origin")

# 2. Favicon handler (no 404)
req = urllib.request.Request(f"{BASE_URL}/favicon.ico")
try:
    with urllib.request.urlopen(req) as resp:
        test("System: Favicon 204 No Content", resp.status == 204)
except urllib.error.HTTPError as e:
    test("System: Favicon 204 No Content", False, f"(Got {e.code})")

# 3. Real-Time Visual Analytics Dashboard API
status, analytics, _ = get_json(f"{BASE_URL}/api/analytics/dashboard")
test("Analytics: Endpoint Status 200", status == 200)
test("Analytics: 7-Day Sales Trend populated", len(analytics.get("sales_trend_7d", [])) > 0, f"({len(analytics.get('sales_trend_7d', []))} days)")
test("Analytics: Category Revenue Breakdown", len(analytics.get("category_breakdown", [])) > 0, f"({len(analytics.get('category_breakdown', []))} categories)")
test("Analytics: Real-time Stock Health counts", "in_stock" in analytics.get("stock_health", {}) and "total_skus" in analytics.get("stock_health", {}), f"(In-Stock: {analytics.get('stock_health',{}).get('in_stock')}/{analytics.get('stock_health',{}).get('total_skus')})")
test("Analytics: Working Capital overview", "total_sales_revenue" in analytics.get("working_capital", {}))

# 4. Smart Auto-PO Restock Generator API
status, auto_po, _ = get_json(f"{BASE_URL}/api/stock/auto-reorder-draft")
test("Auto-PO: Status ready", status == 200 and auto_po.get("status") == "ready")
test("Auto-PO: Low stock detection", auto_po.get("low_stock_count", 0) > 0, f"({auto_po.get('low_stock_count')} SKUs below threshold)")
test("Auto-PO: Preferred vendor recommendation", len(auto_po.get("suggested_vendor", "")) > 0, f"(Vendor: {auto_po.get('suggested_vendor')})")
test("Auto-PO: Reorder quantity economic calculation", all(it.get("suggested_quantity", 0) > 0 for it in auto_po.get("items", [])))

# 5. Customer Credit Ledger & Payment Collection
status, customers, _ = get_json(f"{BASE_URL}/api/customers")
test("Customer Credit: Directory retrieval", status == 200 and len(customers) > 0)
cust = customers[0]
cid = cust.get("customer_id") or cust.get("_id")
test("Customer Credit: Dues & Credit limit fields", "outstanding_dues" in cust and "credit_limit" in cust, f"(Dues: ₹{cust.get('outstanding_dues')}, Limit: ₹{cust.get('credit_limit')})")

status, ledger, _ = get_json(f"{BASE_URL}/api/customers/{cid}/ledger")
test("Customer Ledger: Statement generation", status == 200 and "transactions" in ledger and "dues_status" in ledger)

status, pay_result, _ = post_json(f"{BASE_URL}/api/customers/{cid}/payment", {
    "amount": 100.0,
    "payment_mode": "UPI",
    "reference_no": "UPI-TEST-AUTO",
    "notes": "Automated ledger test repayment"
})
test("Customer Credit: Repayment posting", status == 200 and pay_result.get("payment", {}).get("amount") == 100.0)

# 6. Vendor Bill Payment Tracking
status, purs, _ = get_json(f"{BASE_URL}/api/purchases?limit=5")
test("Purchases: Enriched payment status fields", status == 200 and all("payment_status" in p and "balance_due" in p for p in purs))

unpaid_bill = next((p for p in purs if p.get("payment_status") != "PAID"), purs[0])
target_inv = unpaid_bill.get("invoice_no") or unpaid_bill.get("_id")
status, vpay_result, _ = post_json(f"{BASE_URL}/api/purchases/{target_inv}/payment", {
    "amount": 250.0,
    "payment_mode": "NEFT",
    "reference_no": "NEFT-AUTO-TEST",
    "notes": "Automated accounts payable test"
})
test("Vendor Payment: Bill repayment posting", status == 200 and vpay_result.get("amount_paid", 0) >= 250.0, f"(Status: {vpay_result.get('payment_status')})")

status, unpaid_filter, _ = get_json(f"{BASE_URL}/api/purchases?payment_status=UNPAID")
test("Purchases: Payment status query filter", status == 200 and all(p.get("payment_status") == "UNPAID" for p in unpaid_filter), f"({len(unpaid_filter)} unpaid bills)")

# 7. Frontend UI Integration Elements
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

test("UI HTML: Pure SVG Charts container", "svg-sales-trend-container" in html and "svg-category-donut-container" in html and "svg-stock-gauge-container" in html)
test("UI HTML: Barcode Scanner indicator pill", "barcode-scanner-pill" in html)
test("UI HTML: Auto-PO Restock buttons", "btn-auto-restock-po" in html and "btn-quick-auto-po" in html)
test("UI HTML: Customer Credit Ledger button", "btn-open-customer-ledger" in html)
test("UI HTML: Customer Ledger Modal dialog", "modal-customer-ledger" in html and "modal-cust-select" in html)
test("UI HTML: Vendor Bill Payment Modal dialog", "modal-vendor-payment" in html and "vpay-input-amount" in html)
test("UI HTML: Purchases Payment Status filter dropdown", "purchases-filter-payment-status" in html)

with open("app.js", "r", encoding="utf-8") as f:
    js = f.read()

test("UI JS: Chart renderer functions", "renderSalesTrendSvg" in js and "renderCategoryDonutSvg" in js and "renderStockHealthGaugeSvg" in js)
test("UI JS: Barcode scanner Web Audio API synthesizer", "AudioContext" in js and "createOscillator" in js)
test("UI JS: Auto-PO restock draft population", "initAutoPoRestock" in js and "/api/stock/auto-reorder-draft" in js)
test("UI JS: Customer Credit Ledger modal handler", "initCustomerLedgerModal" in js and "/api/customers/" in js)
test("UI JS: Vendor Bill Payment modal handler", "openVendorPaymentModal" in js and "/api/purchases/" in js)

print("=" * 70)
print(f"MASTER ENHANCEMENT TEST RESULTS: {passed} PASSED, {failed} FAILED")
print("=" * 70)

if failed > 0:
    sys.exit(1)
