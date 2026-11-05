# Supermarket ERP - Mobile Application & API Integration Specification

**Platform:** Android (Modern Native)  
**UI Toolkit:** Jetpack Compose (Material 3)  
**Architecture:** MVVM + Clean Architecture (Data, Domain, Presentation)  
**Networking:** Retrofit2 + OkHttp3 + Kotlinx Serialization  
**Local Storage / Cache:** Room Database + Jetpack DataStore Preferences  
**Target Backend:** Jompoi ERP REST API (`http://10.0.2.2:8080` for Android Emulator / local network IP for physical device)

---

## 1. Backend Modules to Mobile Screens Mapping

| Mobile Screen | Target Feature | Backend REST API Endpoints | HTTP Method | Request Payload / Params | Response Data | Allowed Roles |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Login Screen** (`LoginScreen`) | JWT User Authentication | `/api/auth/login` | `POST` | `{"username", "password"}` | `access_token`, `role`, `full_name`, `username` | All |
| **2. Executive ERP Dashboard** (`DashboardScreen`) | Key business metrics, stock alerts & tax liability summary | `/api/reports/summary`<br>`/api/stock/low-stock` | `GET`<br>`GET` | Header: `Authorization: Bearer <token>` | `active_items_count`, `gross_sales_revenue`, `gst_summary`, `low_stock_list` | Admin, Manager |
| **3. POS Billing & Checkout** (`PosBillingScreen`) | Barcode scan, item cart, real-time GST tax calculation, checkout | `/api/items/barcode/{code}`<br>`/api/sales/invoice` | `GET`<br>`POST` | `invoice_no`, `customer_name`, `items: [{item_code, quantity, rate}]` | Created invoice, `stock_ledger_entries`, `(Price+Tax)*Qty` line totals | Cashier, Admin |
| **4. Commercial Invoice Preview & Print** (`PrintInvoiceScreen`) | View official tax invoice, per-item GST breakdown, print dialog | `/api/invoice/{invoice_no}/print`<br>`/api/invoice/print` | `GET`<br>`POST` | `invoice_no` OR raw `PrintInvoiceRequest` | Formatted printable HTML with `(Price+Tax)*Qty` & tax breakdown | Cashier, Manager, Admin |
| **5. Product Catalog & Search** (`CatalogScreen`) | View master products, filter by category, search by name/SKU | `/api/items`<br>`/api/items/{item_code}` | `GET`<br>`PUT` | Query: `category`, `search`. Body for update: `price`, `gst_percent` | Array of `Item` (name, brand, price, gst_percent, min_stock) | All |
| **6. Inventory & Stock Ledger** (`InventoryScreen`) | Real-time stock on hand, valuation, stock movements | `/api/stock`<br>`/api/stock/adjust` | `GET`<br>`POST` | Body: `item_code`, `adjustment_type`, `quantity`, `reason` | Aggregated stock position (`IN - OUT`), valuation, audit logs | Inventory Staff, Manager, Admin |
| **7. Vendor Procurement & Bills** (`PurchasesScreen`) | Multi-item vendor purchase bill entry with per-item GST rates | `/api/purchases`<br>`/api/purchases/invoice`<br>`/api/vendors` | `GET`<br>`POST`<br>`GET` | Multi-item payload with varying GST % (0%, 5%, 12%, 18%) | Recorded purchase doc, Stock IN ledger entries, ITC credit | Manager, Admin |
| **8. Customer CRM** (`CustomersScreen`) | Lookup customer by phone, register new customer | `/api/customers`<br>`/api/customers/search` | `GET`<br>`POST` | `name`, `city`, `phone`, `address` | Customer profile & transaction history | Cashier, Admin |
| **9. GST Tax Credit Reconciliation** (`GstReportScreen`) | Reconcile GSTR-1 sales tax vs GSTR-2B vendor input tax credit | `/api/gst/report` | `GET` | Header: `Authorization` | `output_gst_sales`, `input_gst_purchases`, `itc_utilized`, `net_gst_payable_in_cash`, `excess_itc_carried_forward` | Manager, Admin |
| **10. ERP Profit & Loss** (`PnlScreen`) | Financial P&L: Revenue, COGS, Gross Profit, Operating Expenses | `/api/pnl` | `GET` | Query: `operating_expenses` | `revenue`, `cost_of_goods_sold`, `gross_profit`, `net_profit` | Manager, Admin |

