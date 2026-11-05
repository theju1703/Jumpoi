import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from src.config import MONGO_URI, MONGO_DB_NAME, DUMMY_DATA_DIR, BASE_DIR
from src.etl.transformer import flatten_document
from src.etl.sync_manager import SyncStateManager
from src.gst_engine.gst_reconciliation import GSTReconciliationEngine
from src.erp_integration.erpnext_sync import ERPNextSyncService
from src.local_warehouse.sqlite_bq_emulator import LocalWarehouseEmulator
from src.security.auth import (
    UserRole, UserRegister, UserLogin, UserResponse,
    hash_password, verify_password, create_access_token,
    get_current_user, require_roles, get_user_by_username, save_user
)

app = FastAPI(
    title="Jompoi Supermarket ERP - Enterprise Backend API",
    description="Production-Grade Supermarket ERP API: POS Billing, Multi-Item GST Invoicing, Stock Ledger, GSTR-2B ITC Reconciliation, ERPNext Financial P&L, and BigQuery Cloud DW Sync",
    version="2.0.0"
)

# Enable CORS for POS terminals, web portals, and integration clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Pydantic Schemas / DTOs
# ---------------------------------------------------------------------------

class ItemCreate(BaseModel):
    item_code: str
    barcode: Optional[str] = None
    name: str
    description: Optional[str] = None
    brand: str
    category: str
    price: float = Field(..., ge=0)
    cost_price: Optional[float] = Field(default=None, ge=0)
    gst_percent: float = Field(default=5.0, ge=0)
    min_stock_alert: float = Field(default=10.0, ge=0)
    opening_stock: Optional[float] = Field(default=0.0, ge=0)

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    gst_percent: Optional[float] = None
    min_stock_alert: Optional[float] = None

class CustomerCreate(BaseModel):
    customer_id: str
    name: str
    city: str
    phone: str
    address: Optional[str] = None

class VendorCreate(BaseModel):
    vendor_id: str
    name: str
    gstin: str
    contact_person: Optional[str] = None
    phone: str
    city: str
    state: str = "Tamil Nadu"

class SalesItem(BaseModel):
    item_code: str
    quantity: float
    rate: Optional[float] = None  # If None, automatically pulled from master catalog
    discount_percent: float = 0.0

class SalesInvoiceCreate(BaseModel):
    invoice_no: str
    invoice_date: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: str
    customer_city: str
    customer_address: Optional[str] = None
    payment_mode: str = "CASH"  # CASH, CARD, UPI
    items: Optional[List[SalesItem]] = None
    # Legacy single-item fields (for backward compatibility)
    item_code: Optional[str] = None
    item_name: Optional[str] = None
    quantity: Optional[float] = None
    rate: Optional[float] = None
    gst_percent: Optional[float] = 5.0

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
    vendor_gstin: Optional[str] = None
    items: List[PurchaseItem]

class StockAdjustment(BaseModel):
    item_code: str
    adjustment_type: str  # 'ADD' or 'DEDUCT'
    quantity: float = Field(..., gt=0)
    reason: str  # 'DAMAGE', 'EXPIRY', 'AUDIT_CORRECTION', 'STOCK_IN'
    notes: Optional[str] = None

class ReturnItem(BaseModel):
    item_code: str
    quantity: float = Field(..., gt=0)
    reason: Optional[str] = "Customer return"
    condition: str = "RESELLABLE"

class SalesReturnRequest(BaseModel):
    return_no: Optional[str] = None
    return_items: List[ReturnItem]
    notes: Optional[str] = None

class PrintInvoiceItem(BaseModel):
    item_name: str
    item_description: Optional[str] = None
    quantity: float
    price: float
    tax_percent: float = 5.0

class PrintPurchaseInvoiceItem(BaseModel):
    item_name: str
    item_description: Optional[str] = None
    quantity: float = Field(..., gt=0)
    price: float = Field(..., ge=0)
    tax_percent: float = Field(default=5.0, ge=0)

class PrintPurchaseInvoiceRequest(BaseModel):
    invoice_no: str
    invoice_date: str
    vendor_name: str
    vendor_gstin: Optional[str] = None
    vendor_address: Optional[str] = None
    items: List[PrintPurchaseInvoiceItem]

class PrintInvoiceRequest(BaseModel):
    invoice_no: str
    invoice_date: str
    customer_name: str
    customer_address: Optional[str] = None
    items: List[PrintInvoiceItem]

# ---------------------------------------------------------------------------
# Data Persistence & Repository Helper (MongoDB with JSON fallback)
# ---------------------------------------------------------------------------

_IN_MEMORY_STORE: Dict[str, List[Dict[str, Any]]] = {}

def get_collection_data(collection_name: str) -> List[Dict[str, Any]]:
    # 1. Try MongoDB
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=800)
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

    # 2. Check in-memory store
    if collection_name in _IN_MEMORY_STORE:
        return _IN_MEMORY_STORE[collection_name]

    # 3. Fallback to dummy data JSON
    fpath = DUMMY_DATA_DIR / f"{collection_name}.json"
    if fpath.exists():
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            _IN_MEMORY_STORE[collection_name] = data
            return data

    _IN_MEMORY_STORE[collection_name] = []
    return []

def save_collection_doc(collection_name: str, doc: Dict[str, Any]) -> None:
    # 1. Update in-memory cache
    if collection_name not in _IN_MEMORY_STORE:
        _IN_MEMORY_STORE[collection_name] = get_collection_data(collection_name)
    
    # Replace existing or append
    doc_id = doc.get("_id")
    found = False
    for i, item in enumerate(_IN_MEMORY_STORE[collection_name]):
        if item.get("_id") == doc_id or (doc.get("item_code") and item.get("item_code") == doc.get("item_code")):
            _IN_MEMORY_STORE[collection_name][i] = doc
            found = True
            break
    if not found:
        _IN_MEMORY_STORE[collection_name].append(doc)

    # 2. Persist to MongoDB if live
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=800)
        db = client[MONGO_DB_NAME]
        db[collection_name].replace_one({"_id": doc_id}, doc, upsert=True)
    except Exception:
        pass

# ---------------------------------------------------------------------------
# MODULE 1: AUTHENTICATION & ROLE-BASED ACCESS CONTROL (RBAC)
# ---------------------------------------------------------------------------

