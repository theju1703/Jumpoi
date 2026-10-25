import datetime
from dateutil import parser
from typing import Any, Dict, List

DATE_FIELDS = {"invoice_date", "date", "order_date"}
TIMESTAMP_FIELDS = {"created_at", "updated_at"}

def format_date_value(val: Any) -> str:
    """Formats a date or datetime value to YYYY-MM-DD."""
    if isinstance(val, (datetime.date, datetime.datetime)):
        return val.strftime("%Y-%m-%d")
    elif isinstance(val, str):
        try:
            parsed = parser.parse(val)
            return parsed.strftime("%Y-%m-%d")
        except Exception:
            return val
    return str(val)

def format_timestamp_value(val: Any) -> str:
    """Formats timestamp to ISO 8601 string for BigQuery TIMESTAMP."""
    if isinstance(val, datetime.datetime):
        return val.isoformat()
    elif isinstance(val, datetime.date):
        return datetime.datetime.combine(val, datetime.time.min).isoformat()
    elif isinstance(val, str):
        try:
            parsed = parser.parse(val)
            return parsed.isoformat()
        except Exception:
            return val
    return str(val)

def flatten_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms and flattens a MongoDB document to conform with BigQuery schema.
    Converts ObjectId, handles nested dicts (such as customer: {name, city}),
    and standardizes date and timestamp formats.
    """
    flat: Dict[str, Any] = {}

    # Standardize _id
    if "_id" in doc:
        flat["_id"] = str(doc["_id"])

    for key, value in doc.items():
        if key == "_id":
            continue

        # Handle nested customer objects explicitly as per blueprint
        if isinstance(value, dict):
            if key == "customer":
                flat["customer_name"] = value.get("name")
                flat["customer_city"] = value.get("city")
            else:
                for sub_k, sub_v in value.items():
                    sub_key = f"{key}_{sub_k}"
                    if isinstance(sub_v, dict):
                        flat[sub_key] = str(sub_v)
                    else:
                        flat[sub_key] = sub_v

        # Handle Date fields
        elif key in DATE_FIELDS:
            flat[key] = format_date_value(value)

        # Handle Timestamp fields
        elif key in TIMESTAMP_FIELDS:
            flat[key] = format_timestamp_value(value)

        elif isinstance(value, (datetime.datetime, datetime.date)):
            flat[key] = value.isoformat()

        else:
            flat[key] = value

    return flat

def transform_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transforms a list of MongoDB documents into flattened BigQuery rows."""
    return [flatten_document(r) for r in records]
