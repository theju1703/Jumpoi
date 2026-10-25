-- ====================================================================
-- JOMPOI REPORTING VIEWS FOR LOOKER STUDIO (Step 4 of Client Guide)
-- Run these in BigQuery Query Editor after creating the tables
-- ====================================================================

-- 1. Daily Sales View (as per client example in screenshot)
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
FROM
  `jompoi_reporting.sales`
GROUP BY
  sales_date,
  item_code,
  item_name,
  customer_city;

-- 2. Daily Purchase View
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
FROM
  `jompoi_reporting.purchases`
GROUP BY
  purchase_date,
  vendor,
  item_code,
  item_name;

-- 3. Stock Position View (Closing stock from stock ledger)
CREATE OR REPLACE VIEW `jompoi_reporting.vw_stock_position` AS
SELECT
  item_code,
  item_name,
  SUM(CASE WHEN transaction_type = 'IN' THEN quantity ELSE -quantity END) AS current_stock_qty
FROM
  `jompoi_reporting.stock_ledger`
GROUP BY
  item_code,
  item_name;

-- 4. Item Profitability View
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
FROM
  sales_summary s
LEFT JOIN
  purchase_summary p ON s.item_code = p.item_code;

-- 5. GST Summary View (Output GST vs Input GST -> Net GST Payable)
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
FROM
  output_gst o
FULL OUTER JOIN
  input_gst i ON o.gst_date = i.gst_date;

-- 6. Inventory Movement View
CREATE OR REPLACE VIEW `jompoi_reporting.vw_inventory_movement` AS
SELECT
  date AS movement_date,
  item_code,
  item_name,
  transaction_type,
  voucher_no,
  quantity
FROM
  `jompoi_reporting.stock_ledger`;