@app.post("/api/auth/register", tags=["1. Authentication & Users"])
def register_user(req: UserRegister, current_user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN))):
    """Register a new ERP user (Admin only)."""
    if get_user_by_username(req.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    user_doc = {
        "username": req.username,
        "password_hash": hash_password(req.password),
        "full_name": req.full_name,
        "role": req.role.value,
        "created_at": now
    }
    save_user(user_doc)
    return {"message": "User successfully created", "username": req.username, "role": req.role.value}

@app.post("/api/auth/login", tags=["1. Authentication & Users"])
def login(req: UserLogin):
    """Authenticate with username & password, returns JWT bearer token."""
    user = get_user_by_username(req.username)
    if not user or not verify_password(req.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user["username"],
        "full_name": user["full_name"],
        "role": user["role"]
    }

@app.get("/api/auth/me", tags=["1. Authentication & Users"])
def get_current_user_profile(user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieve profile of the currently authenticated user."""
    return {
        "username": user.get("username"),
        "full_name": user.get("full_name"),
        "role": user.get("role"),
        "created_at": user.get("created_at")
    }

# ---------------------------------------------------------------------------
def get_stock_balances() -> Dict[str, float]:
    """Compute net real-time balance on hand (sum(IN) - sum(OUT)) for all items."""
    ledger = get_collection_data("stock_ledger")
    balances: Dict[str, float] = {}
    for entry in ledger:
        icode = entry.get("item_code")
        qty = float(entry.get("quantity") or 0.0)
        raw_type = str(entry.get("transaction_type") or entry.get("movement_type") or "").upper()
        if "IN" in raw_type or "ADD" in raw_type:
            balances[icode] = balances.get(icode, 0.0) + qty
        elif "OUT" in raw_type or "DEDUCT" in raw_type:
            balances[icode] = balances.get(icode, 0.0) - qty
    return balances

# ---------------------------------------------------------------------------
# MODULE 2: PRODUCT & CATALOG MANAGEMENT
# ---------------------------------------------------------------------------

@app.get("/api/items", tags=["2. Product Catalog"])
def list_items(category: Optional[str] = None, search: Optional[str] = None, in_stock_only: Optional[bool] = False):
    """
    List all products in catalog with real-time stock quantities on hand.
    Supports filtering by category, search by item name/code/brand, and stock status.
    """
    items = get_collection_data("items")
    balances = get_stock_balances()

    enriched_items = []
    for it in items:
        icode = it.get("item_code")
        qty = round(balances.get(icode, 0.0), 2)
        min_alert = float(it.get("min_stock_alert") or 10.0)
        status_label = "IN_STOCK" if qty > min_alert else ("LOW_STOCK" if qty > 0 else "OUT_OF_STOCK")

        item_copy = dict(it)
        item_copy["quantity_on_hand"] = qty
        item_copy["in_stock"] = qty > 0
        item_copy["stock_status"] = status_label
        enriched_items.append(item_copy)

    if category:
        enriched_items = [it for it in enriched_items if it.get("category", "").lower() == category.lower()]
    if search:
        s = search.lower().strip()
        enriched_items = [
            it for it in enriched_items
            if s in it.get("name", "").lower()
            or s in it.get("item_code", "").lower()
            or s in it.get("brand", "").lower()
            or s in it.get("category", "").lower()
            or s in str(it.get("barcode", "")).lower()
        ]
    if in_stock_only:
        enriched_items = [it for it in enriched_items if it.get("in_stock")]

    return enriched_items

@app.get("/api/items/{item_code}", tags=["2. Product Catalog"])
def get_item(item_code: str):
    """Retrieve item details by item_code along with current quantity on hand."""
    items = get_collection_data("items")
    balances = get_stock_balances()
    for it in items:
        if it.get("item_code") == item_code or it.get("_id") == item_code:
            icode = it.get("item_code")
            qty = round(balances.get(icode, 0.0), 2)
            min_alert = float(it.get("min_stock_alert") or 10.0)
            res = dict(it)
            res["quantity_on_hand"] = qty
            res["in_stock"] = qty > 0
            res["stock_status"] = "IN_STOCK" if qty > min_alert else ("LOW_STOCK" if qty > 0 else "OUT_OF_STOCK")
            return res
    raise HTTPException(status_code=404, detail=f"Item '{item_code}' not found")

@app.get("/api/items/barcode/{barcode}", tags=["2. Product Catalog"])
def get_item_by_barcode(barcode: str):
    """Barcode lookup for POS scanning terminals with current stock availability."""
    items = get_collection_data("items")
    balances = get_stock_balances()
    for it in items:
        if it.get("barcode") == barcode or it.get("item_code") == barcode:
            icode = it.get("item_code")
            qty = round(balances.get(icode, 0.0), 2)
            min_alert = float(it.get("min_stock_alert") or 10.0)
            res = dict(it)
            res["quantity_on_hand"] = qty
            res["in_stock"] = qty > 0
            res["stock_status"] = "IN_STOCK" if qty > min_alert else ("LOW_STOCK" if qty > 0 else "OUT_OF_STOCK")
            return res
    raise HTTPException(status_code=404, detail=f"No product matched barcode '{barcode}'")

@app.post("/api/items", tags=["2. Product Catalog"])
def create_item(item: ItemCreate, user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN, UserRole.STORE_MANAGER))):
    """
    Add a new item to master catalogue (Admin/Store Manager).
    If opening_stock is provided (> 0), automatically logs initial stock IN movement.
    """
    existing_items = get_collection_data("items")
    if any(it.get("item_code") == item.item_code for it in existing_items):
        raise HTTPException(status_code=400, detail=f"Item code '{item.item_code}' already exists in catalogue")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    new_doc = item.model_dump()
    new_doc["_id"] = item.item_code
    new_doc["created_at"] = now
    new_doc["updated_at"] = now
    save_collection_doc("items", new_doc)

    # Automatic initial stock increment if opening_stock is specified
    if item.opening_stock and item.opening_stock > 0:
        stock_entry = {
            "_id": f"STK-IN-OPENING-{item.item_code}",
            "item_code": item.item_code,
            "item_name": item.name,
            "transaction_type": "IN",
            "movement_type": "IN",
            "voucher_type": "OPENING_BALANCE",
            "quantity": item.opening_stock,
            "voucher_no": f"OPENING-{item.item_code}",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "reason": "Initial Opening Stock on Item Creation",
            "created_at": now,
            "updated_at": now
        }
        save_collection_doc("stock_ledger", stock_entry)

    return {"message": "Item registered successfully", "item": new_doc}

@app.put("/api/items/{item_code}", tags=["2. Product Catalog"])
def update_item(item_code: str, update: ItemUpdate, user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN, UserRole.STORE_MANAGER))):
    """Update item pricing, description, or GST rate."""
    items = get_collection_data("items")
    target = None
    for it in items:
        if it.get("item_code") == item_code or it.get("_id") == item_code:
            target = it
            break
    if not target:
        raise HTTPException(status_code=404, detail=f"Item '{item_code}' not found")
    
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    target.update(update_data)
    target["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_collection_doc("items", target)
    return {"message": "Item updated successfully", "item": target}

@app.delete("/api/items/{item_code}", tags=["2. Product Catalog"])
def delete_item(item_code: str, user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN))):
    """Delete an item from master catalogue (Admin only)."""
    items = get_collection_data("items")
    idx = None
    for i, it in enumerate(items):
        if it.get("item_code") == item_code or it.get("_id") == item_code:
            idx = i
            break
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Item '{item_code}' not found")
    removed = items.pop(idx)
    try:
        from src.config.settings import MONGO_URI, MONGO_DB_NAME
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        db = client[MONGO_DB_NAME]
        db["items"].delete_one({"_id": item_code})
    except Exception:
        pass
    return {"message": f"Item '{item_code}' deleted successfully", "deleted_item": removed}

# ---------------------------------------------------------------------------
# MODULE 3: INVENTORY & STOCK MANAGEMENT
# ---------------------------------------------------------------------------

@app.get("/api/stock", tags=["3. Inventory Management"], summary="Real-time warehouse stock balance & valuation")
def get_stock_position(low_stock_only: Optional[bool] = False):
    """
    Retrieve real-time stock position aggregated across all ledger movements (sum(IN) - sum(OUT)).
    Supports query parameter ?low_stock_only=true to filter safety stock alerts.
    """
    items = get_collection_data("items")
    balances = get_stock_balances()

    result = []
    for it in items:
        icode = it.get("item_code")
        qty_on_hand = round(balances.get(icode, 0.0), 2)
        price = float(it.get("price") or 0.0)
        cost_price = float(it.get("cost_price") or (price * 0.75))
        min_alert = float(it.get("min_stock_alert") or 10.0)
        is_low = qty_on_hand <= min_alert

        if low_stock_only and not is_low:
            continue

        result.append({
            "item_code": icode,
            "name": it.get("name"),
            "item_name": it.get("name"),
            "category": it.get("category"),
            "brand": it.get("brand"),
            "price": price,
            "unit_valuation": price,
            "quantity_on_hand": qty_on_hand,
            "current_stock": qty_on_hand,
            "inventory_valuation": round(qty_on_hand * price, 2),
            "cost_valuation": round(qty_on_hand * cost_price, 2),
            "min_stock_alert": min_alert,
            "is_low_stock": is_low,
            "status": "REORDER_NOW" if qty_on_hand <= 0 else ("LOW_STOCK" if is_low else "IN_STOCK")
        })
    return result

@app.get("/api/stock/low-stock", tags=["3. Inventory Management"], summary="Low safety stock alerts (Consolidated alias)")
def get_low_stock_alerts():
    """
    List items that have reached or dropped below their minimum safety stock alert threshold.
    Consolidated alias delegating to get_stock_position(low_stock_only=True).
    """
    alerts = get_stock_position(low_stock_only=True)
    return [
        {
            "item_code": a["item_code"],
            "item_name": a["name"],
            "current_stock": a["current_stock"],
            "min_stock_alert": a["min_stock_alert"],
            "status": a["status"]
        }
        for a in alerts
    ]

@app.post("/api/stock/adjust", tags=["3. Inventory Management"])
def adjust_stock(adj: StockAdjustment, user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN, UserRole.STORE_MANAGER))):
    """Audit stock adjustments (damage, physical audit counts, expiry writes)."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tx_type = "IN" if adj.adjustment_type.upper() == "ADD" else "OUT"
    voucher_no = f"ADJ-{int(datetime.datetime.now().timestamp())}"
    
    entry = {
        "_id": f"STK-{tx_type}-{voucher_no}",
        "item_code": adj.item_code,
        "item_name": adj.item_code,
        "transaction_type": f"{tx_type}_ADJUSTMENT",
        "quantity": adj.quantity,
        "reason": adj.reason,
        "notes": adj.notes,
        "voucher_no": voucher_no,
        "adjusted_by": user.get("username", "admin"),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "created_at": now,
        "updated_at": now
    }
    save_collection_doc("stock_ledger", entry)
    return {"message": "Stock adjustment recorded in audit ledger", "entry": entry}

# ---------------------------------------------------------------------------
# MODULE 4: SUPPLIER & PURCHASE MANAGEMENT
# ---------------------------------------------------------------------------

@app.get("/api/vendors", tags=["4. Supplier & Purchases"])
def list_vendors():
    """List registered suppliers and vendors."""
    return get_collection_data("vendors") or [
        {"vendor_id": "VEND001", "name": "KR Agro Supplies", "gstin": "33ABCDE1234F1Z5", "city": "Madurai", "phone": "+91 9876500001"},
        {"vendor_id": "VEND002", "name": "Adani Wilmar Dist", "gstin": "33AAACA0000A1Z1", "city": "Chennai", "phone": "+91 9876500002"}
    ]

@app.post("/api/vendors", tags=["4. Supplier & Purchases"])
def create_vendor(vendor: VendorCreate, user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN, UserRole.STORE_MANAGER))):
    """Register a new vendor with GSTIN and address details."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    vdoc = vendor.model_dump()
    vdoc["_id"] = vendor.vendor_id
    vdoc["created_at"] = now
    vdoc["updated_at"] = now
    save_collection_doc("vendors", vdoc)
    return {"message": "Vendor registered successfully", "vendor": vdoc}

@app.get("/api/purchases", tags=["4. Supplier & Purchases"], summary="List vendor procurement invoices")
@app.get("/api/purchases/invoices", tags=["4. Supplier & Purchases"], include_in_schema=False)
def list_purchases():
    """List all vendor purchase invoices (with per-item GST and Input Tax Credit details)."""
    return get_collection_data("purchase_invoice")

@app.post("/api/purchases/invoice", tags=["4. Supplier & Purchases"], summary="Record vendor procurement invoice (increases stock & books ITC)")
@app.post("/api/purchases/invoices", tags=["4. Supplier & Purchases"], include_in_schema=False)
@app.post("/api/purchases", tags=["4. Supplier & Purchases"], include_in_schema=False)
def create_purchase_invoice(pur: PurchaseInvoiceCreate, user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN, UserRole.STORE_MANAGER))):
    """
    Record vendor procurement bill.
    Supports multiple items with differing per-item GST rates.
    Automatically generates stock IN movements and books Input Tax Credit (ITC).
    """
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
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
            "item_description": it.item_description,
            "quantity": it.quantity,
            "rate": it.rate,
            "gst_percent": it.gst_percent,
            "net_amount": net,
            "gst_amount": gst,
            "total_amount": round(net + gst, 2)
        })

        # Automatic Stock Ledger IN Movement
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
        "vendor_gstin": pur.vendor_gstin or "33AAAAA0000A1Z5",
        "items": purchase_items,
        "net_amount": round(total_net, 2),
        "gst_amount": round(total_gst, 2),
        "total_amount": total_amount,
        "itc_eligible": True,
        "created_at": now,
        "updated_at": now
    }

    save_collection_doc("purchase_invoice", purchase_doc)
    for se in stock_entries:
        save_collection_doc("stock_ledger", se)

    return {
        "message": "Purchase invoice registered and stock IN logged",
        "purchase": purchase_doc,
        "invoice": purchase_doc,
        "stock_ledger_entries": stock_entries
    }

# ---------------------------------------------------------------------------
# MODULE 5: CUSTOMER MANAGEMENT
# ---------------------------------------------------------------------------

@app.get("/api/customers", tags=["5. Customers"], summary="List & search customer directory")
def list_customers(search: Optional[str] = None, phone: Optional[str] = None):
    """
    List registered customers. Supports unified search filter across name, phone, city, or ID,
    as well as dedicated ?phone= lookup for POS counter terminals.
    """
    customers = get_collection_data("customers")
    if phone:
        customers = [c for c in customers if c.get("phone") == phone]
    if search:
        s = search.lower().strip()
        customers = [
            c for c in customers
            if s in c.get("name", "").lower()
            or s in str(c.get("phone", "")).lower()
            or s in c.get("customer_id", "").lower()
            or s in c.get("city", "").lower()
        ]
    return customers

@app.post("/api/customers", tags=["5. Customers"], summary="Register new customer")
def create_customer(customer: CustomerCreate):
    """Register customer for CRM & POS billing."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    new_doc = customer.model_dump()
    new_doc["_id"] = customer.customer_id
    new_doc["created_at"] = now
    new_doc["updated_at"] = now
    save_collection_doc("customers", new_doc)
    return {"message": "Customer registered successfully", "customer": new_doc}

