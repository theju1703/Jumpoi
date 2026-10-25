-- ====================================================================
-- LOOKER STUDIO CUSTOM SQL QUERIES
-- Use these directly in Looker Studio:
-- Create -> Data Source -> BigQuery -> Custom Query
-- ====================================================================

-- 1. Executive Dashboard KPI Query
SELECT * FROM `jompoi_reporting.vw_executive_kpis`;

-- 2. Sales Analytics Query (with Brand, Category, and City dimensions)
SELECT
  s.invoice_no,
  s.invoice_date,
  s.customer_name,
  s.customer_city,
  s.item_code,
  s.item_name,
  COALESCE(i.brand, 'Generic') AS brand,
  COALESCE(i.category, 'General Grocery') AS category,
  s.quantity,
  s.rate,
  s.net_amount,
  s.gst_percent,
  s.gst_amount,
  s.total_amount
FROM `jompoi_reporting.sales` s
LEFT JOIN `jompoi_reporting.items` i ON s.item_code = i.item_code;

-- 3. Purchases & Supplier Performance Query
SELECT
  p.invoice_no,
  p.invoice_date,
  p.vendor,
  p.item_code,
  p.item_name,
  p.quantity,
  p.rate,
  p.net_amount,
  p.gst_amount AS input_gst,
  p.total_amount,
  COALESCE(i.price, 0) AS retail_selling_price,
  (COALESCE(i.price, 0) - p.rate) AS gross_unit_margin
FROM `jompoi_reporting.purchases` p
LEFT JOIN `jompoi_reporting.items` i ON p.item_code = i.item_code;

-- 4. Inventory Valuation & Stock Movement Query
SELECT
  sp.item_code,
  sp.item_name,
  COALESCE(i.brand, 'Generic') AS brand,
  COALESCE(i.category, 'General') AS category,
  COALESCE(i.price, 0) AS selling_price,
  sp.current_stock_qty,
  (sp.current_stock_qty * COALESCE(i.price, 0)) AS current_valuation,
  CASE
    WHEN sp.current_stock_qty <= 10 THEN 'LOW STOCK'
    ELSE 'SUFFICIENT'
  END AS inventory_health
FROM `jompoi_reporting.vw_stock_position` sp
LEFT JOIN `jompoi_reporting.items` i ON sp.item_code = i.item_code;

-- 5. GST Output vs Input Reconciliation Query (GSTR-3B Table)
SELECT
  report_date,
  output_gst_sales,
  input_gst_purchase,
  net_gst_payable,
  CASE
    WHEN net_gst_payable > 0 THEN 'Payable in Cash'
    ELSE 'Credit Carried Forward'
  END AS settlement_status
FROM `jompoi_reporting.vw_gst_summary`;
