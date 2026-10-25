import datetime
from src.etl.transformer import flatten_document, transform_records

def test_flatten_customer_nested():
    raw = {
        "_id": "ORD001",
        "customer": {
            "name": "ABC Stores",
            "city": "Chennai"
        },
        "date": "2026-08-24",
        "amount": 12500.0
    }
    flat = flatten_document(raw)
    assert flat["_id"] == "ORD001"
    assert flat["customer_name"] == "ABC Stores"
    assert flat["customer_city"] == "Chennai"
    assert "customer" not in flat
    assert flat["date"] == "2026-08-24"
    assert flat["amount"] == 12500.0

def test_flatten_dates_and_timestamps():
    now = datetime.datetime(2026, 8, 24, 15, 30, 0)
    raw = {
        "_id": 12345,
        "invoice_date": datetime.date(2026, 8, 24),
        "created_at": now
    }
    flat = flatten_document(raw)
    assert flat["_id"] == "12345"
    assert flat["invoice_date"] == "2026-08-24"
    assert "2026-08-24T15:30:00" in flat["created_at"]

def test_transform_records_list():
    raw_list = [
        {"_id": "1", "item_code": "ITM001", "price": 450.0},
        {"_id": "2", "item_code": "ITM002", "price": 135.0}
    ]
    transformed = transform_records(raw_list)
    assert len(transformed) == 2
    assert transformed[0]["item_code"] == "ITM001"
    assert transformed[1]["item_code"] == "ITM002"