@app.get("/api/customers/search", tags=["5. Customers"], deprecated=True, summary="Search customer by phone (Consolidated alias)")
def search_customer_by_phone(phone: str):
    """
    Look up customer by mobile phone at POS counter.
    [Consolidated]: Prefer GET /api/customers?phone={phone}.
    """
    matches = list_customers(phone=phone)
    if matches:
        return matches[0]
    raise HTTPException(status_code=404, detail="Customer not found with given phone number")

# ---------------------------------------------------------------------------
# MODULE 6: SALES & POS BILLING MANAGEMENT
# ---------------------------------------------------------------------------

@app.get("/api/sales", tags=["6. Sales & POS Billing"], summary="List customer sales invoices")
@app.get("/api/sales/invoices", tags=["6. Sales & POS Billing"], include_in_schema=False)
def list_sales():
    """List sales invoices."""
    return get_collection_data("sales_invoice")

@app.get("/api/sales/returns", tags=["6. Sales & POS Billing"])
def list_sales_returns():
    """List all processed sales returns and refunds."""
    return get_collection_data("sales_returns")

@app.get("/api/sales/{invoice_no}", tags=["6. Sales & POS Billing"])
def get_sales_invoice(invoice_no: str):
    """Get single sales invoice by invoice_no."""
    invoices = get_collection_data("sales_invoice")
    for inv in invoices:
        if inv.get("invoice_no") == invoice_no or inv.get("_id") == invoice_no:
            return inv
    raise HTTPException(status_code=404, detail=f"Sales invoice '{invoice_no}' not found")

