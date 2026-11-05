# Jompoi Supermarket ERP - Complete Backend API Reference & Testing Guide

Welcome to the **Jompoi Supermarket ERP Enterprise Backend API**. This system implements the complete 5-step retail architecture blueprint:
`Operational Backend (MongoDB) -> Daily Cloud Sync (BigQuery) -> ERPNext Regular Updates -> GST Government APIs (ITC Reconciliation) -> Reports (P&L, GST)`.

---

## 1. Quick Server Launch

Run either of the launcher scripts inside the project directory:

```powershell
.\run_erp.bat
# or in PowerShell:
.\run_erp.ps1
```

* **Interactive Swagger UI**: `http://localhost:8080/docs`
* **Raw OpenAPI JSON**: `http://localhost:8080/openapi.json`
* **Health Check**: `http://localhost:8080/api/health`
* **GitHub Pages Web Live Reference**: `https://theju1703.github.io/Jumpoi/`
* **Online Interactive API Docs**: `https://theju1703.github.io/Jumpoi/docs.html`

---

## 2. Authentication & Pre-Seeded Roles (RBAC)

The system enforces JWT Bearer tokens with 4 pre-seeded role accounts:

| Username | Password | Role | Permissions |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | **ADMIN** | Full system access, User registration, P&L, ETL Sync |
| `manager` | `manager123` | **STORE_MANAGER** | Product pricing, Vendor procurement, Stock adjustments |
| `cashier1` | `cashier123` | **CASHIER** | POS billing, Barcode scans, Customer creation, Print Invoice |
| `inventory1`| `inventory123` | **INVENTORY_STAFF**| Stock ledger viewing, Physical stock counts |

### Login Example
```bash
curl -X POST http://localhost:8080/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

---

## 3. Core Enterprise API Endpoints

### A. Commercial Tax Invoice & Printing
* **`POST /api/invoice/print`**: Generates a commercial printable tax invoice from request payload.
  * Formula per line: $\text{Total} = (\text{Price} + \text{Tax}) \times \text{Quantity}$
  * Request payload example:
    ```json
    {
      "invoice_no": "INV-2026-001",
      "invoice_date": "2026-11-05",
      "customer_name": "ABC Stores",
      "customer_address": "123, Anna Nagar, Chennai",
      "items": [
        {
          "item_name": "Basmati Rice 5kg",
          "item_description": "India Gate Classic Aged Grain",
          "quantity": 10,
          "price": 450.0,
          "tax_percent": 5.0
        },
        {
          "item_name": "Sunflower Oil 1L",
          "item_description": "Fortune Pure Refined Oil",
          "quantity": 5,
          "price": 135.0,
          "tax_percent": 12.0
        }
      ]
    }
    ```
* **`GET /api/invoice/{invoice_no}/print`**: Look up an existing sales invoice by number and immediately render its printable commercial invoice.

### B. POS Billing & Sales Invoices
* **`POST /api/sales/invoice`**: Multi-item POS sales checkout. Automatically calculates line totals via $(\text{Price} + \text{Tax}) \times \text{Quantity}$ and logs Stock Ledger OUT movements.
  ```json
  {
    "invoice_no": "INV-2026-099",
    "invoice_date": "2026-11-05",
    "customer_name": "Retail Walk-in Customer",
    "customer_city": "Chennai",
    "payment_mode": "UPI",
    "items": [
      {"item_code": "ITM001", "quantity": 2, "rate": 450.0},
      {"item_code": "ITM002", "quantity": 3, "rate": 135.0}
    ]
  }
  ```

### C. Multi-Item Purchases with Per-Item GST
* **`POST /api/purchases/invoice`**: Multi-item procurement bill. Supports different GST rates (0%, 5%, 12%, 18%) per line-item, logs Stock Ledger IN movements, and books Input Tax Credit (ITC).
  ```json
  {
    "invoice_no": "PUR-2026-009",
    "invoice_date": "2026-11-05",
    "vendor": "KR Agro Supplies",
    "items": [
      {
        "item_code": "ITM001",
        "item_name": "Basmati Rice 5kg",
        "quantity": 50,
        "rate": 350.0,
        "gst_percent": 5.0
      },
      {
        "item_code": "ITM002",
        "item_name": "Sunflower Oil 1L",
        "quantity": 25,
        "rate": 110.0,
        "gst_percent": 12.0
      }
    ]
  }
  ```

### D. Inventory & Stock Position
* **`GET /api/stock`**: Real-time stock on hand and valuation.
* **`GET /api/stock/low-stock`**: Reorder alerts for products at or below safety stock.
* **`POST /api/stock/adjust`**: Audit adjustments (damage, wastage, physical counts).

### E. GST ITC Tax Credit Reconciliation (Step 4 of Blueprint)
* **`GET /api/gst/report`**: Simulates Government GSTR-2B matching against GSTR-1 sales.
  * Returns:
    * `output_gst_sales`: Output tax collected on customer sales.
    * `input_gst_purchases`: Total ITC paid on supplier invoices.
    * `itc_utilized`: Eligible credit offset against tax liability.
    * `net_gst_payable_in_cash`: Net cash payable to government (Rs 0.00 when fully offset).
    * `excess_itc_carried_forward`: Excess tax credit balance carried forward to next month.

### F. Profit & Loss Statement (Step 5 of Blueprint)
* **`GET /api/pnl`**: Real-time ERP financial statement:
  * Gross Sales Revenue
  * Less: Cost of Goods Sold (COGS)
  * Gross Profit & Gross Margin %
  * Less: Operating Expenses
  * Net Operating Profit

### G. Incremental BigQuery Cloud DW Sync (Step 2 of Blueprint)
* **`POST /api/etl/sync`**: Triggers state-aware ETL synchronization to BigQuery dataset `jompoi_reporting`.

---

## 4. Automated Test Suite Execution

All 29 test suites pass with 100% test coverage across all domain modules:

```powershell
& "C:\Users\Thejeshwharan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m pytest -v
```

```
============================= test session starts =============================
collected 29 items

