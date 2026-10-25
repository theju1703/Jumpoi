import sys
import os
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from seed_mongo import seed_database
from etl_sync import main as run_etl
from src.local_warehouse.sqlite_bq_emulator import LocalWarehouseEmulator
from src.gst_engine.gst_reconciliation import GSTReconciliationEngine
from src.erp_integration.erpnext_sync import ERPNextSyncService
from src.config import MONGO_URI, MONGO_DB_NAME, DUMMY_DATA_DIR
import json

def run_full_pipeline():
    print("=" * 70)
    print("       JOMPOI GROCERY DATA PIPELINE - FULL WORKFLOW RUNNER")
    print("=" * 70)

    # Step 1: Seed MongoDB
    print("\n[STEP 1/5] Seeding Operational MongoDB...")
    seeded = seed_database(MONGO_URI, MONGO_DB_NAME)
    if not seeded:
        print("[!] Note: Seeding skipped or local MongoDB is offline. Continuing with dummy data.")

    # Step 2: Run Local Warehouse Emulator (BigQuery SQL Views)
    print("\n[STEP 2/5] Initializing BigQuery Data Warehouse & Materializing Views...")
    warehouse = LocalWarehouseEmulator()
    warehouse.load_from_json_files(DUMMY_DATA_DIR)

    kpis = warehouse.query_view("vw_executive_kpis")
    if kpis:
        k = kpis[0]
        print(f"  -> Total Revenue:           Rs {k.get('total_revenue', 0):,.2f}")
        print(f"  -> Total Procurement:       Rs {k.get('total_purchase_spend', 0):,.2f}")
        print(f"  -> Gross Profit:            Rs {k.get('gross_profit', 0):,.2f}")
        print(f"  -> Net Output GST:          Rs {k.get('total_output_gst', 0):,.2f}")
        print(f"  -> Total Input GST:         Rs {k.get('total_input_gst', 0):,.2f}")

    stock_pos = warehouse.query_view("vw_stock_position")
    print(f"  -> Tracked Inventory Items: {len(stock_pos)}")
    for s in stock_pos:
        print(f"     * {s['item_code']} ({s['item_name']}): Current Stock = {s['current_stock_qty']} units")

    # Step 3: Run GST Service API Simulation (ITC Reconciliation)
    print("\n[STEP 3/5] Simulating GST Service APIs & ITC Reconciliation (Step 4 & 5)...")
    with open(DUMMY_DATA_DIR / "sales_invoice.json", "r", encoding="utf-8") as f:
        sales = json.load(f)
    with open(DUMMY_DATA_DIR / "purchase_invoice.json", "r", encoding="utf-8") as f:
        purchases = json.load(f)

    gst_engine = GSTReconciliationEngine(sales, purchases)
    gst_report = gst_engine.generate_gst_payment_report()
    print(f"  -> Output GST (Sales):      Rs {gst_report['output_gst_sales']:,.2f}")
    print(f"  -> Input Tax Credit (ITC):  Rs {gst_report['input_gst_purchases']:,.2f}")
    print(f"  -> ITC Utilized:            Rs {gst_report['itc_utilized']:,.2f}")
    print(f"  -> Net Cash Payable:        Rs {gst_report['net_gst_payable_in_cash']:,.2f}")
    print(f"  -> Excess ITC Carried Fwd:  Rs {gst_report['excess_itc_carried_forward']:,.2f}")

    # Step 4: Run ERPNext Integration Service (P&L Generation)
    print("\n[STEP 4/5] Running ERPNext Business System Sync & P&L Generation...")
    with open(DUMMY_DATA_DIR / "items.json", "r", encoding="utf-8") as f:
        items = json.load(f)

    erp_service = ERPNextSyncService(items, sales, purchases)
    pnl = erp_service.generate_profit_and_loss(operating_expenses=850.0)
    print(f"  -> Revenue:                 Rs {pnl['revenue']:,.2f}")
    print(f"  -> Cost of Goods Sold:      Rs {pnl['cost_of_goods_sold']:,.2f}")
    print(f"  -> Gross Profit:            Rs {pnl['gross_profit']:,.2f} ({pnl['gross_profit_margin_percent']}%)")
    print(f"  -> Operating Expenses:      Rs {pnl['operating_expenses']:,.2f}")
    print(f"  -> Net Operating Profit:    Rs {pnl['net_profit']:,.2f}")

    # Step 5: Web Dashboard Info
    print("\n[STEP 5/5] Pipeline Workflow Verification Complete!")
    print("  -> To launch the interactive browser dashboard, run:")
    print("     python scripts/serve_dashboard.py")
    print("=" * 70)

if __name__ == "__main__":
    run_full_pipeline()