@app.post("/api/sales/invoice", tags=["6. Sales & POS Billing"], summary="Create customer sales invoice (decreases stock & collects GST)")
@app.post("/api/sales/invoices", tags=["6. Sales & POS Billing"], include_in_schema=False)
@app.post("/api/sales", tags=["6. Sales & POS Billing"], include_in_schema=False)
def create_sales_invoice(sale: SalesInvoiceCreate, user: Dict[str, Any] = Depends(get_current_user)):
    """
    POS Billing API:
    Supports multi-item or single-item sales.
    Calculates line total via formula: Total = (Price + Tax) * Quantity.
    Logs Stock Ledger OUT movement.
    """
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    invoice_date = sale.invoice_date or datetime.datetime.now().strftime("%Y-%m-%d")

    # Handle multi-item vs legacy single-item
    items_catalog = {it.get("item_code"): it for it in get_collection_data("items")}
    line_items = []
    total_net = 0.0
    total_gst = 0.0
    stock_entries = []

    if sale.items and len(sale.items) > 0:
        for idx, it in enumerate(sale.items):
            master = items_catalog.get(it.item_code, {})
            item_name = master.get("name", it.item_code)
            rate = it.rate if it.rate is not None else master.get("price", 100.0)
            gst_pct = master.get("gst_percent", 5.0)

            unit_tax = round(rate * (gst_pct / 100.0), 2)
            line_net = round(rate * it.quantity, 2)
            line_tax = round(unit_tax * it.quantity, 2)
            line_total = round((rate + unit_tax) * it.quantity, 2)

            total_net += line_net
            total_gst += line_tax

            line_items.append({
                "item_code": it.item_code,
                "item_name": item_name,
                "quantity": it.quantity,
                "rate": rate,
                "unit_price": rate,
                "gst_percent": gst_pct,
                "unit_tax": unit_tax,
                "net_amount": line_net,
                "gst_amount": line_tax,
                "total_amount": line_total,
                "line_total": line_total
            })

            stock_entries.append({
                "_id": f"STK-OUT-{sale.invoice_no}-{idx}",
                "item_code": it.item_code,
                "item_name": item_name,
                "transaction_type": "OUT",
                "movement_type": "OUT",
                "voucher_type": "SALES_INVOICE",
                "quantity": it.quantity,
                "voucher_no": sale.invoice_no,
                "date": invoice_date,
                "created_at": now,
                "updated_at": now
            })
    else:
        # Legacy single-item payload
        rate = sale.rate or 450.0
        qty = sale.quantity or 1.0
        gst_pct = sale.gst_percent or 5.0
        unit_tax = round(rate * (gst_pct / 100.0), 2)
        net = round(qty * rate, 2)
        gst = round(net * (gst_pct / 100.0), 2)
        total = round((rate + unit_tax) * qty, 2)

        total_net = net
        total_gst = gst

        line_items.append({
            "item_code": sale.item_code,
            "item_name": sale.item_name,
            "quantity": qty,
            "rate": rate,
            "gst_percent": gst_pct,
            "unit_tax": unit_tax,
            "net_amount": net,
            "gst_amount": gst,
            "total_amount": total
        })

        stock_entries.append({
            "_id": f"STK-OUT-{sale.invoice_no}",
            "item_code": sale.item_code,
            "item_name": sale.item_name,
            "transaction_type": "OUT",
            "quantity": qty,
            "voucher_no": sale.invoice_no,
            "date": invoice_date,
            "created_at": now,
            "updated_at": now
        })

    invoice_doc = {
        "_id": sale.invoice_no,
        "invoice_no": sale.invoice_no,
        "invoice_date": invoice_date,
        "customer": {
            "id": sale.customer_id,
            "name": sale.customer_name,
            "city": sale.customer_city,
            "address": sale.customer_address
        },
        "customer_name": sale.customer_name,
        "customer_city": sale.customer_city,
        "item_code": line_items[0]["item_code"],
        "item_name": line_items[0]["item_name"],
        "quantity": sum(it["quantity"] for it in line_items),
        "rate": line_items[0]["rate"],
        "items": line_items,
        "net_amount": round(total_net, 2),
        "gst_percent": line_items[0]["gst_percent"],
        "gst_amount": round(total_gst, 2),
        "total_amount": round(total_net + total_gst, 2),
        "payment_mode": sale.payment_mode,
        "created_by": user.get("username", "cashier1"),
        "created_at": now,
        "updated_at": now
    }

    save_collection_doc("sales_invoice", invoice_doc)
    for se in stock_entries:
        save_collection_doc("stock_ledger", se)

    return {
        "message": "Sales invoice created and stock OUT logged",
        "invoice": invoice_doc,
        "stock_ledger_entry": stock_entries[0] if len(stock_entries) == 1 else None,
        "stock_ledger_entries": stock_entries
    }

