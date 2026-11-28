import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8080"

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def get_csv(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read().decode("utf-8"), resp.headers.get("Content-Disposition")

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

print("=" * 70)
print("RUNNING END-TO-END ERP-WIDE FILTERING, SEARCH, SORT & EXPORT TESTS")
print("=" * 70)

# 1. Health check
status, data = get_json(f"{BASE_URL}/api/health")
test("API Health Status", status == 200 and data.get("status") == "healthy")

# 2. Items API Filtering
status, all_items = get_json(f"{BASE_URL}/api/items")
test("Items: Base retrieval", status == 200 and len(all_items) > 0, f"({len(all_items)} items)")

status, search_items = get_json(f"{BASE_URL}/api/items?search=Rice")
test("Items: Search filter by 'Rice'", status == 200 and all("rice" in i.get("name","").lower() or "rice" in i.get("category","").lower() for i in search_items), f"({len(search_items)} matches)")

status, cat_items = get_json(f"{BASE_URL}/api/items?category=Edible%20Oils")
test("Items: Category filter 'Edible Oils'", status == 200 and all(i.get("category") == "Edible Oils" for i in cat_items), f"({len(cat_items)} matches)")

status, stock_items = get_json(f"{BASE_URL}/api/items?stock_status=IN_STOCK")
test("Items: Stock status filter 'IN_STOCK'", status == 200 and all(i.get("quantity_on_hand", 0) > 0 for i in stock_items), f"({len(stock_items)} matches)")

status, sorted_items = get_json(f"{BASE_URL}/api/items?sort_by=price&sort_order=desc")
test("Items: Price sorting DESC", status == 200 and sorted_items[0]["price"] >= sorted_items[-1]["price"], f"(Top: {sorted_items[0]['price']}, Bottom: {sorted_items[-1]['price']})")

status, paged_items = get_json(f"{BASE_URL}/api/items?limit=2&offset=0")
test("Items: Pagination limit=2", status == 200 and len(paged_items) == 2)

# 3. Purchases API Filtering
status, all_pur = get_json(f"{BASE_URL}/api/purchases")
test("Purchases: Base retrieval", status == 200 and len(all_pur) > 0, f"({len(all_pur)} purchases)")

status, vendor_pur = get_json(f"{BASE_URL}/api/purchases?vendor=KR%20Agro%20Supplies")
test("Purchases: Vendor filter 'KR Agro Supplies'", status == 200 and all("KR Agro" in p.get("vendor","") for p in vendor_pur), f"({len(vendor_pur)} bills)")

status, date_pur = get_json(f"{BASE_URL}/api/purchases?start_date=2026-08-01&end_date=2026-08-25")
test("Purchases: Date range filter", status == 200 and len(date_pur) > 0, f"({len(date_pur)} bills)")

status, sorted_pur = get_json(f"{BASE_URL}/api/purchases?sort_by=total_amount&sort_order=desc")
test("Purchases: Amount sorting DESC", status == 200 and sorted_pur[0]["total_amount"] >= sorted_pur[-1]["total_amount"])

# 4. Sales API Filtering
status, all_sales = get_json(f"{BASE_URL}/api/sales")
test("Sales: Base retrieval", status == 200 and len(all_sales) > 0, f"({len(all_sales)} sales)")

status, search_sales = get_json(f"{BASE_URL}/api/sales?search=ABC%20Stores")
test("Sales: Customer search filter", status == 200 and all("ABC" in str(s) for s in search_sales), f"({len(search_sales)} invoices)")

status, date_sales = get_json(f"{BASE_URL}/api/sales?start_date=2026-08-20&end_date=2026-08-25")
test("Sales: Date range filter", status == 200 and len(date_sales) > 0, f"({len(date_sales)} invoices)")

# 5. Inventory Movement Ledger API
status, all_ledger = get_json(f"{BASE_URL}/api/stock/ledger")
test("Inventory: Stock ledger base retrieval", status == 200 and len(all_ledger) > 0, f"({len(all_ledger)} entries)")

status, in_ledger = get_json(f"{BASE_URL}/api/stock/ledger?movement_type=IN")
test("Inventory: Movement filter 'IN'", status == 200 and len(in_ledger) > 0 and all(("IN" in str(e.get("transaction_type") or "").upper() or "IN" in str(e.get("movement_type") or "").upper() or "ADD" in str(e.get("transaction_type") or "").upper() or "PURCHASE" in str(e.get("transaction_type") or "").upper() or "OPENING" in str(e.get("transaction_type") or "").upper()) for e in in_ledger), f"({len(in_ledger)} IN entries)")

status, out_ledger = get_json(f"{BASE_URL}/api/stock/ledger?movement_type=OUT")
test("Inventory: Movement filter 'OUT'", status == 200 and len(out_ledger) > 0 and all(("OUT" in str(e.get("transaction_type") or "").upper() or "OUT" in str(e.get("movement_type") or "").upper() or "DEDUCT" in str(e.get("transaction_type") or "").upper() or "SALE" in str(e.get("transaction_type") or "").upper() or "DAMAGE" in str(e.get("transaction_type") or "").upper()) for e in out_ledger), f"({len(out_ledger)} OUT entries)")

# 6. GST and PnL Reports
status, gst_report = get_json(f"{BASE_URL}/api/gst/report")
test("GST Report: Generation", status == 200 and "output_gst_sales" in gst_report and "input_gst_purchases" in gst_report, f"(Output: {gst_report.get('output_gst_sales')}, ITC: {gst_report.get('input_gst_purchases')})")

status, pnl_report = get_json(f"{BASE_URL}/api/pnl")
test("P&L Statement: Generation", status == 200 and "revenue" in pnl_report and "net_profit" in pnl_report, f"(Revenue: {pnl_report.get('revenue')}, Net Profit: {pnl_report.get('net_profit')})")

# 7. CSV Export Endpoints
modules_to_test = ["items", "purchases", "sales", "inventory", "gst", "pnl"]
for mod in modules_to_test:
    status, csv_text, disp = get_csv(f"{BASE_URL}/api/export/{mod}/csv")
    test(f"Export CSV: Module '{mod}'", status == 200 and len(csv_text.strip().splitlines()) >= 2 and f"{mod}_export.csv" in (disp or ""), f"({len(csv_text.strip().splitlines())} lines)")

# 8. Frontend HTML & CSS Assertions
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

test("HTML: Items Filter Card & Inputs", "items-filter-search" in html_content and "items-filter-category" in html_content and "items-filter-stock" in html_content)
test("HTML: Purchases Filter Card & Presets", "purchases-filter-search" in html_content and "purchases-filter-vendor" in html_content and 'data-module="purchases"' in html_content)
test("HTML: Sales Filter Card & Presets", "sales-filter-search" in html_content and "sales-filter-customer" in html_content and 'data-module="sales"' in html_content)
test("HTML: Inventory Filter Card & Presets", "inv-filter-search" in html_content and "inv-filter-item" in html_content and 'data-module="inventory"' in html_content)
test("HTML: GST Filter Card", "gst-filter-date-from" in html_content and "gst-filter-vendor" in html_content)
test("HTML: PnL Filter Card & Opex Input", "pnl-filter-date-from" in html_content and "pnl-input-opex" in html_content)
test("HTML: Sortable Headers with icons", "sortable-th" in html_content and "sort-icon" in html_content)
test("HTML: Pagination Containers on all tables", "items-pagination-bar" in html_content and "purchases-pagination-bar" in html_content and "sales-pagination-bar" in html_content and "inv-pagination-bar" in html_content)
test("HTML: CSV Export Buttons on all modules", "btn-export-items-csv" in html_content and "btn-export-purchases-csv" in html_content and "btn-export-sales-csv" in html_content and "btn-export-inventory-csv" in html_content and "btn-export-gst-csv" in html_content and "btn-export-pnl-csv" in html_content)

# 9. Frontend JavaScript Assertions
with open("app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

test("JS: Multi-module state object", "erpState" in js_content and "pageSize" in js_content)
test("JS: Date Presets helper", "getDatePresetRange" in js_content and "THIS_WEEK" in js_content and "THIS_MONTH" in js_content)
test("JS: Sorter helper & header listeners", "sortRecords" in js_content and "setupSortableHeaders" in js_content)
test("JS: Paginator helper", "renderPagination" in js_content)
test("JS: Client-side CSV Exporter", "exportDataToCSV" in js_content)
test("JS: Dynamic KPI cards update", "stat-stock-valuation" in js_content and "pur-kpi-count" in js_content and "sales-kpi-count" in js_content and "inv-kpi-movements" in js_content)
test("JS: Preserved Add to Bill button", "btn-add-bill-item" in js_content and "currentBillItems" in js_content)

print("=" * 70)
print(f"RESULTS: {passed} PASSED, {failed} FAILED")
print("=" * 70)

if failed > 0:
    sys.exit(1)
