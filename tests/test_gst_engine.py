from src.gst_engine.gst_reconciliation import GSTReconciliationEngine

def test_gst_output_and_input_calculation():
    sales = [
        {"invoice_no": "INV-001", "invoice_date": "2026-08-24", "net_amount": 4500.0, "gst_percent": 5.0, "gst_amount": 225.0, "total_amount": 4725.0},
        {"invoice_no": "INV-002", "invoice_date": "2026-08-24", "net_amount": 3375.0, "gst_percent": 5.0, "gst_amount": 168.75, "total_amount": 3543.75}
    ]
    purchases = [
        {"invoice_no": "PUR-001", "invoice_date": "2026-08-20", "vendor": "Vendor A", "net_amount": 10000.0, "gst_percent": 5.0, "gst_amount": 500.0, "total_amount": 10500.0}
    ]

    engine = GSTReconciliationEngine(sales, purchases)
    report = engine.generate_gst_payment_report()

    # Output tax = 225.0 + 168.75 = 393.75
    assert report["output_gst_sales"] == 393.75
    # Input tax = 500.0
    assert report["input_gst_purchases"] == 500.0
    # ITC utilized = min(393.75, 500) = 393.75
    assert report["itc_utilized"] == 393.75
    # Net payable in cash = 0 (since input tax > output tax)
    assert report["net_gst_payable_in_cash"] == 0.0
    # Excess ITC carry forward = 500 - 393.75 = 106.25
    assert report["excess_itc_carried_forward"] == 106.25
