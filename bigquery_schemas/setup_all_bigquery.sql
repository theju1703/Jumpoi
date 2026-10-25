-- ====================================================================
-- JOMPOI ONLINE GROCERY - ALL-IN-ONE BIGQUERY SETUP SCRIPT
-- Paste this entire script into Google Cloud BigQuery Query Editor
-- (https://console.cloud.google.com/bigquery) and click RUN.
-- ====================================================================

-- 1. CLEAN RE-CREATION OF DATASET (CASCADE removes old non-partitioned tables)
DROP SCHEMA IF EXISTS `jompoi_reporting` CASCADE;

CREATE SCHEMA `jompoi_reporting`
OPTIONS (location = 'US');

-- 2. CREATE FRESH PARTITIONED MASTER & TRANSACTION TABLES
CREATE TABLE `jompoi_reporting.customers` (
  _id STRING,
  name STRING,
  city STRING,
  phone STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE `jompoi_reporting.items` (
  _id STRING,
  item_code STRING,
  name STRING,
  brand STRING,
  category STRING,
  price NUMERIC,
  gst_percent NUMERIC,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE `jompoi_reporting.sales` (
  _id STRING,
  invoice_no STRING,
  invoice_date DATE,
  customer_name STRING,
  customer_city STRING,
  item_code STRING,
  item_name STRING,
  quantity NUMERIC,
  rate NUMERIC,
  net_amount NUMERIC,
  gst_percent NUMERIC,
  gst_amount NUMERIC,
  total_amount NUMERIC,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY invoice_date
CLUSTER BY customer_city, item_code;

CREATE TABLE `jompoi_reporting.purchases` (
  _id STRING,
  invoice_no STRING,
  invoice_date DATE,
  vendor STRING,
  item_code STRING,
  item_name STRING,
  quantity NUMERIC,
  rate NUMERIC,
  net_amount NUMERIC,
  gst_percent NUMERIC,
  gst_amount NUMERIC,
  total_amount NUMERIC,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY invoice_date
CLUSTER BY vendor, item_code;

CREATE TABLE `jompoi_reporting.stock_ledger` (
  _id STRING,
  item_code STRING,
  item_name STRING,
  transaction_type STRING,
  quantity NUMERIC,
  voucher_no STRING,
  date DATE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY date
CLUSTER BY item_code;

CREATE TABLE `jompoi_reporting.orders` (
  _id STRING,
  order_id STRING,
  customer_name STRING,
  customer_city STRING,
  order_date DATE,
  amount NUMERIC,
  status STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY order_date
CLUSTER BY customer_city;

-- 3. INSERT REPLICATED OPERATIONAL DATA
INSERT INTO `jompoi_reporting.customers` (_id, name, city, phone, created_at, updated_at)
VALUES
  ('CUST001', 'ABC Stores', 'Chennai', '9876543210', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('CUST002', 'Sri Murugan Supermarket', 'Madurai', '9876543211', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('CUST003', 'Kovai Fresh Mart', 'Coimbatore', '9876543212', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

INSERT INTO `jompoi_reporting.items` (_id, item_code, name, brand, category, price, gst_percent, created_at, updated_at)
VALUES
  ('ITM001', 'ITM001', 'Basmati Rice 5kg', 'India Gate', 'Grains & Rice', 450.0, 5.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ITM002', 'ITM002', 'Sunflower Oil 1L', 'Fortune', 'Edible Oils', 135.0, 5.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ITM003', 'ITM003', 'Toor Dal 1kg', 'Tata Sampann', 'Pulses', 160.0, 0.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ITM004', 'ITM004', 'Milk 500ml', 'Aavin', 'Dairy', 25.0, 0.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

INSERT INTO `jompoi_reporting.sales` (
  _id, invoice_no, invoice_date, customer_name, customer_city,
  item_code, item_name, quantity, rate, net_amount, gst_percent, gst_amount, total_amount,
  created_at, updated_at
)
VALUES
  ('INV001', 'INV-2026-001', DATE '2026-08-24', 'ABC Stores', 'Chennai', 'ITM001', 'Basmati Rice 5kg', 10, 450.0, 4500.0, 5.0, 225.0, 4725.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('INV002', 'INV-2026-002', DATE '2026-08-24', 'Sri Murugan Supermarket', 'Madurai', 'ITM002', 'Sunflower Oil 1L', 25, 135.0, 3375.0, 5.0, 168.75, 3543.75, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('INV003', 'INV-2026-003', DATE '2026-08-25', 'Kovai Fresh Mart', 'Coimbatore', 'ITM003', 'Toor Dal 1kg', 30, 160.0, 4800.0, 0.0, 0.0, 4800.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

INSERT INTO `jompoi_reporting.purchases` (
  _id, invoice_no, invoice_date, vendor,
  item_code, item_name, quantity, rate, net_amount, gst_percent, gst_amount, total_amount,
  created_at, updated_at
)
VALUES
  ('PINV001', 'PUR-2026-001', DATE '2026-08-20', 'KR Agro Supplies', 'ITM001', 'Basmati Rice 5kg', 50, 380.0, 19000.0, 5.0, 950.0, 19950.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('PINV002', 'PUR-2026-002', DATE '2026-08-21', 'Adani Wilmar Dist', 'ITM002', 'Sunflower Oil 1L', 100, 110.0, 11000.0, 5.0, 550.0, 11550.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

INSERT INTO `jompoi_reporting.stock_ledger` (
  _id, item_code, item_name, transaction_type, quantity, voucher_no, date, created_at, updated_at
)
VALUES
  ('STK001', 'ITM001', 'Basmati Rice 5kg', 'IN', 50, 'PUR-2026-001', DATE '2026-08-20', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('STK002', 'ITM002', 'Sunflower Oil 1L', 'IN', 100, 'PUR-2026-002', DATE '2026-08-21', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('STK003', 'ITM001', 'Basmati Rice 5kg', 'OUT', 10, 'INV-2026-001', DATE '2026-08-24', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('STK004', 'ITM002', 'Sunflower Oil 1L', 'OUT', 25, 'INV-2026-002', DATE '2026-08-24', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('STK005', 'ITM003', 'Toor Dal 1kg', 'OUT', 30, 'INV-2026-003', DATE '2026-08-25', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

INSERT INTO `jompoi_reporting.orders` (
  _id, order_id, customer_name, customer_city, order_date, amount, status, created_at, updated_at
)
VALUES
  ('ORD001', 'ORD001', 'ABC Stores', 'Chennai', DATE '2026-08-24', 12500.0, 'DELIVERED', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ORD002', 'ORD002', 'Sri Murugan Supermarket', 'Madurai', DATE '2026-08-24', 3543.75, 'DELIVERED', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ORD003', 'ORD003', 'Kovai Fresh Mart', 'Coimbatore', DATE '2026-08-25', 4800.0, 'PROCESSING', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

-- 4. CREATE REPORTING VIEWS FOR LOOKER STUDIO (Step 4 of Blueprint)
CREATE OR REPLACE VIEW `jompoi_reporting.vw_daily_sales` AS
SELECT
  invoice_date AS sales_date,
  item_code,
  item_name,
  customer_city,
  SUM(quantity) AS quantity_sold,
  SUM(net_amount) AS sales_value,
  SUM(gst_amount) AS gst_collected,
  SUM(total_amount) AS gross_sales_amount
FROM `jompoi_reporting.sales`
GROUP BY sales_date, item_code, item_name, customer_city;

CREATE OR REPLACE VIEW `jompoi_reporting.vw_daily_purchase` AS
SELECT
  invoice_date AS purchase_date,
  vendor,
  item_code,
  item_name,
  SUM(quantity) AS quantity_purchased,
  SUM(net_amount) AS purchase_value,
  SUM(gst_amount) AS input_gst_paid,
  SUM(total_amount) AS total_purchase_amount
FROM `jompoi_reporting.purchases`
GROUP BY purchase_date, vendor, item_code, item_name;

CREATE OR REPLACE VIEW `jompoi_reporting.vw_stock_position` AS
SELECT
  item_code,
  item_name,
  SUM(CASE WHEN transaction_type = 'IN' THEN quantity ELSE -quantity END) AS current_stock_qty
FROM `jompoi_reporting.stock_ledger`
GROUP BY item_code, item_name;

CREATE OR REPLACE VIEW `jompoi_reporting.vw_item_profitability` AS
WITH sales_summary AS (
  SELECT
    item_code,
    item_name,
    SUM(quantity) AS total_sold_qty,
    SUM(net_amount) AS total_revenue
  FROM `jompoi_reporting.sales`
  GROUP BY item_code, item_name
),
purchase_summary AS (
  SELECT
    item_code,
    AVG(rate) AS avg_purchase_rate
  FROM `jompoi_reporting.purchases`
  GROUP BY item_code
)
SELECT
  s.item_code,
  s.item_name,
  s.total_sold_qty,
  s.total_revenue,
  COALESCE(p.avg_purchase_rate, 0) AS avg_cost_per_unit,
  (s.total_sold_qty * COALESCE(p.avg_purchase_rate, 0)) AS total_cogs,
  s.total_revenue - (s.total_sold_qty * COALESCE(p.avg_purchase_rate, 0)) AS gross_profit
FROM sales_summary s
LEFT JOIN purchase_summary p ON s.item_code = p.item_code;

CREATE OR REPLACE VIEW `jompoi_reporting.vw_gst_summary` AS
WITH output_gst AS (
  SELECT
    invoice_date AS gst_date,
    SUM(gst_amount) AS output_tax
  FROM `jompoi_reporting.sales`
  GROUP BY invoice_date
),
input_gst AS (
  SELECT
    invoice_date AS gst_date,
    SUM(gst_amount) AS input_tax_credit
  FROM `jompoi_reporting.purchases`
  GROUP BY invoice_date
)
SELECT
  COALESCE(o.gst_date, i.gst_date) AS report_date,
  COALESCE(o.output_tax, 0) AS output_gst_sales,
  COALESCE(i.input_tax_credit, 0) AS input_gst_purchase,
  (COALESCE(o.output_tax, 0) - COALESCE(i.input_tax_credit, 0)) AS net_gst_payable
FROM output_gst o
FULL OUTER JOIN input_gst i ON o.gst_date = i.gst_date;

CREATE OR REPLACE VIEW `jompoi_reporting.vw_inventory_movement` AS
SELECT
  date AS movement_date,
  item_code,
  item_name,
  transaction_type,
  voucher_no,
  quantity
FROM `jompoi_reporting.stock_ledger`;

CREATE OR REPLACE VIEW `jompoi_reporting.vw_executive_kpis` AS
WITH sales_agg AS (
  SELECT
    COALESCE(SUM(net_amount), 0) AS total_revenue,
    COALESCE(SUM(gst_amount), 0) AS total_output_gst,
    COUNT(DISTINCT invoice_no) AS total_sales_orders
  FROM `jompoi_reporting.sales`
),
purchases_agg AS (
  SELECT
    COALESCE(SUM(net_amount), 0) AS total_purchase_spend,
    COALESCE(SUM(gst_amount), 0) AS total_input_gst,
    COUNT(DISTINCT invoice_no) AS total_purchase_bills
  FROM `jompoi_reporting.purchases`
),
inventory_agg AS (
  SELECT
    COALESCE(SUM(
      (CASE WHEN sl.transaction_type = 'IN' THEN sl.quantity ELSE -sl.quantity END) * COALESCE(it.price, 0)
    ), 0) AS total_inventory_value
  FROM `jompoi_reporting.stock_ledger` sl
  LEFT JOIN `jompoi_reporting.items` it ON sl.item_code = it.item_code
)
SELECT
  s.total_revenue,
  p.total_purchase_spend,
  (s.total_revenue - p.total_purchase_spend) AS estimated_gross_profit,
  ROUND(
    CASE 
      WHEN s.total_revenue > 0 THEN ((s.total_revenue - p.total_purchase_spend) / s.total_revenue) * 100 
      ELSE 0 
    END, 2
  ) AS gross_profit_margin_pct,
  i.total_inventory_value,
  s.total_output_gst,
  p.total_input_gst,
  (s.total_output_gst - p.total_input_gst) AS net_gst_payable,
  s.total_sales_orders,
  p.total_purchase_bills
FROM sales_agg s
CROSS JOIN purchases_agg p
CROSS JOIN inventory_agg i;