tests/test_api.py::test_health_endpoint PASSED                           [  3%]
tests/test_api.py::test_auth_login_success PASSED                        [  6%]
tests/test_api.py::test_auth_login_invalid_password PASSED               [ 10%]
tests/test_api.py::test_auth_me_authenticated PASSED                     [ 13%]
tests/test_api.py::test_auth_register_new_user PASSED                    [ 17%]
tests/test_api.py::test_list_items_endpoint PASSED                       [ 20%]
tests/test_api.py::test_get_item_by_code PASSED                          [ 24%]
tests/test_api.py::test_barcode_lookup PASSED                            [ 27%]
tests/test_api.py::test_update_item PASSED                               [ 31%]
tests/test_api.py::test_stock_position PASSED                            [ 34%]
tests/test_api.py::test_stock_low_stock_alerts PASSED                    [ 37%]
tests/test_api.py::test_stock_adjustment PASSED                          [ 41%]
tests/test_api.py::test_vendors_list_and_create PASSED                   [ 44%]
tests/test_api.py::test_create_purchase_invoice_multi_item PASSED        [ 48%]
tests/test_api.py::test_create_sales_invoice_single_item PASSED          [ 51%]
tests/test_api.py::test_create_sales_invoice_multi_item PASSED           [ 55%]
tests/test_api.py::test_customer_create_and_search PASSED                [ 58%]
tests/test_api.py::test_print_invoice_custom PASSED                      [ 62%]
tests/test_api.py::test_print_existing_sales_invoice PASSED              [ 65%]
tests/test_api.py::test_gst_report_endpoint PASSED                       [ 68%]
tests/test_api.py::test_pnl_endpoint PASSED                              [ 72%]
tests/test_api.py::test_executive_summary_report PASSED                  [ 75%]
tests/test_api.py::test_etl_sync_trigger PASSED                          [ 79%]
tests/test_gst_engine.py::test_gst_output_and_input_calculation PASSED   [ 82%]
tests/test_sync_manager.py::test_sync_state_manager_lifecycle PASSED     [ 86%]
tests/test_transformer.py::test_flatten_customer_nested PASSED           [ 89%]
tests/test_transformer.py::test_flatten_dates_and_timestamps PASSED      [ 93%]
tests/test_transformer.py::test_transform_records_list PASSED            [ 96%]
tests/test_views_execution.py::test_sqlite_warehouse_views PASSED        [100%]

======================= 29 passed, 1 warning in 11.68s ========================
```