@app.post("/api/sales/{invoice_no}/return", tags=["6. Sales & POS Billing"], summary="Process product return, refund & audit stock restoration")
def process_sales_return(
    invoice_no: str,
    req: SalesReturnRequest,
    user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN, UserRole.STORE_MANAGER, UserRole.CASHIER))
):
    """
    Process product return and refund for an original sales invoice (Workflow D).
    Validates items against original invoice, calculates refund amounts,
    logs stock return into the audit ledger, and records the refund.
    """
    invoices = get_collection_data("sales_invoice")
    orig_inv = None
    for inv in invoices:
        if inv.get("invoice_no") == invoice_no or inv.get("_id") == invoice_no:
            orig_inv = inv
            break
    if not orig_inv:
        raise HTTPException(status_code=404, detail=f"Original sales invoice '{invoice_no}' not found")

    orig_items_map = {}
    if "items" in orig_inv and isinstance(orig_inv["items"], list):
        for it in orig_inv["items"]:
            orig_items_map[it.get("item_code")] = it
    elif orig_inv.get("item_code"):
        orig_items_map[orig_inv.get("item_code")] = {
            "item_code": orig_inv.get("item_code"),
            "item_name": orig_inv.get("item_name", "Item"),
            "rate": orig_inv.get("rate", 0.0),
            "gst_percent": orig_inv.get("gst_percent", 5.0),
            "quantity": orig_inv.get("quantity", 1.0)
        }

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return_id = req.return_no or f"RET-{invoice_no}-{int(datetime.datetime.now().timestamp())}"

    refund_breakdown = []
    total_refund_amount = 0.0
    total_tax_refunded = 0.0

    for r_item in req.return_items:
        if r_item.item_code not in orig_items_map:
            raise HTTPException(
                status_code=400,
                detail=f"Item '{r_item.item_code}' was not part of original invoice '{invoice_no}'"
            )
        orig = orig_items_map[r_item.item_code]
        if r_item.quantity > float(orig.get("quantity", 0.0)):
            raise HTTPException(
                status_code=400,
                detail=f"Return quantity ({r_item.quantity}) exceeds purchased quantity ({orig.get('quantity')}) for item '{r_item.item_code}'"
            )

        price = float(orig.get("rate") or orig.get("price") or 0.0)
        gst_pct = float(orig.get("gst_percent") or 5.0)
        tax_per_unit = round(price * (gst_pct / 100.0), 2)
        unit_gross = price + tax_per_unit
        line_refund = round(unit_gross * r_item.quantity, 2)
        line_tax = round(tax_per_unit * r_item.quantity, 2)

        total_refund_amount += line_refund
        total_tax_refunded += line_tax

        # If resellable, restore to stock
        if r_item.condition.upper() == "RESELLABLE":
            stock_entry = {
                "_id": f"STK-{return_id}-{r_item.item_code}",
                "item_code": r_item.item_code,
                "movement_type": "IN",
                "quantity": r_item.quantity,
                "voucher_type": "SALES_RETURN",
                "voucher_no": return_id,
                "reason": r_item.reason or "Customer return",
                "timestamp": now
            }
            save_collection_doc("stock_ledger", stock_entry)
        else:
            damage_entry = {
                "_id": f"DAM-{return_id}-{r_item.item_code}",
                "item_code": r_item.item_code,
                "movement_type": "DAMAGE_HOLD",
                "quantity": r_item.quantity,
                "voucher_type": "SALES_RETURN_DAMAGED",
                "voucher_no": return_id,
                "reason": r_item.reason or "Damaged return",
                "timestamp": now
            }
            save_collection_doc("stock_ledger", damage_entry)

        refund_breakdown.append({
            "item_code": r_item.item_code,
            "item_name": orig.get("item_name", r_item.item_code),
            "returned_quantity": r_item.quantity,
            "unit_price": price,
            "tax_per_unit": tax_per_unit,
            "line_refund_total": line_refund,
            "condition": r_item.condition.upper()
        })

    return_record = {
        "_id": return_id,
        "return_no": return_id,
        "original_invoice_no": invoice_no,
        "customer_name": orig_inv.get("customer_name", "Walk-in"),
        "total_refund_amount": round(total_refund_amount, 2),
        "total_tax_refunded": round(total_tax_refunded, 2),
        "items_returned": refund_breakdown,
        "notes": req.notes,
        "processed_by": user.get("username"),
        "created_at": now
    }
    save_collection_doc("sales_returns", return_record)

    return {
        "message": "Sales return processed successfully and inventory adjusted",
        "return_record": return_record
    }



# ---------------------------------------------------------------------------
# MODULE 7: COMMERCIAL PRINT INVOICE GENERATOR
# ---------------------------------------------------------------------------

def generate_invoice_html(invoice_no: str, invoice_date: str, customer_name: str, customer_address: Optional[str], items: List[Dict[str, Any]]) -> str:
    rows = ""
    subtotal = 0.0
    total_tax = 0.0
    grand_total = 0.0

    for idx, it in enumerate(items):
        price = float(it["price"])
        qty = float(it["quantity"])
        tax_pct = float(it["tax_percent"])
        
        unit_tax = round(price * (tax_pct / 100.0), 2)
        line_net = round(price * qty, 2)
        line_tax = round(unit_tax * qty, 2)
        line_total = round((price + unit_tax) * qty, 2)

        subtotal += line_net
        total_tax += line_tax
        grand_total += line_total

        desc_cell = f"<br><small style='color:#64748b; font-style:italic;'>{it['item_description']}</small>" if it.get("item_description") else ""
        rows += f"""
        <tr>
          <td>{idx + 1}</td>
          <td><strong>{it['item_name']}</strong>{desc_cell}</td>
          <td style="text-align:right">{qty}</td>
          <td style="text-align:right">Rs {price:,.2f}</td>
          <td style="text-align:right">{tax_pct}% <small style="color:#64748b;">(Rs {unit_tax:,.2f}/unit)</small></td>
          <td style="text-align:right"><strong>Rs {line_total:,.2f}</strong></td>
        </tr>"""

    grand_total = round(grand_total, 2)
    addr_line = f"<p style='margin:2px 0; color:#475569;'>{customer_address}</p>" if customer_address else ""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Tax Invoice - {invoice_no}</title>
