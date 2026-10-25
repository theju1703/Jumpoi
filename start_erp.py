import os
import sys
import webbrowser
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.config import MONGO_URI, MONGO_DB_NAME, DUMMY_DATA_DIR
from src.local_warehouse.sqlite_bq_emulator import LocalWarehouseEmulator
from src.gst_engine.gst_reconciliation import GSTReconciliationEngine
from src.erp_integration.erpnext_sync import ERPNextSyncService

PORT = 8080

def print_cli_erp_report():
    import json
    print("\n" + "=" * 78)
    print("      JOMPOI ERP BUSINESS SYSTEM - CLIENT ARCHITECTURE DEMONSTRATION")
    print("      (Based on Operational Grocery Backend -> Google Cloud -> ERPNext)")
    print("=" * 78)

    warehouse = LocalWarehouseEmulator()
    warehouse.load_from_json_files(DUMMY_DATA_DIR)

    with open(DUMMY_DATA_DIR / "items.json", "r", encoding="utf-8") as f:
        items = json.load(f)
    with open(DUMMY_DATA_DIR / "sales_invoice.json", "r", encoding="utf-8") as f:
        sales = json.load(f)
    with open(DUMMY_DATA_DIR / "purchase_invoice.json", "r", encoding="utf-8") as f:
        purchases = json.load(f)

    # 1. Operational Master & Transaction Summary
    print("\n[BLOCK 1] JOMPOI OPERATIONAL SYSTEM (MongoDB)")
    print(f"  * Master Items:        {len(items)} items in catalog")
    print(f"  * Sales Invoices:      {len(sales)} customer invoices")
    print(f"  * Purchase Invoices:   {len(purchases)} vendor bills")

    # 2. Daily Cloud Sync
    print("\n[BLOCK 2 & 3] GOOGLE CLOUD & ERPNEXT REGULAR SYNC")
    print("  * Cloud DB:            BigQuery Dataset `jompoi_reporting`")
    print("  * ERPNext Sync Status: Synchronized (Items, Sales, Purchases)")

    # 3. GST API Simulation & ITC
    gst_engine = GSTReconciliationEngine(sales, purchases)
    gst_report = gst_engine.generate_gst_payment_report()
    print("\n[BLOCK 4] GST SERVICE (GOVERNMENT APIs - ITC RECONCILIATION)")
    print(f"  * Output GST (Sales / GSTR-1):       Rs {gst_report['output_gst_sales']:>10,.2f}")
    print(f"  * Input Tax Credit (ITC / GSTR-2B):  Rs {gst_report['input_gst_purchases']:>10,.2f}")
    print(f"  * Eligible ITC Utilized:             Rs {gst_report['itc_utilized']:>10,.2f}")
    print(f"  * Net Cash Payable to Govt:          Rs {gst_report['net_gst_payable_in_cash']:>10,.2f}")
    print(f"  * Excess ITC Carried Forward:        Rs {gst_report['excess_itc_carried_forward']:>10,.2f}")

    # 4. ERPNext Financial Output: P&L
    erp_service = ERPNextSyncService(items, sales, purchases)
    pnl = erp_service.generate_profit_and_loss(operating_expenses=850.0)
    print("\n[BLOCK 5] ERPNEXT FINANCIAL OUTPUT: PROFIT & LOSS STATEMENT")
    print("-" * 55)
    print(f"  Gross Sales Revenue:                 Rs {pnl['revenue']:>10,.2f}")
    print(f"  Less: Cost of Goods Sold (COGS):     Rs {pnl['cost_of_goods_sold']:>10,.2f}")
    print(f"  ---------------------------------------------------")
    print(f"  Gross Profit:                        Rs {pnl['gross_profit']:>10,.2f} ({pnl['gross_profit_margin_percent']}%)")
    print(f"  Less: Operating Expenses:            Rs {pnl['operating_expenses']:>10,.2f}")
    print(f"  ===================================================")
    print(f"  NET OPERATING PROFIT:                Rs {pnl['net_profit']:>10,.2f}")
    print("=" * 78 + "\n")

def start_server():
    print_cli_erp_report()
    print("-------------------------------------------------------------------")
    print(" Launching Jompoi ERP Web Application for Antigravity IDE:")
    print(f" -> Local ERP URL:     http://localhost:{PORT}")
    print(f" -> REST API Docs:     http://localhost:{PORT}/docs")
    print("-------------------------------------------------------------------")
    print("Opening ERP Dashboard in your default browser automatically...")
    webbrowser.open(f"http://localhost:{PORT}")

    try:
        import uvicorn
        from src.api.main import app
        uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")
    except Exception as e:
        import http.server
        import socketserver
        WEB_DIR = BASE_DIR / "web"
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(WEB_DIR), **kwargs)
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nERP Server stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Jompoi ERP System")
    parser.add_argument("--cli", action="store_true", help="Print CLI report only and exit")
    args = parser.parse_args()

    if args.cli:
        print_cli_erp_report()
    else:
        start_server()
