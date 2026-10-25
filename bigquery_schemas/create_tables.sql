-- ====================================================================
-- JOMPOI REPORTING BIGQUERY DDL (Step 2 of Blueprint)
-- Database / Dataset: jompoi_reporting
-- ====================================================================

-- 1. Create the Dataset (Replace with your GCP project ID)
-- CREATE SCHEMA IF NOT EXISTS `your-project-id.jompoi_reporting`
-- OPTIONS (location = 'US');

-- 2. Create Customers Table
CREATE TABLE IF NOT EXISTS `jompoi_reporting.customers` (
  _id STRING OPTIONS(description="MongoDB Document ID"),
  customer_id STRING OPTIONS(description="Business Customer Code"),
  name STRING OPTIONS(description="Customer Store or Personal Name"),
  city STRING OPTIONS(description="Customer City / Location"),
  phone STRING OPTIONS(description="Contact Phone Number"),
  created_at TIMESTAMP OPTIONS(description="Record creation timestamp"),
  updated_at TIMESTAMP OPTIONS(description="Record last updated timestamp")
);

-- 3. Create Items Master Table
CREATE TABLE IF NOT EXISTS `jompoi_reporting.items` (
  _id STRING OPTIONS(description="MongoDB Document ID"),
  item_code STRING OPTIONS(description="Unique Item SKU / Code"),
  name STRING OPTIONS(description="Item Description / Title"),
  brand STRING OPTIONS(description="Manufacturer / Brand"),
  category STRING OPTIONS(description="Grocery Category"),
  price NUMERIC OPTIONS(description="Retail Selling Price per Unit"),
  gst_percent NUMERIC OPTIONS(description="Applicable GST Tax Percentage"),
  created_at TIMESTAMP OPTIONS(description="Record creation timestamp"),
  updated_at TIMESTAMP OPTIONS(description="Record last updated timestamp")
);

-- 4. Create Sales Table (Flattened from sales_invoice & orders)
CREATE TABLE IF NOT EXISTS `jompoi_reporting.sales` (
  _id STRING OPTIONS(description="MongoDB Document ID"),
  invoice_no STRING OPTIONS(description="Unique Sales Invoice Number"),
  invoice_date DATE OPTIONS(description="Invoice Date"),
  customer_name STRING OPTIONS(description="Flattened Customer Name"),
  customer_city STRING OPTIONS(description="Flattened Customer City"),
  item_code STRING OPTIONS(description="Item SKU Code"),
  item_name STRING OPTIONS(description="Item Name"),
  quantity NUMERIC OPTIONS(description="Quantity Sold"),
  rate NUMERIC OPTIONS(description="Unit Selling Rate excluding tax"),
  net_amount NUMERIC OPTIONS(description="Net Sales Amount (Qty * Rate)"),
  gst_percent NUMERIC OPTIONS(description="GST Rate %"),
  gst_amount NUMERIC OPTIONS(description="Output GST Collected"),
  total_amount NUMERIC OPTIONS(description="Gross Invoice Total (Net + GST)"),
  created_at TIMESTAMP OPTIONS(description="Record creation timestamp"),
  updated_at TIMESTAMP OPTIONS(description="Record last updated timestamp")
)
PARTITION BY invoice_date
CLUSTER BY customer_city, item_code;

-- 5. Create Purchases Table (Procurement / Purchase Invoices)
CREATE TABLE IF NOT EXISTS `jompoi_reporting.purchases` (
  _id STRING OPTIONS(description="MongoDB Document ID"),
  invoice_no STRING OPTIONS(description="Vendor Invoice Number"),
  invoice_date DATE OPTIONS(description="Vendor Invoice Date"),
  vendor STRING OPTIONS(description="Supplier / Vendor Name"),
  item_code STRING OPTIONS(description="Item SKU Code"),
  item_name STRING OPTIONS(description="Item Name"),
  quantity NUMERIC OPTIONS(description="Quantity Received / Purchased"),
  rate NUMERIC OPTIONS(description="Unit Purchase Rate excluding tax"),
  net_amount NUMERIC OPTIONS(description="Net Purchase Amount (Qty * Rate)"),
  gst_percent NUMERIC OPTIONS(description="Input GST %"),
  gst_amount NUMERIC OPTIONS(description="Input GST Paid (ITC Eligible)"),
  total_amount NUMERIC OPTIONS(description="Total Purchase Amount (Net + GST)"),
  created_at TIMESTAMP OPTIONS(description="Record creation timestamp"),
  updated_at TIMESTAMP OPTIONS(description="Record last updated timestamp")
)
PARTITION BY invoice_date
CLUSTER BY vendor, item_code;

-- 6. Create Stock Ledger Table (Inventory Movements)
CREATE TABLE IF NOT EXISTS `jompoi_reporting.stock_ledger` (
  _id STRING OPTIONS(description="MongoDB Document ID"),
  item_code STRING OPTIONS(description="Item SKU Code"),
  item_name STRING OPTIONS(description="Item Name"),
  transaction_type STRING OPTIONS(description="IN (Purchase/Return) or OUT (Sales/Damage)"),
  quantity NUMERIC OPTIONS(description="Quantity Moved"),
  voucher_no STRING OPTIONS(description="Reference Sales/Purchase Invoice No"),
  date DATE OPTIONS(description="Movement Date"),
  created_at TIMESTAMP OPTIONS(description="Record creation timestamp"),
  updated_at TIMESTAMP OPTIONS(description="Record last updated timestamp")
)
PARTITION BY date
CLUSTER BY item_code;

-- 7. Create Orders Table (Flattened from MongoDB orders)
CREATE TABLE IF NOT EXISTS `jompoi_reporting.orders` (
  _id STRING OPTIONS(description="MongoDB Document ID"),
  order_id STRING OPTIONS(description="Order Identifier"),
  customer_name STRING OPTIONS(description="Flattened Customer Name"),
  customer_city STRING OPTIONS(description="Flattened Customer City"),
  order_date DATE OPTIONS(description="Order Placed Date"),
  amount NUMERIC OPTIONS(description="Total Order Value"),
  status STRING OPTIONS(description="Order Status: PENDING, DELIVERED, CANCELLED"),
  created_at TIMESTAMP OPTIONS(description="Record creation timestamp"),
  updated_at TIMESTAMP OPTIONS(description="Record last updated timestamp")
)
PARTITION BY order_date
CLUSTER BY customer_city;
