-- ====================================================================
-- POPULATE BIGQUERY TABLES WITH REPLICATED JOMPOI DUMMY DATA
-- Run this in BigQuery Query Editor after running create_tables.sql
-- ====================================================================

-- 1. Insert Customers
INSERT INTO `jompoi_reporting.customers` (_id, customer_id, name, city, phone, created_at, updated_at)
VALUES
  ('CUST001', 'C001', 'ABC Stores', 'Chennai', '9876543210', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('CUST002', 'C002', 'Sri Murugan Supermarket', 'Madurai', '9876543211', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('CUST003', 'C003', 'Kovai Fresh Mart', 'Coimbatore', '9876543212', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

-- 2. Insert Items Master Data
INSERT INTO `jompoi_reporting.items` (_id, item_code, name, brand, category, price, gst_percent, created_at, updated_at)
VALUES
  ('ITM001', 'ITM001', 'Basmati Rice 5kg', 'India Gate', 'Grains & Rice', 450.0, 5.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ITM002', 'ITM002', 'Sunflower Oil 1L', 'Fortune', 'Edible Oils', 135.0, 5.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ITM003', 'ITM003', 'Toor Dal 1kg', 'Tata Sampann', 'Pulses', 160.0, 0.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ITM004', 'ITM004', 'Milk 500ml', 'Aavin', 'Dairy', 25.0, 0.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

-- 3. Insert Flattened Sales Invoices (replicated from MongoDB)
INSERT INTO `jompoi_reporting.sales` (
  _id, invoice_no, invoice_date, customer_name, customer_city,
  item_code, item_name, quantity, rate, net_amount, gst_percent, gst_amount, total_amount,
  created_at, updated_at
)
VALUES
  ('INV001', 'INV-2026-001', DATE '2026-08-24', 'ABC Stores', 'Chennai', 'ITM001', 'Basmati Rice 5kg', 10, 450.0, 4500.0, 5.0, 225.0, 4725.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('INV002', 'INV-2026-002', DATE '2026-08-24', 'Sri Murugan Supermarket', 'Madurai', 'ITM002', 'Sunflower Oil 1L', 25, 135.0, 3375.0, 5.0, 168.75, 3543.75, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('INV003', 'INV-2026-003', DATE '2026-08-25', 'Kovai Fresh Mart', 'Coimbatore', 'ITM003', 'Toor Dal 1kg', 30, 160.0, 4800.0, 0.0, 0.0, 4800.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

-- 4. Insert Purchases
INSERT INTO `jompoi_reporting.purchases` (
  _id, invoice_no, invoice_date, vendor,
  item_code, item_name, quantity, rate, net_amount, gst_percent, gst_amount, total_amount,
  created_at, updated_at
)
VALUES
  ('PINV001', 'PUR-2026-001', DATE '2026-08-20', 'KR Agro Supplies', 'ITM001', 'Basmati Rice 5kg', 50, 380.0, 19000.0, 5.0, 950.0, 19950.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('PINV002', 'PUR-2026-002', DATE '2026-08-21', 'Adani Wilmar Dist', 'ITM002', 'Sunflower Oil 1L', 100, 110.0, 11000.0, 5.0, 550.0, 11550.0, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

-- 5. Insert Stock Ledger
INSERT INTO `jompoi_reporting.stock_ledger` (
  _id, item_code, item_name, transaction_type, quantity, voucher_no, date, created_at, updated_at
)
VALUES
  ('STK001', 'ITM001', 'Basmati Rice 5kg', 'IN', 50, 'PUR-2026-001', DATE '2026-08-20', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('STK002', 'ITM001', 'Basmati Rice 5kg', 'OUT', 10, 'INV-2026-001', DATE '2026-08-24', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

-- 6. Insert Orders
INSERT INTO `jompoi_reporting.orders` (
  _id, order_id, customer_name, customer_city, order_date, amount, status, created_at, updated_at
)
VALUES
  ('ORD001', 'ORD001', 'ABC Stores', 'Chennai', DATE '2026-08-24', 12500.0, 'DELIVERED', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ORD002', 'ORD002', 'Sri Murugan Supermarket', 'Madurai', DATE '2026-08-24', 3543.75, 'DELIVERED', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()),
  ('ORD003', 'ORD003', 'Kovai Fresh Mart', 'Coimbatore', DATE '2026-08-25', 4800.0, 'PROCESSING', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());
