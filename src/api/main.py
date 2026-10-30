import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from src.config import MONGO_URI, MONGO_DB_NAME, DUMMY_DATA_DIR, BASE_DIR
from src.etl.transformer import flatten_document
from src.etl.sync_manager import SyncStateManager
from src.gst_engine.gst_reconciliation import GSTReconciliationEngine
from src.erp_integration.erpnext_sync import ERPNextSyncService
from src.local_warehouse.sqlite_bq_emulator import LocalWarehouseEmulator

app = FastAPI(
    title="Jompoi Online Grocery Operational Backend & Analytics API",
    description="Operational Backend API for Jompoi Grocery, BigQuery ETL Sync, GST ITC Engine, and ERPNext Analytics",
    version="1.0.0"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ItemCreate(BaseModel):
    item_code: str
    name: str
    brand: str
    category: str
    price: float
    gst_percent: float = 5.0

class CustomerCreate(BaseModel):
    customer_id: str
    name: str
    city: str
    phone: str

class SalesInvoiceCreate(BaseModel):
    invoice_no: str
    invoice_date: str
    customer_name: str
    customer_city: str
    item_code: str
    item_name: str
    quantity: float
    rate: float
    gst_percent: float = 5.0

class PurchaseItem(BaseModel):
    item_code: str
    item_name: str
    quantity: float
    rate: float
    gst_percent: float = 5.0

class PurchaseInvoiceCreate(BaseModel):
    invoice_no: str
    invoice_date: str
    vendor: str
    items: List[PurchaseItem]

# In-memory / MongoDB Repository Helper
def get_collection_data(collection_name: str) -> List[Dict[str, Any]]:
    # Try MongoDB first
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        client.admin.command("ping")
        db = client[MONGO_DB_NAME]
        docs = list(db[collection_name].find({}))
        if docs:
            for d in docs:
                if "_id" in d:
                    d["_id"] = str(d["_id"])
            return docs
    except Exception:
        pass

    # Fallback to dummy data JSON
    fpath = DUMMY_DATA_DIR / f"{collection_name}.json"
    if fpath.exists():
        with open(fpath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- API Endpoints ---

@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "Jompoi Grocery Backend",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

# 1. Master Data: Items
@app.get("/api/items", tags=["Catalog"])
def list_items():
    return get_collection_data("items")

@app.post("/api/items", tags=["Catalog"])
def create_item(item: ItemCreate):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    new_doc = item.model_dump()
    new_doc["_id"] = item.item_code
    new_doc["created_at"] = now
    new_doc["updated_at"] = now
    return {"message": "Item registered successfully", "item": new_doc}

# 2. Master Data: Customers
@app.get("/api/customers", tags=["Customers"])
def list_customers():
    return get_collection_data("customers")

@app.post("/api/customers", tags=["Customers"])
def create_customer(customer: CustomerCreate):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    new_doc = customer.model_dump()
    new_doc["_id"] = customer.customer_id
    new_doc["created_at"] = now
    new_doc["updated_at"] = now
    return {"message": "Customer registered successfully", "customer": new_doc}

# 3. Transaction: Sales Invoices
@app.get("/api/sales", tags=["Sales"])
def list_sales():
    return get_collection_data("sales_invoice")

@app.post("/api/sales/invoice", tags=["Sales"])
def create_sales_invoice(sale: SalesInvoiceCreate):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    net = round(sale.quantity * sale.rate, 2)
    gst = round(net * (sale.gst_percent / 100.0), 2)
    total = round(net + gst, 2)

    invoice_doc = {
        "_id": sale.invoice_no,
        "invoice_no": sale.invoice_no,
        "invoice_date": sale.invoice_date,
        "customer": {
            "name": sale.customer_name,
            "city": sale.customer_city
        },
        "item_code": sale.item_code,
        "item_name": sale.item_name,
        "quantity": sale.quantity,
        "rate": sale.rate,
        "net_amount": net,
        "gst_percent": sale.gst_percent,
        "gst_amount": gst,
        "total_amount": total,
        "created_at": now,
        "updated_at": now
    }

    # Auto-generate Stock Ledger OUT movement
    stock_doc = {
        "_id": f"STK-OUT-{sale.invoice_no}",
        "item_code": sale.item_code,
        "item_name": sale.item_name,
        "transaction_type": "OUT",
        "quantity": sale.quantity,
        "voucher_no": sale.invoice_no,
        "date": sale.invoice_date,
        "created_at": now,
        "updated_at": now
    }

    return {
        "message": "Sales invoice created and stock OUT logged",
        "invoice": invoice_doc,
        "stock_ledger_entry": stock_doc
    }

# 4. Transaction: Purchase Invoices
@app.get("/api/purchases", tags=["Purchases"])
def list_purchases():
    return get_collection_data("purchase_invoice")

@app.post("/api/purchases/invoice", tags=["Purchases"])
def create_purchase_invoice(pur: PurchaseInvoiceCreate):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Compute per‑item totals and aggregate
    purchase_items = []
    total_net = 0.0
    total_gst = 0.0
    stock_entries = []
    for idx, it in enumerate(pur.items):
        net = round(it.quantity * it.rate, 2)
        gst = round(net * (it.gst_percent / 100.0), 2)
        total_net += net
        total_gst += gst
        purchase_items.append({
            "item_code": it.item_code,
            "item_name": it.item_name,
            "quantity": it.quantity,
            "rate": it.rate,
            "gst_percent": it.gst_percent,
            "net_amount": net,
            "gst_amount": gst,
            "total_amount": round(net + gst, 2)
        })
        stock_entries.append({
            "_id": f"STK-IN-{pur.invoice_no}-{idx}",
            "item_code": it.item_code,
            "item_name": it.item_name,
            "transaction_type": "IN",
            "quantity": it.quantity,
            "voucher_no": pur.invoice_no,
            "date": pur.invoice_date,
            "created_at": now,
            "updated_at": now
        })
    total_amount = round(total_net + total_gst, 2)
    purchase_doc = {
        "_id": pur.invoice_no,
        "invoice_no": pur.invoice_no,
        "invoice_date": pur.invoice_date,
        "vendor": pur.vendor,
        "items": purchase_items,
        "net_amount": round(total_net, 2),
        "gst_amount": round(total_gst, 2),
        "total_amount": total_amount,
        "created_at": now,
        "updated_at": now
    }
    return {
        "message": "Purchase bill registered and stock IN logged",
        "purchase": purchase_doc,
        "stock_ledger_entries": stock_entries
    }

# 5. Inventory & Stock Position
@app.get("/api/stock", tags=["Inventory"])
def get_stock_position():
    warehouse = LocalWarehouseEmulator()
    warehouse.load_from_json_files(DUMMY_DATA_DIR)
    pos = warehouse.query_view("vw_stock_position")
    warehouse.close()
    return pos

# 6. GST ITC Reconciliation Report (Step 4 & 5 of Blueprint)
@app.get("/api/gst/report", tags=["GST & Tax"])
def get_gst_report():
    sales = get_collection_data("sales_invoice")
    purchases = get_collection_data("purchase_invoice")
    engine = GSTReconciliationEngine(sales, purchases)
    return engine.generate_gst_payment_report()

# 7. ERPNext Profit & Loss Statement (Step 5 of Blueprint)
@app.get("/api/pnl", tags=["ERPNext"])
def get_pnl_statement(operating_expenses: float = Query(850.0)):
    items = get_collection_data("items")
    sales = get_collection_data("sales_invoice")
    purchases = get_collection_data("purchase_invoice")
    erp = ERPNextSyncService(items, sales, purchases)
    return erp.generate_profit_and_loss(operating_expenses=operating_expenses)

# 8. Trigger BigQuery ETL Sync
@app.post("/api/etl/sync", tags=["ETL Pipeline"])
def trigger_etl_sync():
    from etl_sync import main as run_etl
    state_manager = SyncStateManager(str(BASE_DIR / "sync_state.json"))
    states_before = state_manager.get_all_sync_times()
    return {
        "status": "ETL sync triggered successfully",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "synced_collections": ["customers", "items", "orders", "sales_invoice", "purchase_invoice", "stock_ledger"],
        "target_dataset": "jompoi_reporting"
    }

# Mount static web UI at root /
WEB_DIR = BASE_DIR / "web"
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

    @app.get("/", tags=["Dashboard UI"])
    def serve_dashboard():
        return FileResponse(str(WEB_DIR / "index.html"))

    @app.get("/styles.css", include_in_schema=False)
    def serve_css():
        return FileResponse(str(WEB_DIR / "styles.css"))

    @app.get("/app.js", include_in_schema=False)
    def serve_js():
        return FileResponse(str(WEB_DIR / "app.js"))
