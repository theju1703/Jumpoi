from pathlib import Path
from src.local_warehouse.sqlite_bq_emulator import LocalWarehouseEmulator

BASE_DIR = Path(__file__).resolve().parent.parent
DUMMY_DIR = BASE_DIR / "dummy_data"

def test_sqlite_warehouse_views():
    warehouse = LocalWarehouseEmulator()
    warehouse.load_from_json_files(DUMMY_DIR)

    # 1. Test Daily Sales View
    daily_sales = warehouse.query_view("vw_daily_sales")
    assert len(daily_sales) > 0
    first_sale = daily_sales[0]
    assert "sales_date" in first_sale
    assert "quantity_sold" in first_sale
    assert "sales_value" in first_sale

    # 2. Test Daily Purchase View
    daily_purchase = warehouse.query_view("vw_daily_purchase")
    assert len(daily_purchase) > 0

    # 3. Test Stock Position View
    stock_pos = warehouse.query_view("vw_stock_position")
    assert len(stock_pos) > 0
    # ITM001 had IN: 50, OUT: 10 -> current_stock_qty should be 40
    itm001 = next(item for item in stock_pos if item["item_code"] == "ITM001")
    assert itm001["current_stock_qty"] == 40.0

    # 4. Test Item Profitability View
    profitability = warehouse.query_view("vw_item_profitability")
    assert len(profitability) > 0

    # 5. Test GST Summary View
    gst_summary = warehouse.query_view("vw_gst_summary")
    assert len(gst_summary) > 0

    # 6. Test Executive KPIs View
    kpis = warehouse.query_view("vw_executive_kpis")
    assert len(kpis) == 1
    assert kpis[0]["total_revenue"] > 0
    assert kpis[0]["total_purchase_spend"] > 0

    warehouse.close()
