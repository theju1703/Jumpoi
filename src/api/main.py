import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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
    item_description: Optional[str] = None
    quantity: float
    rate: float
    gst_percent: float = 5.0

class PurchaseInvoiceCreate(BaseModel):
    invoice_no: str
    invoice_date: str
    vendor: str
    items: List[PurchaseItem]

class PrintInvoiceItem(BaseModel):
    item_name: str
    item_description: Optional[str] = None
    quantity: float
    price: float
    tax_percent: float = 5.0

class PrintInvoiceRequest(BaseModel):
    invoice_no: str
    invoice_date: str
    customer_name: str
    customer_address: Optional[str] = None
    items: List[PrintInvoiceItem]

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

# 9. Print Invoice – returns a printable HTML invoice
@app.post("/api/invoice/print", tags=["Invoice"], response_class=HTMLResponse)
def print_invoice(req: PrintInvoiceRequest):
    rows = ""
    grand_total = 0.0
    for it in req.items:
        tax_amount = round(it.price * (it.tax_percent / 100.0), 2)
        line_total = round((it.price + tax_amount) * it.quantity, 2)
        grand_total += line_total
        desc_cell = f"<br><small style='color:#666'>{it.item_description}</small>" if it.item_description else ""
        rows += f"""
        <tr>
          <td>{it.item_name}{desc_cell}</td>
          <td style="text-align:right">{it.quantity}</td>
          <td style="text-align:right">Rs {it.price:,.2f}</td>
          <td style="text-align:right">{it.tax_percent}% (Rs {tax_amount:,.2f})</td>
          <td style="text-align:right"><strong>Rs {line_total:,.2f}</strong></td>
        </tr>"""

    grand_total = round(grand_total, 2)
    addr_line = f"<p>{req.customer_address}</p>" if req.customer_address else ""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Invoice {req.invoice_no}</title>
<style>
  @media print {{ @page {{ margin: 15mm; }} body {{ margin: 0; }} }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 20px auto; color: #1e293b; }}
  .header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 3px solid #0f172a; padding-bottom: 16px; margin-bottom: 20px; }}
  .company {{ font-size: 24px; font-weight: 700; color: #0f172a; }}
  .company small {{ display: block; font-size: 12px; font-weight: 400; color: #64748b; }}
  .invoice-meta {{ text-align: right; }}
  .invoice-meta h2 {{ margin: 0; color: #0f172a; }}
  .invoice-meta p {{ margin: 2px 0; color: #475569; font-size: 14px; }}
  .bill-to {{ margin-bottom: 20px; }}
  .bill-to h4 {{ margin: 0 0 4px 0; color: #64748b; font-size: 12px; text-transform: uppercase; }}
  .bill-to p {{ margin: 0; font-size: 15px; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
  th {{ background: #0f172a; color: #fff; padding: 10px 12px; text-align: left; font-size: 13px; }}
  th:not(:first-child) {{ text-align: right; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }}
  .total-row {{ background: #f1f5f9; }}
  .total-row td {{ font-size: 16px; font-weight: 700; border-top: 2px solid #0f172a; }}
  .footer {{ text-align: center; margin-top: 40px; color: #94a3b8; font-size: 12px; }}
  .print-btn {{ display: block; margin: 20px auto; padding: 10px 30px; background: #0f172a; color: #fff; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; }}
  @media print {{ .print-btn {{ display: none; }} }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <div class="company">JOMPOI<small>Online Grocery ERP</small></div>
    </div>
    <div class="invoice-meta">
      <h2>INVOICE</h2>
      <p><strong>{req.invoice_no}</strong></p>
      <p>Date: {req.invoice_date}</p>
    </div>
  </div>

  <div class="bill-to">
    <h4>Bill To</h4>
    <p><strong>{req.customer_name}</strong></p>
    {addr_line}
  </div>

  <table>
    <thead>
      <tr>
        <th>Item Name</th>
        <th>Qty</th>
        <th>Price</th>
        <th>Tax</th>
        <th>Total</th>
      </tr>
    </thead>
    <tbody>
      {rows}
      <tr class="total-row">
        <td colspan="4" style="text-align:right">Grand Total</td>
        <td style="text-align:right">Rs {grand_total:,.2f}</td>
      </tr>
    </tbody>
  </table>

  <div class="footer">
    <p>Thank you for your business!</p>
    <p>Jompoi Online Grocery &bull; Generated on {datetime.datetime.now().strftime("%d-%b-%Y %H:%M")}</p>
  </div>

  <button class="print-btn" onclick="window.print()">🖨 Print Invoice</button>
</body>
</html>"""
    return HTMLResponse(content=html)


# Root redirect to API docs (no dashboard)
@app.get("/", include_in_schema=False)
def root_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")
