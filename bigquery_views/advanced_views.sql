-- ====================================================================
-- JOMPOI ADVANCED REPORTING VIEWS FOR LOOKER STUDIO / BI
-- Matches Executive Dashboard Structure from Client Architecture Blueprint:
--   - Executive Dashboard
--   - Sales Analytics
--   - Purchase & Supplier Analytics
--   - Inventory Movements & Valuation
--   - GST Summary
-- ====================================================================

-- 1. Executive Summary KPIs View
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

-- 2. Sales by Category & Brand View
CREATE OR REPLACE VIEW `jompoi_reporting.vw_sales_by_brand_category` AS
SELECT
  s.invoice_date,
  COALESCE(i.category, 'Uncategorized') AS category,
  COALESCE(i.brand, 'Generic') AS brand,
  s.item_code,
  s.item_name,
  s.customer_city,
  SUM(s.quantity) AS total_qty_sold,
  SUM(s.net_amount) AS total_net_sales,
  SUM(s.gst_amount) AS total_gst_collected,
  SUM(s.total_amount) AS total_gross_sales
FROM `jompoi_reporting.sales` s
LEFT JOIN `jompoi_reporting.items` i ON s.item_code = i.item_code
GROUP BY
  s.invoice_date,
  category,
  brand,
  s.item_code,
  s.item_name,
  s.customer_city;

-- 3. Sales by Customer View
CREATE OR REPLACE VIEW `jompoi_reporting.vw_sales_by_customer` AS
SELECT
  customer_name,
  customer_city,
  COUNT(DISTINCT invoice_no) AS invoice_count,
  SUM(quantity) AS total_items_bought,
  SUM(net_amount) AS total_spent_net,
  SUM(gst_amount) AS total_gst_paid,
  SUM(total_amount) AS total_spent_gross,
  MIN(invoice_date) AS first_order_date,
  MAX(invoice_date) AS latest_order_date
FROM `jompoi_reporting.sales`
GROUP BY
  customer_name,
  customer_city;

-- 4. Supplier Purchase Trends View
CREATE OR REPLACE VIEW `jompoi_reporting.vw_purchase_trends_by_supplier` AS
SELECT
  vendor,
  item_code,
  item_name,
  COUNT(DISTINCT invoice_no) AS bills_count,
  SUM(quantity) AS total_qty_purchased,
  AVG(rate) AS average_purchase_rate,
  MIN(rate) AS min_purchase_rate,
  MAX(rate) AS max_purchase_rate,
  SUM(net_amount) AS total_net_purchase,
  SUM(gst_amount) AS total_input_gst,
  SUM(total_amount) AS total_gross_purchase
FROM `jompoi_reporting.purchases`
GROUP BY
  vendor,
  item_code,
  item_name;

-- 5. Comprehensive Inventory Valuation & Stock Movement
CREATE OR REPLACE VIEW `jompoi_reporting.vw_inventory_valuation` AS
WITH stock_calc AS (
  SELECT
    item_code,
    item_name,
    SUM(CASE WHEN transaction_type = 'IN' THEN quantity ELSE 0 END) AS total_stock_in,
    SUM(CASE WHEN transaction_type = 'OUT' THEN quantity ELSE 0 END) AS total_stock_out,
    SUM(CASE WHEN transaction_type = 'IN' THEN quantity ELSE -quantity END) AS closing_stock_qty
  FROM `jompoi_reporting.stock_ledger`
  GROUP BY item_code, item_name
)
SELECT
  sc.item_code,
  sc.item_name,
  it.brand,
  it.category,
  it.price AS selling_price,
  sc.total_stock_in,
  sc.total_stock_out,
  sc.closing_stock_qty,
  (sc.closing_stock_qty * COALESCE(it.price, 0)) AS stock_valuation_at_selling_price,
  CASE
    WHEN sc.closing_stock_qty <= 10 THEN 'LOW STOCK'
    WHEN sc.closing_stock_qty > 50 THEN 'OVERSTOCKED'
    ELSE 'HEALTHY'
  END AS inventory_status
FROM stock_calc sc
LEFT JOIN `jompoi_reporting.items` it ON sc.item_code = it.item_code;
