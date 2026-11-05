# Jompoi Supermarket ERP - Backend REST API

This folder provides direct documentation, launch scripts, and testing instructions for the **Jompoi Supermarket ERP Backend API**.

---

## 🚀 Starting the Backend API

To launch the backend server locally:

```bash
# Using the dedicated launcher:
python api/run_api.py

# Or using uvicorn directly:
uvicorn src.api.main:app --host 0.0.0.0 --port 8080 --reload
```

Once running:
- **Interactive Swagger UI Documentation:** [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc Alternative:** [http://localhost:8080/redoc](http://localhost:8080/redoc)
- **OpenAPI JSON Spec:** [http://localhost:8080/openapi.json](http://localhost:8080/openapi.json)
- **Hosted GitHub Pages ERP System:** [https://theju1703.github.io/Jumpoi/](https://theju1703.github.io/Jumpoi/)
- **Hosted API Documentation:** [https://theju1703.github.io/Jumpoi/docs.html](https://theju1703.github.io/Jumpoi/docs.html)
- **Android APK Direct Download:** [https://github.com/theju1703/Jumpoi/raw/main/apk/jumpoi.apk](https://github.com/theju1703/Jumpoi/raw/main/apk/jumpoi.apk)

---

## 🧪 Automated Testing

To run the full enterprise QA test suite (44 tests covering inventory lifecycle, positive/negative scenarios, GST reconciliation, invoice printing, and security):

```bash
python -m pytest tests/ -v
```

---

## 📋 Comprehensive API Endpoints Catalog

### 1. Authentication & Role-Based Access Control (RBAC)
- `POST /api/auth/login`: Authenticate with username and password, returns JWT bearer token.
- `POST /api/auth/register`: Register a new ERP user (Admin-only).
- `GET /api/auth/me`: Retrieve current user profile and role permissions.

### 2. Product Catalog & Real-Time Stock Analytics
- `GET /api/items`: List all catalog products with real-time stock balances on hand ($\sum \text{IN} - \sum \text{OUT}$), status (`IN_STOCK`, `LOW_STOCK`, `OUT_OF_STOCK`), search by item name/code/brand, and `in_stock_only` filters.
- `GET /api/items/{item_code}`: Retrieve single product details including real-time `quantity_on_hand` and `stock_status`.
- `GET /api/items/barcode/{barcode}`: High-speed barcode lookup for POS scanning terminals with current quantity on hand.
- `POST /api/items`: Create/register a new product with SKU, barcode, price, GST rate, and optional `opening_stock` (Admin/Manager). When `opening_stock > 0`, automatically logs stock IN into the inventory ledger.
- `PUT /api/items/{item_code}`: Update product pricing or metadata (Admin/Manager).
- `DELETE /api/items/{item_code}`: Remove product from catalog (Admin-only).

### 3. Inventory & Stock Lifecycle Management
- **Automatic Stock Lifecycle:**
  - **Item Registration:** When created with opening stock, stock increases.
  - **Vendor Procurement:** When purchased from vendor (`POST /api/purchases/invoice`), stock increases by procured quantity.
  - **POS Customer Sale:** When sold to customer (`POST /api/sales/invoice`), stock decreases by sold quantity.
- `GET /api/stock`: Real-time stock position, quantity on hand ($\sum \text{IN} - \sum \text{OUT}$), retail valuation, and reorder status.
- `GET /api/stock/low-stock`: Filter items currently below minimum safety stock levels.
- `POST /api/stock/adjust`: Record manual inventory audit adjustments, damage write-offs, or physical count corrections.

### 4. Supplier & Purchase Management (with Bill Printing)
- `GET /api/vendors`: List registered suppliers with GSTIN and contact details.
- `POST /api/vendors`: Register a new supplier/vendor.
- `GET /api/purchases` or `GET /api/purchases/invoices`: List inward purchase procurement bills with Input Tax Credit (ITC).
- `POST /api/purchases/invoice` or `POST /api/purchases/invoices`: Record inward vendor purchase, automatically increasing item stock and booking Input Tax Credit.
- `GET /api/purchases/{invoice_no}/print`: Render printable Purchase Invoice with client's exact required columns:
  `#` | `Item name` | `Item description(Optional)` | `quantity` | `price` | `tax` | `(total=(price+tax)*quantity)`
- `POST /api/purchases/print`: Custom printable Purchase Bill generator with exact formula $\text{Total} = (\text{Price} + \text{Tax}) \times \text{Quantity}$.

### 5. Sales & POS Billing Management
- `GET /api/sales` or `GET /api/sales/invoices`: List all sales invoices.
- `GET /api/sales/{invoice_no}`: Retrieve single sales invoice details.
- `POST /api/sales/invoice` or `POST /api/sales/invoices`: Create POS billing transaction with per-item tax formula $\text{Total} = (\text{Price} + \text{Tax}) \times \text{Quantity}$ and automatic stock deduction.
- `POST /api/sales/{invoice_no}/return`: Process product return, validate refund eligibility, restore stock for resellable items, and record audit ledger.
- `GET /api/sales/returns`: List all processed customer returns and refunds.

### 6. Commercial Tax Invoice Generator
- `POST /api/invoice/print`: Calculate and generate printable HTML Sales Tax Invoice from custom input line items.
- `GET /api/invoice/{invoice_no}/print`: Render printable HTML Sales Tax Invoice for an existing database invoice.

### 7. Tax & Financial Reports
- `GET /api/gst/report` or `GET /api/gst/reconciliation`: Government GSTR-1 vs GSTR-2B Input Tax Credit reconciliation.
- `GET /api/pnl` or `GET /api/reports/pnl`: Profit & Loss statement (Revenue, COGS, Gross Profit, Operating Expenses, Net Operating Profit).
- `GET /api/reports/summary`: Executive operational KPIs.

### 8. Cloud Data Warehouse ETL Sync
- `POST /api/sync/trigger`: Trigger incremental ETL pipeline syncing MongoDB transactions to Google Cloud BigQuery.
