# Looker Studio Visual Configuration Guide for Jompoi

This guide provides the exact setup steps and styling configurations to build the reporting dashboards in **Looker Studio** ([datastudio.google.com/navigation/reporting](https://datastudio.google.com/navigation/reporting)) corresponding to the architecture blueprint.

---

## 1. Quick Data Source Connection

1. Navigate to [datastudio.google.com/navigation/reporting](https://datastudio.google.com/navigation/reporting).
2. Click **Create** &rarr; **Data Source**.
3. Select the **BigQuery** connector.
4. Choose **My Projects** &rarr; Your GCP Project &rarr; Dataset `jompoi_reporting`.
5. Select either:
   - Specific reporting views: `vw_executive_kpis`, `vw_daily_sales`, `vw_stock_position`, etc.
   - Or click **Custom Query** and paste queries from [`looker_studio/custom_queries.sql`](./custom_queries.sql).
6. Click **Connect** (top right).

---

## 2. Page-by-Page Visual Construction

### Page 1: Executive Dashboard (Summary Page)
- **Top Scorecard Row**:
  - `Gross Revenue`: Metric = `SUM(total_revenue)`, Format = Currency (₹ INR)
  - `Total Procurement`: Metric = `SUM(total_purchase_spend)`, Format = Currency (₹ INR)
  - `Gross Profit Margin`: Metric = `AVG(gross_profit_margin_pct)`, Format = Percent (%)
  - `Stock Valuation`: Metric = `SUM(total_inventory_value)`, Format = Currency (₹ INR)
  - `Net GST Payable`: Metric = `SUM(net_gst_payable)`, Format = Currency (₹ INR)
- **Chart 1 (Bar / Column)**: Daily Revenue vs Procurement
  - Dimension: `invoice_date`
  - Metrics: `SUM(net_amount)` (Sales), `SUM(net_amount)` (Purchases)
- **Chart 2 (Donut Chart)**: Sales Share by Grocery Category
  - Dimension: `category`
  - Metric: `SUM(total_amount)`

---

### Page 2: Sales In-Depth
- **Chart 1 (Horizontal Bar)**: Top Items by Revenue & Quantity
  - Dimension: `item_name`
  - Metric: `SUM(quantity)` and `SUM(net_amount)`
- **Chart 2 (Donut Chart)**: Revenue Breakdown by Customer City
  - Dimension: `customer_city`
  - Metric: `SUM(net_amount)`
- **Table with Heatmap**: Invoices Detailed Audit Table
  - Dimensions: `invoice_no`, `invoice_date`, `customer_name`, `item_name`
  - Metrics: `quantity`, `rate`, `net_amount`, `gst_amount`, `total_amount`

---

### Page 3: Purchases & Vendor Performance
- **Chart 1 (Donut Chart)**: Procurement Share by Supplier
  - Dimension: `vendor`
  - Metric: `SUM(total_amount)`
- **Chart 2 (Column Chart)**: Cost Rate vs Retail Selling Price
  - Dimension: `item_name`
  - Metrics: `AVG(rate)` (Purchase Cost), `AVG(retail_selling_price)` (Retail Price)
- **Table**: Supplier Bills Summary
  - Dimensions: `vendor`, `item_name`
  - Metrics: `COUNT(invoice_no)`, `SUM(quantity)`, `SUM(net_amount)`, `SUM(input_gst)`

---

### Page 4: Inventory & Live Stock
- **Chart 1 (Bar Chart)**: Closing Stock Levels per Product
  - Dimension: `item_name`
  - Metric: `SUM(current_stock_qty)`
- **Table with Conditional Formatting**: Low Stock Alert Table
  - Dimensions: `item_code`, `item_name`, `brand`, `category`
  - Metrics: `current_stock_qty`, `current_valuation`
  - Conditional Color: If `current_stock_qty <= 10`, highlight in RED/AMBER.

---

### Page 5: GST & Input Tax Credit (ITC)
- **Scorecards**:
  - `Output Tax (Sales Liability)`: `SUM(output_gst_sales)`
  - `Input Tax Credit (ITC)`: `SUM(input_gst_purchase)`
  - `Net Cash Outflow`: `SUM(net_gst_payable)`
- **Table**: Monthly Tax Settlement Table
  - Dimension: `report_date`
  - Metrics: `output_gst_sales`, `input_gst_purchase`, `net_gst_payable`
  - Calculated Field: `settlement_status`

---

## 3. Recommended Theme & Styling
- **Theme**: Simple Dark or Edge (matches dark dashboard aesthetics).
- **Primary Color**: `#3B82F6` (Electric Blue).
- **Secondary Color**: `#10B981` (Emerald Green for positive margins/ITC).
- **Warning Color**: `#F59E0B` (Amber for low inventory).
