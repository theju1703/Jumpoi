import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List

class LocalWarehouseEmulator:
    """
    Simulates Google Cloud BigQuery locally using SQLite.
    Loads transformed MongoDB collections, builds reporting tables, and provisions
    the reporting SQL views for offline analytics and automated testing.
    """

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            _id TEXT PRIMARY KEY,
            customer_id TEXT,
            name TEXT,
            city TEXT,
            phone TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            _id TEXT PRIMARY KEY,
            item_code TEXT,
            name TEXT,
            brand TEXT,
            category TEXT,
            price REAL,
            gst_percent REAL,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            _id TEXT PRIMARY KEY,
            invoice_no TEXT,
            invoice_date TEXT,
            customer_name TEXT,
            customer_city TEXT,
            item_code TEXT,
            item_name TEXT,
            quantity REAL,
            rate REAL,
            net_amount REAL,
            gst_percent REAL,
            gst_amount REAL,
            total_amount REAL,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            _id TEXT PRIMARY KEY,
            invoice_no TEXT,
            invoice_date TEXT,
            vendor TEXT,
            item_code TEXT,
            item_name TEXT,
            quantity REAL,
            rate REAL,
            net_amount REAL,
            gst_percent REAL,
            gst_amount REAL,
            total_amount REAL,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_ledger (
            _id TEXT PRIMARY KEY,
            item_code TEXT,
            item_name TEXT,
            transaction_type TEXT,
            quantity REAL,
            voucher_no TEXT,
            date TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            _id TEXT PRIMARY KEY,
            order_id TEXT,
            customer_name TEXT,
            customer_city TEXT,
            date TEXT,
            order_date TEXT,
            amount REAL,
            status TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        """)

        self.conn.commit()
        self._init_views()

    def _init_views(self):
        cursor = self.conn.cursor()

        # 1. Daily Sales View
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_daily_sales AS
        SELECT
            invoice_date AS sales_date,
            item_code,
            item_name,
            customer_city,
            SUM(quantity) AS quantity_sold,
            SUM(net_amount) AS sales_value,
            SUM(gst_amount) AS gst_collected,
            SUM(total_amount) AS gross_sales_amount
        FROM sales
        GROUP BY sales_date, item_code, item_name, customer_city;
        """)

        # 2. Daily Purchase View
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_daily_purchase AS
        SELECT
            invoice_date AS purchase_date,
            vendor,
            item_code,
            item_name,
            SUM(quantity) AS quantity_purchased,
            SUM(net_amount) AS purchase_value,
            SUM(gst_amount) AS input_gst_paid,
            SUM(total_amount) AS total_purchase_amount
        FROM purchases
        GROUP BY purchase_date, vendor, item_code, item_name;
        """)

        # 3. Stock Position View
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_stock_position AS
        SELECT
            item_code,
            item_name,
            SUM(CASE WHEN transaction_type = 'IN' THEN quantity ELSE -quantity END) AS current_stock_qty
        FROM stock_ledger
        GROUP BY item_code, item_name;
        """)

        # 4. Item Profitability View
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_item_profitability AS
        WITH sales_summary AS (
            SELECT
                item_code,
                item_name,
                SUM(quantity) AS total_sold_qty,
                SUM(net_amount) AS total_revenue
            FROM sales
            GROUP BY item_code, item_name
        ),
        purchase_summary AS (
            SELECT
                item_code,
                AVG(rate) AS avg_purchase_rate
            FROM purchases
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
        """)

        # 5. GST Summary View
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_gst_summary AS
        WITH output_gst AS (
            SELECT invoice_date AS gst_date, SUM(gst_amount) AS output_tax
            FROM sales
            GROUP BY invoice_date
        ),
        input_gst AS (
            SELECT invoice_date AS gst_date, SUM(gst_amount) AS input_tax_credit
            FROM purchases
            GROUP BY invoice_date
        ),
        all_dates AS (
            SELECT gst_date FROM output_gst
            UNION
            SELECT gst_date FROM input_gst
        )
        SELECT
            d.gst_date AS report_date,
            COALESCE(o.output_tax, 0) AS output_gst_sales,
            COALESCE(i.input_tax_credit, 0) AS input_gst_purchase,
            (COALESCE(o.output_tax, 0) - COALESCE(i.input_tax_credit, 0)) AS net_gst_payable
        FROM all_dates d
        LEFT JOIN output_gst o ON d.gst_date = o.gst_date
        LEFT JOIN input_gst i ON d.gst_date = i.gst_date;
        """)

        # 6. Inventory Movement View
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_inventory_movement AS
        SELECT
            date AS movement_date,
            item_code,
            item_name,
            transaction_type,
            voucher_no,
            quantity
        FROM stock_ledger;
        """)

        # 7. Executive KPIs View
        cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_executive_kpis AS
        SELECT
            (SELECT COALESCE(SUM(net_amount), 0) FROM sales) AS total_revenue,
            (SELECT COALESCE(SUM(net_amount), 0) FROM purchases) AS total_purchase_spend,
            ((SELECT COALESCE(SUM(net_amount), 0) FROM sales) - (SELECT COALESCE(SUM(net_amount), 0) FROM purchases)) AS gross_profit,
            (SELECT COALESCE(SUM(gst_amount), 0) FROM sales) AS total_output_gst,
            (SELECT COALESCE(SUM(gst_amount), 0) FROM purchases) AS total_input_gst,
            ((SELECT COALESCE(SUM(gst_amount), 0) FROM sales) - (SELECT COALESCE(SUM(gst_amount), 0) FROM purchases)) AS net_gst_payable,
            (SELECT COUNT(DISTINCT invoice_no) FROM sales) AS total_sales_orders,
            (SELECT COUNT(DISTINCT invoice_no) FROM purchases) AS total_purchase_bills;
        """)

        self.conn.commit()

    def load_from_json_files(self, data_dir: Path):
        """Loads records from dummy_data folder directly into tables."""
        from src.etl.transformer import flatten_document

        file_table_map = {
            "customers.json": "customers",
            "items.json": "items",
            "orders.json": "orders",
            "sales_invoice.json": "sales",
            "purchase_invoice.json": "purchases",
            "stock_ledger.json": "stock_ledger"
        }

        cursor = self.conn.cursor()
        for file_name, table in file_table_map.items():
            fpath = data_dir / file_name
            if fpath.exists():
                with open(fpath, "r", encoding="utf-8") as f:
                    records = json.load(f)
                for raw in records:
                    doc = flatten_document(raw)
                    cols = list(doc.keys())
                    placeholders = ", ".join(["?"] * len(cols))
                    sql = f"INSERT OR REPLACE INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
                    cursor.execute(sql, list(doc.values()))

        self.conn.commit()

    def query_view(self, view_name: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {view_name}")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self):
        self.conn.close()