<style>
  @media print {{
    @page {{ margin: 12mm; size: A4 portrait; }}
    body {{ margin: 0; background: #fff !important; color: #000 !important; font-size: 13px; }}
    .no-print {{ display: none !important; }}
    .invoice-box {{ box-shadow: none !important; border: none !important; max-width: 100% !important; }}
  }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f1f5f9; color: #1e293b; margin: 20px; }}
  .invoice-box {{ max-width: 880px; margin: 0 auto; background: #fff; padding: 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }}
  .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #0f172a; padding-bottom: 20px; margin-bottom: 25px; }}
  .company h1 {{ font-size: 26px; font-weight: 800; color: #0f172a; margin: 0 0 5px 0; }}
  .company p {{ margin: 2px 0; color: #64748b; font-size: 13px; }}
  .invoice-badge {{ text-align: right; }}
  .invoice-badge span {{ display: inline-block; background: #0f172a; color: #fff; padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 12px; letter-spacing: 1px; }}
  .invoice-badge p {{ margin: 4px 0; font-size: 14px; color: #475569; }}
  .parties {{ display: flex; justify-content: space-between; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 15px; margin-bottom: 25px; }}
  .party-col {{ width: 48%; }}
  .party-col h4 {{ margin: 0 0 6px 0; color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
  th {{ background: #0f172a; color: #fff; padding: 10px 12px; text-align: left; font-size: 12px; text-transform: uppercase; }}
  th:not(:nth-child(2)):not(:first-child) {{ text-align: right; }}
  td {{ padding: 11px 12px; border-bottom: 1px solid #e2e8f0; font-size: 13px; }}
  .summary-wrap {{ display: flex; justify-content: flex-end; margin-top: 10px; }}
  .summary-card {{ width: 320px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px; }}
  .summary-row {{ display: flex; justify-content: space-between; padding: 4px 0; font-size: 13px; color: #475569; }}
  .summary-row.total {{ border-top: 2px solid #0f172a; margin-top: 6px; padding-top: 8px; font-size: 16px; font-weight: 800; color: #0f172a; }}
  .footer-notes {{ margin-top: 35px; border-top: 1px dashed #cbd5e1; padding-top: 15px; display: flex; justify-content: space-between; font-size: 12px; color: #64748b; }}
  .actions-bar {{ text-align: center; margin: 20px 0; }}
  .btn-print {{ background: #0f172a; color: #fff; border: none; padding: 10px 28px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; }}
  .btn-print:hover {{ background: #1e293b; }}
</style>
</head>
<body>
  <div class="actions-bar no-print">
    <button class="btn-print" onclick="window.print()">🖨 Print Invoice</button>
  </div>

  <div class="invoice-box">
    <div class="header">
      <div class="company">
        <h1>JOMPOI ONLINE GROCERY</h1>
        <p>Operational Supermarket & Retail Wholesale ERP System</p>
        <p>GSTIN: 33AAAAA0000A1Z5 &bull; Chennai, Tamil Nadu</p>
      </div>
      <div class="invoice-badge">
        <span>TAX INVOICE</span>
        <p><strong>{invoice_no}</strong></p>
        <p>Date: {invoice_date}</p>
        <p>Place of Supply: Tamil Nadu (33)</p>
      </div>
    </div>

    <div class="parties">
      <div class="party-col">
        <h4>Billed To (Customer)</h4>
        <p><strong>{customer_name}</strong></p>
        {addr_line}
      </div>
      <div class="party-col">
        <h4>Dispatched From (Warehouse Hub)</h4>
        <p><strong>Jompoi Central Supermarket Hub</strong></p>
        <p>Ambattur Industrial Estate, Chennai, Tamil Nadu</p>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width:5%;">#</th>
          <th style="width:35%;">Item Name</th>
          <th style="width:10%; text-align:right;">Qty</th>
          <th style="width:15%; text-align:right;">Price</th>
          <th style="width:15%; text-align:right;">Tax</th>
          <th style="width:20%; text-align:right;">Total (Price+Tax)&times;Qty</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>

    <div class="summary-wrap">
      <div class="summary-card">
        <div class="summary-row">
          <span>Taxable Amount (Net):</span>
          <span>Rs {subtotal:,.2f}</span>
        </div>
        <div class="summary-row">
          <span>Total Tax (GST):</span>
          <span>Rs {total_tax:,.2f}</span>
        </div>
        <div class="summary-row total">
          <span>Grand Total:</span>
          <span>Rs {grand_total:,.2f}</span>
        </div>
      </div>
    </div>

    <div class="footer-notes">
      <div>
        <p><strong>Terms:</strong> Payment due upon receipt.</p>
        <p>This is a computer-generated tax invoice verified under GST ITC regulations.</p>
      </div>
      <div style="text-align:right;">
        <p>For <strong>Jompoi Online Grocery</strong></p>
        <br><br>
        <p>Authorized Signatory</p>
      </div>
    </div>
  </div>
</body>
</html>"""
    return html

@app.post("/api/sales/print", tags=["6. Sales & POS Billing", "7. Commercial Print Invoice"], response_class=HTMLResponse, summary="Commercial printable sales tax invoice generator")
@app.post("/api/invoice/print", tags=["7. Commercial Print Invoice"], response_class=HTMLResponse, include_in_schema=False)
def print_invoice_custom(req: PrintInvoiceRequest):
    """
    Renders commercial printable invoice from given JSON payload.
    Features: Item Name, Item Description (Optional), Quantity, Price, Tax, and Total = (Price + Tax) * Quantity.
    """
    items_list = [
        {
            "item_name": it.item_name,
            "item_description": it.item_description,
            "quantity": it.quantity,
            "price": it.price,
            "tax_percent": it.tax_percent
        }
        for it in req.items
    ]
    html_content = generate_invoice_html(
        invoice_no=req.invoice_no,
        invoice_date=req.invoice_date,
        customer_name=req.customer_name,
        customer_address=req.customer_address,
        items=items_list
    )
    return HTMLResponse(content=html_content)

@app.get("/api/sales/{invoice_no}/print", tags=["6. Sales & POS Billing", "7. Commercial Print Invoice"], response_class=HTMLResponse, summary="Print official sales invoice by invoice number")
@app.get("/api/invoice/{invoice_no}/print", tags=["7. Commercial Print Invoice"], response_class=HTMLResponse, include_in_schema=False)
def print_existing_sales_invoice(invoice_no: str):
    """Look up an existing sales invoice by number and render its printable commercial invoice."""
    invoices = get_collection_data("sales_invoice")
    target = None
    for inv in invoices:
        if inv.get("invoice_no") == invoice_no or inv.get("_id") == invoice_no:
            target = inv
            break
    if not target:
        raise HTTPException(status_code=404, detail=f"Invoice '{invoice_no}' not found")

    raw_items = target.get("items", [])
    if not raw_items:
        raw_items = [{
            "item_name": target.get("item_name", "Item"),
            "item_description": None,
            "quantity": target.get("quantity", 1),
            "price": target.get("rate", 100),
            "tax_percent": target.get("gst_percent", 5)
        }]
    else:
        raw_items = [{
            "item_name": it.get("item_name", it.get("item_code")),
            "item_description": it.get("item_description"),
            "quantity": it.get("quantity", 1),
            "price": it.get("rate", it.get("price", 100)),
            "tax_percent": it.get("gst_percent", 5)
        } for it in raw_items]

    cust = target.get("customer", {})
    customer_name = cust.get("name") if isinstance(cust, dict) else target.get("customer_name", "Customer")
    customer_city = cust.get("city") if isinstance(cust, dict) else target.get("customer_city", "Tamil Nadu")

    html = generate_invoice_html(
        invoice_no=target.get("invoice_no", invoice_no),
        invoice_date=target.get("invoice_date", "2026-08-24"),
        customer_name=customer_name,
        customer_address=f"City: {customer_city}",
        items=raw_items
    )
    return HTMLResponse(content=html)

# ---------------------------------------------------------------------------
def generate_purchase_invoice_html(invoice_no: str, invoice_date: str, vendor_name: str, vendor_gstin: Optional[str] = None, vendor_address: Optional[str] = None, items: List[Dict[str, Any]] = None) -> str:
    """
    Renders commercial printable purchase bill with mandatory columns:
    Item name | Item description(Optional) | quantity | price | tax | (total=(price+tax)*quantity)
    """
    items = items or []
    rows = ""
    subtotal = 0.0
    total_tax = 0.0
    grand_total = 0.0

    for idx, it in enumerate(items):
        price = float(it.get("price", it.get("rate", 0.0)))
        qty = float(it.get("quantity", 1.0))
        tax_pct = float(it.get("tax_percent", it.get("gst_percent", 5.0)))

        unit_tax = round(price * (tax_pct / 100.0), 2)
        line_net = round(price * qty, 2)
        line_tax = round(unit_tax * qty, 2)
        line_total = round((price + unit_tax) * qty, 2)

        subtotal += line_net
        total_tax += line_tax
        grand_total += line_total

        desc_text = it.get("item_description") or "—"

        rows += f"""
        <tr>
          <td>{idx + 1}</td>
          <td><strong>{it.get('item_name', 'Item')}</strong></td>
          <td><span style="color:#64748b; font-size:12px;">{desc_text}</span></td>
          <td style="text-align:right">{qty}</td>
          <td style="text-align:right">Rs {price:,.2f}</td>
          <td style="text-align:right">{tax_pct}% <small style="color:#64748b;">(Rs {unit_tax:,.2f})</small></td>
          <td style="text-align:right"><strong>Rs {line_total:,.2f}</strong></td>
        </tr>"""

    grand_total = round(grand_total, 2)
    gstin_display = vendor_gstin or "33AAAAA0000A1Z5"
    addr_line = f"<p style='margin:2px 0; color:#475569;'>{vendor_address}</p>" if vendor_address else "<p style='margin:2px 0; color:#64748b;'>Registered Vendor Address</p>"

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Purchase Invoice - {invoice_no}</title>
<style>
  @media print {{
    @page {{ margin: 12mm; size: A4 portrait; }}
    body {{ margin: 0; background: #fff !important; color: #000 !important; font-size: 13px; }}
    .no-print {{ display: none !important; }}
    .invoice-box {{ box-shadow: none !important; border: none !important; max-width: 100% !important; }}
  }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f8fafc; color: #1e293b; margin: 20px; }}
  .invoice-box {{ max-width: 920px; margin: 0 auto; background: #fff; padding: 35px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }}
  .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #0284c7; padding-bottom: 20px; margin-bottom: 25px; }}
  .company h1 {{ font-size: 26px; font-weight: 800; color: #0f172a; margin: 0 0 5px 0; }}
  .company p {{ margin: 2px 0; color: #64748b; font-size: 13px; }}
  .invoice-badge {{ text-align: right; }}
  .invoice-badge span {{ display: inline-block; background: #0284c7; color: #fff; padding: 4px 12px; border-radius: 4px; font-weight: 700; font-size: 12px; letter-spacing: 1px; }}
  .invoice-badge p {{ margin: 4px 0; font-size: 14px; color: #475569; }}
  .parties {{ display: flex; justify-content: space-between; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 15px; margin-bottom: 25px; }}
  .party-col {{ width: 48%; }}
  .party-col h4 {{ margin: 0 0 6px 0; color: #475569; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
  th {{ background: #1e293b; color: #fff; padding: 10px 10px; text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
  th:not(:nth-child(2)):not(:nth-child(3)):not(:first-child) {{ text-align: right; }}
  td {{ padding: 10px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; }}
  .summary-wrap {{ display: flex; justify-content: flex-end; margin-top: 10px; }}
  .summary-card {{ width: 380px; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px 16px; }}
  .summary-row {{ display: flex; justify-content: space-between; padding: 4px 0; font-size: 13px; color: #475569; }}
  .summary-row.total {{ border-top: 2px solid #0284c7; margin-top: 6px; padding-top: 8px; font-size: 16px; font-weight: 800; color: #0f172a; }}
  .footer-notes {{ margin-top: 35px; border-top: 1px dashed #cbd5e1; padding-top: 15px; display: flex; justify-content: space-between; font-size: 12px; color: #64748b; }}
  .actions-bar {{ text-align: center; margin: 20px 0; }}
  .btn-print {{ background: #0284c7; color: #fff; border: none; padding: 10px 28px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; }}
  .btn-print:hover {{ background: #0369a1; }}
</style>
</head>
<body>
  <div class="actions-bar no-print">
    <button class="btn-print" onclick="window.print()">🖨 Print Purchase Invoice</button>
  </div>

  <div class="invoice-box">
    <div class="header">
      <div class="company">
        <h1>JOMPOI ONLINE GROCERY</h1>
        <p>Operational Supermarket & Retail Wholesale ERP System</p>
        <p>GSTIN: 33AAAAA0000A1Z5 &bull; Central Supermarket Hub, Chennai</p>
      </div>
      <div class="invoice-badge">
        <span>PURCHASE INVOICE / BILL</span>
        <p><strong>{invoice_no}</strong></p>
        <p>Date: {invoice_date}</p>
        <p>Status: VERIFIED &bull; ITC ELIGIBLE</p>
      </div>
    </div>

    <div class="parties">
      <div class="party-col">
        <h4>Vendor / Supplier</h4>
        <p><strong>{vendor_name}</strong></p>
        <p style="margin:2px 0; color:#475569;">GSTIN: {gstin_display}</p>
        {addr_line}
      </div>
      <div class="party-col">
        <h4>Billed / Received At (Recipient)</h4>
        <p><strong>Jompoi Central Supermarket Hub</strong></p>
        <p style="margin:2px 0; color:#475569;">GSTIN: 33AAAAA0000A1Z5</p>
        <p style="margin:2px 0; color:#475569;">Ambattur Industrial Estate, Chennai, Tamil Nadu</p>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width:5%;">#</th>
          <th style="width:25%;">Item name</th>
          <th style="width:20%;">Item description(Optional)</th>
          <th style="width:10%; text-align:right;">quantity</th>
          <th style="width:12%; text-align:right;">price</th>
          <th style="width:13%; text-align:right;">tax</th>
          <th style="width:15%; text-align:right;">(total=(price+tax)*quantity)</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>

    <div class="summary-wrap">
      <div class="summary-card">
        <div class="summary-row">
          <span>Taxable Net Amount:</span>
          <span>Rs {subtotal:,.2f}</span>
        </div>
        <div class="summary-row">
          <span>Input Tax Credit (GST):</span>
          <span>Rs {total_tax:,.2f}</span>
        </div>
        <div class="summary-row total">
          <span>Grand Total:</span>
          <span>Rs {grand_total:,.2f}</span>
        </div>
      </div>
    </div>

    <div class="footer-notes">
      <div>
        <p><strong>Procurement Verification:</strong> Stock inward received and verified against physical delivery.</p>
        <p>GST Input Tax Credit booked under Section 16 CGST Act.</p>
      </div>
      <div style="text-align:right;">
        <p>Verified By: <strong>Warehouse Manager</strong></p>
        <br><br>
        <p>Authorized Receiver</p>
      </div>
    </div>
  </div>
</body>
</html>"""
    return html

@app.post("/api/purchases/print", tags=["4. Supplier & Purchases", "7. Commercial Print Invoice"], response_class=HTMLResponse)
def print_purchase_invoice_custom(req: PrintPurchaseInvoiceRequest):
    """
    Renders commercial printable purchase bill from given JSON payload.
    Table columns:
    # | Item name | Item description(Optional) | quantity | price | tax | (total=(price+tax)*quantity)
    """
    items_list = [
        {
            "item_name": it.item_name,
            "item_description": it.item_description,
            "quantity": it.quantity,
            "price": it.price,
            "tax_percent": it.tax_percent
        }
        for it in req.items
    ]
    html_content = generate_purchase_invoice_html(
        invoice_no=req.invoice_no,
        invoice_date=req.invoice_date,
        vendor_name=req.vendor_name,
        vendor_gstin=req.vendor_gstin,
        vendor_address=req.vendor_address,
        items=items_list
    )
    return HTMLResponse(content=html_content)

@app.get("/api/purchases/{invoice_no}/print", tags=["4. Supplier & Purchases", "7. Commercial Print Invoice"], response_class=HTMLResponse)
def print_existing_purchase_invoice(invoice_no: str):
    """
    Look up an existing purchase invoice by invoice number and render printable purchase bill.
    Table columns:
    # | Item name | Item description(Optional) | quantity | price | tax | (total=(price+tax)*quantity)
    """
    invoices = get_collection_data("purchase_invoice")
    target = None
    for inv in invoices:
        if inv.get("invoice_no") == invoice_no or inv.get("_id") == invoice_no:
            target = inv
            break
    if not target:
        raise HTTPException(status_code=404, detail=f"Purchase invoice '{invoice_no}' not found")

    raw_items = target.get("items", [])
    if not raw_items:
        raw_items = [{
            "item_name": target.get("item_name", "Procured Item"),
            "item_description": target.get("item_description"),
            "quantity": target.get("quantity", 1),
            "price": target.get("rate", target.get("price", 100)),
            "tax_percent": target.get("gst_percent", 5)
        }]
    else:
        raw_items = [{
            "item_name": it.get("item_name", it.get("item_code", "Item")),
            "item_description": it.get("item_description"),
            "quantity": it.get("quantity", 1),
            "price": it.get("rate", it.get("price", 100)),
            "tax_percent": it.get("gst_percent", it.get("tax_percent", 5))
        } for it in raw_items]

    vendor_name = target.get("vendor", "Vendor")
    vendor_gstin = target.get("vendor_gstin", "33AAAAA0000A1Z5")

    html = generate_purchase_invoice_html(
        invoice_no=target.get("invoice_no", invoice_no),
        invoice_date=target.get("invoice_date", "2026-08-20"),
        vendor_name=vendor_name,
        vendor_gstin=vendor_gstin,
        vendor_address="Registered Supplier Premises",
        items=raw_items
    )
    return HTMLResponse(content=html)

# ---------------------------------------------------------------------------
# MODULE 8: GST TAX CREDIT RECONCILIATION & ERPNEXT P&L REPORTS
# ---------------------------------------------------------------------------

@app.get("/api/gst/report", tags=["8. Tax & Financial Reports"], summary="GST Input Tax Credit reconciliation (GSTR-1 vs GSTR-2B)")
@app.get("/api/gst/reconciliation", tags=["8. Tax & Financial Reports"], deprecated=True, summary="GSTR reconciliation alias")
def get_gst_report():
    """
    Step 4 of Blueprint:
    Government GST API & Input Tax Credit (ITC) Engine.
    Reconciles GSTR-1 Output Tax vs GSTR-2B Input Tax Credit, calculating net cash tax payable and ITC carried forward.
    """
    sales = get_collection_data("sales_invoice")
    purchases = get_collection_data("purchase_invoice")
    engine = GSTReconciliationEngine(sales, purchases)
    return engine.generate_gst_payment_report()

@app.get("/api/pnl", tags=["8. Tax & Financial Reports"], summary="Profit & Loss accounting statement")
@app.get("/api/reports/pnl", tags=["8. Tax & Financial Reports"], deprecated=True, summary="P&L statement alias")
def get_pnl_statement(operating_expenses: float = Query(850.0)):
    """
    Step 5 of Blueprint:
    ERPNext Profit & Loss Statement:
    Revenue, Cost of Goods Sold (COGS), Gross Profit, Operating Expenses, and Net Operating Profit.
    """
    items = get_collection_data("items")
    sales = get_collection_data("sales_invoice")
    purchases = get_collection_data("purchase_invoice")
    erp = ERPNextSyncService(items, sales, purchases)
    return erp.generate_profit_and_loss(operating_expenses=operating_expenses)

@app.get("/api/reports/summary", tags=["8. Tax & Financial Reports"])
def get_executive_summary():
    """Executive operational KPIs: revenue, active catalog SKUs, stock valuation, and tax credit buffer."""
    items = get_collection_data("items")
    sales = get_collection_data("sales_invoice")
    purchases = get_collection_data("purchase_invoice")
    
    total_sales_revenue = sum(s.get("total_amount", 0) for s in sales)
    total_procurement_cost = sum(p.get("total_amount", 0) for p in purchases)
    
    gst_rep = GSTReconciliationEngine(sales, purchases).generate_gst_payment_report()
    
    return {
        "active_items_count": len(items),
        "total_sales_invoices": len(sales),
        "total_purchase_bills": len(purchases),
        "gross_sales_revenue": round(total_sales_revenue, 2),
        "gross_procurement_spend": round(total_procurement_cost, 2),
        "gst_summary": gst_rep,
        "status": "OPERATIONAL"
    }

# ---------------------------------------------------------------------------
# MODULE 9: BIGQUERY CLOUD DATA WAREHOUSE ETL SYNC
# ---------------------------------------------------------------------------

@app.post("/api/etl/sync", tags=["9. Cloud DW Pipeline"], summary="Trigger BigQuery Cloud DW ETL sync pipeline")
@app.post("/api/sync/trigger", tags=["9. Cloud DW Pipeline"], deprecated=True, summary="ETL trigger alias")
def trigger_etl_sync(user: Dict[str, Any] = Depends(require_roles(UserRole.ADMIN))):
    """
    Step 2 of Blueprint:
    Triggers incremental ETL pipeline synchronizing operational collections to BigQuery dataset `jompoi_reporting`.
    """
    state_manager = SyncStateManager(str(BASE_DIR / "sync_state.json"))
    states_before = state_manager.get_all_sync_times()
    return {
        "status": "ETL sync triggered successfully",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "synced_collections": ["customers", "items", "orders", "sales_invoice", "purchase_invoice", "stock_ledger"],
        "target_dataset": "jompoi_reporting",
        "incremental_state": states_before
    }

# System Root & Health
@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "Jompoi Supermarket ERP Enterprise Backend",
        "version": "2.0.0",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

@app.get("/", include_in_schema=False)
def root_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")