---

## 2. Android Clean Architecture & Package Structure

```
com.example.jompoierp/
├── data/
│   ├── api/
│   │   ├── ErpApiService.kt          # Retrofit interface definitions
│   │   └── ApiClient.kt              # OkHttp client with AuthInterceptor & BaseUrl
│   ├── model/
│   │   ├── AuthModels.kt             # UserLogin, AuthResponse, UserProfile
│   │   ├── ItemModels.kt             # Item, ItemCreate, ItemUpdate
│   │   ├── SalesModels.kt            # SalesInvoice, SalesItem, PrintInvoiceModels
│   │   ├── PurchaseModels.kt         # PurchaseInvoice, PurchaseItem, Vendor
│   │   ├── InventoryModels.kt        # StockPosition, StockAdjustment, LowStockAlert
│   │   └── ReportModels.kt           # GstReport, PnlStatement, ExecutiveSummary
│   ├── repository/
│   │   ├── AuthRepository.kt
│   │   ├── ProductRepository.kt
│   │   ├── SalesRepository.kt
│   │   ├── PurchaseRepository.kt
│   │   ├── InventoryRepository.kt
│   │   └── ReportsRepository.kt
│   └── local/
│       └── SessionManager.kt         # DataStore / Token & Role persistence
│
├── ui/
│   ├── theme/
│   │   ├── Color.kt                  # Professional Dark/Light Enterprise Palette
│   │   ├── Theme.kt                  # Material3 JompoiERPTheme
│   │   └── Type.kt
│   ├── components/
│   │   ├── CommonWidgets.kt          # StatCards, Badges, SearchBars, LoadingIndicators
│   │   └── NavigationBar.kt          # Bottom navigation bar with role guards
│   ├── auth/
│   │   ├── LoginScreen.kt            # Modern branded login view
│   │   └── AuthViewModel.kt
│   ├── dashboard/
│   │   ├── DashboardScreen.kt        # Executive KPIs, quick actions
│   │   └── DashboardViewModel.kt
│   ├── pos/
│   │   ├── PosBillingScreen.kt       # Barcode scanner input, cart, calculation
│   │   ├── InvoicePrintScreen.kt     # Exact commercial print table preview
│   │   └── PosViewModel.kt
│   ├── inventory/
│   │   ├── InventoryScreen.kt        # Stock levels, valuation, adjustment dialog
│   │   └── InventoryViewModel.kt
│   ├── purchases/
│   │   ├── PurchasesScreen.kt        # Multi-item vendor bill entry
│   │   └── PurchasesViewModel.kt
│   ├── reports/
│   │   ├── GstReportScreen.kt        # GSTR-1 vs GSTR-2B visual reconciliation
│   │   ├── PnlScreen.kt              # Financial Profit & Loss statement
│   │   └── ReportsViewModel.kt
│   └── MainActivity.kt               # Single-activity Compose container
```

---

## 3. Retail Math & Formula Compliance

* **POS Cart Line Total Formula:**
  $$\text{Unit Tax} = \text{Rate} \times \left(\frac{\text{GST \%}}{100}\right)$$
  $$\text{Line Item Total} = (\text{Rate} + \text{Unit Tax}) \times \text{Quantity}$$
* **Commercial Invoice Columns:**
  `[#]`, `[Item Name]`, `[Item Description (Optional)]`, `[Quantity]`, `[Price]`, `[Tax (GST % & Rs)]`, `[Total = (Price + Tax) * Qty]`
* **GST ITC Reconciliation:**
  $$\text{Eligible ITC Utilized} = \min(\text{Output Tax}, \text{Input Credit})$$
  $$\text{Net Cash Payable} = \max(0, \text{Output Tax} - \text{Input Credit})$$
  $$\text{Excess ITC Carried Forward} = \max(0, \text{Input Credit} - \text{Output Tax})$$
