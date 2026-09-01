







"""Business Validation, safe corrections, audit trail, and classification."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
NUMBER_WORDS = {
    "صفر": 0, "واحد": 1, "واحدة": 1, "اثنان": 2, "اثنين": 2,
    "ثلاثة": 3, "اربعة": 4, "أربعة": 4, "خمسة": 5, "ستة": 6,
    "سبعة": 7, "ثمانية": 8, "تسعة": 9, "عشرة": 10, "عشرون": 20,
    "ثلاثون": 30, "أربعون": 40, "خمسون": 50, "مئة": 100, "مائة": 100,
    "خمسة وعشرون": 25,
}
STATUS_MAP = {
    "pending": "قيد الانتظار", "قيد الانتظار": "قيد الانتظار", "new": "قيد الانتظار",
    "confirmed": "مؤكد", "مؤكد": "مؤكد", "paid": "مؤكد", "مدفوع": "مؤكد", "مؤكد ": "مؤكد",
    "shipping": "قيد الشحن", "قيد الشحن": "قيد الشحن", "delivered": "تم التسليم", "تم التسليم": "تم التسليم",
    "returned": "مرتجع", "مرتجع": "مرتجع", "cancelled": "ملغي", "ملغي": "ملغي", "ملغى": "ملغي",
}
PAYMENT_METHOD_MAP = {
    "cash": "نقدًا عند التسليم", "cash on delivery": "نقدًا عند التسليم", "نقد": "نقدًا عند التسليم",
    "نقدًا عند التسليم": "نقدًا عند التسليم", "card": "بطاقة", "بطاقة": "بطاقة",
    "wallet": "محفظة إلكترونية", "محفظة": "محفظة إلكترونية", "محفظة إلكترونية": "محفظة إلكترونية",
}
PAYMENT_STATUS_MAP = {
    "pending": "بانتظار الدفع", "بانتظار الدفع": "بانتظار الدفع", "paid": "تم الدفع", "مدفوع": "تم الدفع",
    "تم الدفع": "تم الدفع", "rejected": "مرفوض", "مرفوض": "مرفوض",
}
VOLATILE = {"_id", "processed_at", "ingested_at"}
RAW_SCHEMA_REQUIRED = ("order_id", "order_date", "customer_id", "items_json")
FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "order_id": ("order_id", "orderid", "order id", "id"),
    "order_date": ("order_date", "orderdate", "order date", "date"),
    "status": ("status", "order_status", "order status"),
    "customer_id": ("customer_id", "customerid", "customer id"),
    "customer_name": ("customer_name", "customername", "customer name", "name"),
    "customer_phone": ("customer_phone", "customerphone", "customer phone", "phone"),
    "customer_email": ("customer_email", "customeremail", "customer email", "email"),
    "city": ("city", "customer_city"),
    "district": ("district", "customer_district", "area"),
    "delivery_type": ("delivery_type", "deliverytype", "shipping_type"),
    "delivery_cost": ("delivery_cost", "deliverycost", "shipping_cost", "shippingcost"),
    "payment_method": ("payment_method", "paymentmethod", "payment method"),
    "payment_status": ("payment_status", "paymentstatus", "payment status"),
    "payment_amount": ("payment_amount", "paymentamount", "payment amount", "amount"),
    "currency": ("currency", "payment_currency"),
    "total_amount": ("total_amount", "totalamount", "total amount", "order_total"),
    "items_json": ("items_json", "items", "items_data", "items_raw", "order_items"),
}


def _normalise_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).lower())


def canonicalize_raw_fields(raw: dict[str, Any]) -> dict[str, Any]:
    result = dict(raw)
    by_normalized_key = {_normalise_key(key): value for key, value in raw.items()}
    for canonical, aliases in FIELD_ALIASES.items():
        current = result.get(canonical)
        if current not in (None, ""):
            continue
        for alias in aliases:
            normalized = _normalise_key(alias)
            if normalized in by_normalized_key:
                result[canonical] = by_normalized_key[normalized]
                break
    return result


def validate_raw_schema(raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate the raw envelope before business normalization.

    CSV values are intentionally strings in Raw, so type conversion belongs to
    Business Validation. This stage checks required source fields and the raw
    items envelope; the final MongoDB validator checks canonical BSON types.
    """
    raw = canonicalize_raw_fields(raw)
    errors: list[dict[str, Any]] = []
    for field in RAW_SCHEMA_REQUIRED:
        if field not in raw or raw.get(field) in (None, ""):
            errors.append({"code": "SCHEMA_REQUIRED_FIELD", "field": field, "detail": "Required raw field is missing"})
    if "items_json" in raw and raw.get("items_json") not in (None, ""):
        value = raw.get("items_json")
        if not isinstance(value, (str, list, dict)):
            errors.append({"code": "SCHEMA_BSON_TYPE", "field": "items_json", "detail": "Raw items must be a string or JSON-compatible value"})
    return errors


def validate_structure_before_cleaning(raw: dict[str, Any], is_duplicate: bool = False) -> list[dict[str, Any]]:
    """Run only structural checks before any normalization or correction."""
    errors = validate_raw_schema(raw)
    if is_duplicate:
        errors.append({"code": "DUPLICATE_ORDER_ID", "field": "order_id", "detail": "Order ID appears more than once"})
    return errors


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _digits(value: Any) -> str:
    return _text(value).translate(ARABIC_DIGITS)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _correction(items: list[dict[str, Any]], field: str, original: Any, corrected: Any, rule: str) -> None:
    if original != corrected:
        items.append({"field": field, "original_value": original, "corrected_value": corrected, "rule_code": rule})


def _error(errors: list[dict[str, Any]], code: str, field: str, detail: str) -> None:
    errors.append({"code": code, "field": field, "detail": detail})


def _number(value: Any) -> tuple[float | None, str | None]:
    original = value
    text = _digits(value).replace("٬", "").replace(",", "").replace("٫", ".")
    if not text or text.lower() in {"unknown", "n/a", "null", "none", "-"}:
        return None, "UNKNOWN_PRICE"
    if text in NUMBER_WORDS:
        return float(NUMBER_WORDS[text]), "KNOWN_ARABIC_NUMBER_WORDS"
    cleaned = re.sub(r"[^0-9.\-]", "", text)
    try:
        number = float(Decimal(cleaned))
    except (InvalidOperation, ValueError):
        return None, "UNKNOWN_PRICE"
    if number < 0:
        return None, "AMBIGUOUS_NEGATIVE_VALUE"
    return number, None if str(original).strip() in {str(number), f"{number:.2f}"} else "NUMERIC_VALUE_NORMALISED"


def _date(value: Any) -> tuple[str | None, str | None]:
    original = value
    text = re.sub(r"\s*([/-])\s*", r"\1", _digits(value))
    for fmt in (
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
    ):
        try:
            parsed = datetime.strptime(text, fmt)
            result = parsed.strftime("%Y-%m-%d")
            return result, None if str(original).strip() == result else "DATE_ISO8601"
        except ValueError:
            continue
    return None, "INVALID_IMPOSSIBLE_DATE"


def _email(value: Any) -> tuple[str | None, str | None]:
    original = _text(value).lower()
    result = re.sub(r"\s+", "", original).replace("@@", "@").replace("..", ".")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", result):
        return None, "INVALID_EMAIL"
    if result != original:
        rule = "EMAIL_REPEATED_SYMBOLS" if "@@" in original or ".." in original else "EMAIL_NORMALISED"
        return result, rule
    return result, None


def _phone(value: Any) -> tuple[str | None, str | None]:
    original = _text(value)
    result = re.sub(r"[^0-9]", "", _digits(original))
    if result.startswith("00"):
        result = result[2:]
    if result.startswith("7") and len(result) == 9:
        result = "967" + result
    if not re.fullmatch(r"967(70|71|73|77)\d{7}", result):
        return None, "INVALID_PHONE"
    return result, None if result == original else "YEMEN_PHONE_NORMALISED"


def _enum(value: Any, mapping: dict[str, str], field: str, errors: list[dict[str, Any]], corrections: list[dict[str, Any]]) -> str | None:
    original = _text(value)
    result = mapping.get(original.lower(), mapping.get(original))
    if result is None:
        _error(errors, f"INVALID_{field.upper()}", field, "Value is outside the standard dictionary")
        return None
    _correction(corrections, field, value, result, "STATUS_PAYMENT_SYNONYM_NORMALISED")
    return result


def _items(value: Any, errors: list[dict[str, Any]], corrections: list[dict[str, Any]]) -> list[dict[str, Any]] | None:
    if isinstance(value, list):
        parsed = value
    else:
        text = _text(value)
        if not text:
            _error(errors, "EMPTY_ITEMS", "items_json", "No items supplied")
            return None
        try:
            parsed = json.loads(text)
        except (TypeError, json.JSONDecodeError):
            _error(errors, "CORRUPTED_ITEMS_JSON", "items_json", "Items JSON cannot be parsed")
            return None
    if not isinstance(parsed, list) or not parsed:
        _error(errors, "EMPTY_ITEMS", "items_json", "No items supplied")
        return None
    result: list[dict[str, Any]] = []
    for index, item in enumerate(parsed):
        if not isinstance(item, dict):
            _error(errors, "CORRUPTED_ITEMS_JSON", "items_json", f"Item {index} is not an object")
            continue
        qty, qty_rule = _number(item.get("qty", item.get("quantity")))
        price, price_rule = _number(item.get("unit_price", item.get("price")))
        total, total_rule = _number(item.get("total", item.get("line_total")))
        if qty is None or price is None:
            _error(errors, price_rule or "UNKNOWN_PRICE", f"items[{index}]", "Quantity or price cannot be inferred")
            continue
        if total is None:
            total = qty * price
            total_rule = "ITEM_TOTAL_RECALCULATED"
        if qty_rule:
            _correction(corrections, f"items[{index}].qty", item.get("qty", item.get("quantity")), int(qty), qty_rule)
        if price_rule:
            _correction(corrections, f"items[{index}].unit_price", item.get("unit_price", item.get("price")), price, price_rule)
        if total_rule:
            _correction(corrections, f"items[{index}].total", item.get("total", item.get("line_total")), total, total_rule)
        result.append({"sku": _text(item.get("sku")), "name": _text(item.get("name")), "qty": int(qty), "unit_price": price, "total": total})
    if not result and not errors:
        _error(errors, "EMPTY_ITEMS", "items_json", "No valid items remain")
    return result or None


def clean_raw_document(raw: dict[str, Any], is_duplicate: bool = False) -> dict[str, Any]:
    source = {key: value for key, value in raw.items() if key != "_id"}
    corrections: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    order_id = _text(source.get("order_id"))
    customer_id = _text(source.get("customer_id"))
    if not order_id:
        _error(errors, "MISSING_ORDER_ID", "order_id", "Order ID is missing")
    if not customer_id:
        _error(errors, "MISSING_CUSTOMER_ID", "customer_id", "Customer ID is missing")
    order_date, date_rule = _date(source.get("order_date"))
    if date_rule == "INVALID_IMPOSSIBLE_DATE":
        _error(errors, date_rule, "order_date", "Date is missing, invalid, or impossible")
    elif date_rule:
        _correction(corrections, "order_date", source.get("order_date"), order_date, date_rule)
    status = _enum(source.get("status"), STATUS_MAP, "status", errors, corrections)
    method = _enum(source.get("payment_method"), PAYMENT_METHOD_MAP, "payment_method", errors, corrections)
    payment_status = _enum(source.get("payment_status"), PAYMENT_STATUS_MAP, "payment_status", errors, corrections)
    phone, phone_rule = _phone(source.get("customer_phone"))
    if phone_rule == "INVALID_PHONE":
        _error(errors, phone_rule, "customer_phone", "Phone is not a valid Yemen number")
    elif phone_rule:
        _correction(corrections, "customer.phone", source.get("customer_phone"), phone, phone_rule)
    email, email_rule = _email(source.get("customer_email"))
    if email_rule == "INVALID_EMAIL":
        _error(errors, email_rule, "customer.email", "Email is invalid")
    elif email_rule:
        _correction(corrections, "customer.email", source.get("customer_email"), email, email_rule)
    currency_original = _text(source.get("currency"))
    currency = "YER" if currency_original.upper() in {"YER", "ر.ي", "ريال يمني", "ريال"} else None
    if currency is None:
        _error(errors, "INVALID_CURRENCY", "payment.currency", "Only YER is supported")
    elif currency_original != "YER":
        _correction(corrections, "payment.currency", currency_original, "YER", "CURRENCY_TO_YER")
    delivery_cost, delivery_rule = _number(source.get("delivery_cost", 0))
    if delivery_rule in {"UNKNOWN_PRICE", "AMBIGUOUS_NEGATIVE_VALUE"}:
        _error(errors, delivery_rule, "delivery_cost", "Delivery cost is not safely numeric")
    elif delivery_rule:
        _correction(corrections, "delivery.cost", source.get("delivery_cost"), delivery_cost, delivery_rule)
    parsed_items = _items(source.get("items_json"), errors, corrections)
    payment_amount, payment_rule = _number(source.get("payment_amount"))
    if payment_rule in {"UNKNOWN_PRICE", "AMBIGUOUS_NEGATIVE_VALUE"}:
        _error(errors, payment_rule, "payment.amount", "Payment amount is not safely numeric")
    elif payment_rule:
        _correction(corrections, "payment.amount", source.get("payment_amount"), payment_amount, payment_rule)
    original_total, total_rule = _number(source.get("total_amount"))
    if total_rule in {"UNKNOWN_PRICE", "AMBIGUOUS_NEGATIVE_VALUE"}:
        _error(errors, total_rule, "total_amount", "Total is not safely numeric")
    if parsed_items is not None and not errors:
        calculated_total = round(sum(float(item["total"]) for item in parsed_items) + float(delivery_cost or 0), 2)
        if original_total is None or round(original_total, 2) != calculated_total:
            _correction(corrections, "total_amount", source.get("total_amount"), calculated_total, "TOTAL_RECALCULATED")
        original_total = calculated_total
    # Duplicate detection is deliberately after Schema and Business checks.
    if is_duplicate:
        _error(errors, "DUPLICATE_ORDER_ID", "order_id", "Order ID appears more than once")
    if errors:
        codes = list(dict.fromkeys(item["code"] for item in errors))
        if len(codes) > 1:
            codes = ["MULTIPLE_CONFLICTING_ERRORS", *codes]
        return {
            "run_id": raw.get("run_id"), "source_file": raw.get("source_file"), "source_row_number": raw.get("source_row_number"),
            "engine_used": raw.get("engine_used", "pyspark"), "processed_at": _now(), "order_id": order_id or None,
            "quality_status": "quarantined", "validation_stages": ["schema_validation", "business_validation", "duplicate_detection"], "schema_valid": True, "original_document": deepcopy(source), "raw_payload": raw.get("raw_payload"),
            "error_codes": list(dict.fromkeys(codes)), "error_code": codes[0], "error_details": errors, "corrections": corrections,
        }
    document = {
        "run_id": raw.get("run_id"), "source_file": raw.get("source_file"), "source_row_number": raw.get("source_row_number"),
        "engine_used": raw.get("engine_used", "pyspark"), "processed_at": _now(), "order_id": order_id,
        "order_date": order_date, "status": status, "customer": {"customer_id": customer_id, "name": _text(source.get("customer_name")), "phone": phone, "email": email, "address": {"city": _text(source.get("city")), "district": _text(source.get("district"))}},
        "items": parsed_items, "payment": {"method": method, "status": payment_status, "amount": payment_amount, "currency": "YER"},
        "delivery": {"type": _text(source.get("delivery_type")), "cost": delivery_cost or 0.0}, "total_amount": original_total,
        "quality_status": "corrected" if corrections else "validated", "validation_stages": ["schema_validation", "business_validation", "duplicate_detection"], "schema_valid": True, "corrections": corrections,
    }
    return document


def classify_raw_document(raw: dict[str, Any], is_duplicate: bool = False) -> dict[str, Any]:
    """Classify structure first; only structurally safe rows reach cleaning."""
    canonical_raw = canonicalize_raw_fields(raw)
    structural_errors = validate_structure_before_cleaning(canonical_raw, is_duplicate=is_duplicate)
    if structural_errors:
        codes = list(dict.fromkeys(item["code"] for item in structural_errors))
        quarantine = {
            "run_id": raw.get("run_id"), "source_file": raw.get("source_file"), "source_row_number": raw.get("source_row_number"),
            "order_id": _text(raw.get("order_id")) or None, "quality_status": "quarantined",
            "initial_classification": "invalid", "schema_valid": not any(item["code"].startswith("SCHEMA_") for item in structural_errors),
            "validation_stages": ["schema_validation", "duplicate_detection"],             "original_document": deepcopy({key: value for key, value in raw.items() if key != "_id"}),
            "raw_payload": raw.get("raw_payload"), "error_codes": codes, "error_code": codes[0],
            "error_details": structural_errors, "schema_validation_errors": [item for item in structural_errors if item["code"].startswith("SCHEMA_")],
            "corrections": [], "cleaning_applied": False, "processed_at": _now(),
        }
        return {"initial_classification": "invalid", "structure_passed": False, "cleaning_applied": False, "initial_quarantine": quarantine, "final_document": quarantine}

    # Cleaning and Business Validation are deliberately the last stage.
    final_document = clean_raw_document(canonical_raw, is_duplicate=is_duplicate)
    final_document["schema_valid"] = True
    final_document["structure_passed"] = True
    final_document["cleaning_applied"] = True
    final_document["validation_stages"] = ["schema_validation", "duplicate_detection", "business_validation", "cleaning_last"]
    return {
        "initial_classification": "valid", "structure_passed": True, "cleaning_applied": True,
        "initial_quarantine": None, "final_document": final_document,
    }


def clean_and_validate(raw: dict[str, Any]) -> dict[str, Any]:
    """Small teaching-contract adapter used by the unit tests."""
    result = dict(raw)
    errors: list[dict[str, str]] = []
    corrections: list[dict[str, Any]] = []
    if not _text(result.get("order_id")):
        errors.append({"code": "MISSING_ORDER_ID", "field": "order_id"})
    if not _text(result.get("customer_id")):
        errors.append({"code": "MISSING_CUSTOMER_ID", "field": "customer_id"})
    date, date_rule = _date(result.get("order_date"))
    if date_rule == "INVALID_IMPOSSIBLE_DATE":
        errors.append({"code": date_rule, "field": "order_date"})
    elif date_rule:
        corrections.append({"field": "order_date", "original_value": result.get("order_date"), "corrected_value": date, "rule_code": date_rule})
    items = result.get("items")
    if isinstance(items, str):
        try:
            items = json.loads(items)
        except json.JSONDecodeError:
            items = None
    if not isinstance(items, list) or not items:
        errors.append({"code": "EMPTY_ITEMS", "field": "items"})
    email, email_rule = _email(result.get("customer_email"))
    if email_rule == "INVALID_EMAIL":
        errors.append({"code": email_rule, "field": "customer_email"})
    elif email_rule:
        corrections.append({"field": "customer_email", "original_value": result.get("customer_email"), "corrected_value": email, "rule_code": email_rule})
    if errors:
        return {**result, "quality_status": "quarantined", "error_code": errors[0]["code"], "error_details": errors, "corrections": corrections}
    return {**result, "order_date": date, "items": items, "customer_email": email, "quality_status": "corrected" if corrections else "validated", "corrections": corrections}


clean_order_document = clean_raw_document
classify_order_before_cleaning = classify_raw_document

__all__ = ["FIELD_ALIASES", "canonicalize_raw_fields", "clean_and_validate", "validate_raw_schema", "validate_raw_business_rules", "validate_structure_before_cleaning", "clean_raw_document", "clean_order_document", "classify_raw_document", "classify_order_before_cleaning", "classify_raw_without_cleaning"]


# ---------------------------------------------------------------------------
# Raw-only classification: no normalization, correction, or cleaning.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Raw-only classification: separate hard errors from safe deferred corrections.
# ---------------------------------------------------------------------------
RAW_STANDARD_STATUSES = set(STATUS_MAP.values())
RAW_STANDARD_PAYMENT_METHODS = set(PAYMENT_METHOD_MAP.values())
RAW_STANDARD_PAYMENT_STATUSES = set(PAYMENT_STATUS_MAP.values())
RAW_REQUIRED_BUSINESS_FIELDS = (
    "order_id", "order_date", "customer_id", "customer_phone",
    "customer_email", "city", "district", "delivery_type", "delivery_cost",
    "payment_method", "payment_status", "payment_amount", "currency",
    "total_amount", "items_json",
)


def _raw_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _raw_number(value: Any) -> tuple[float | None, str | None]:
    """Return a numeric value and a soft rule, or a hard error code."""
    if value is None or isinstance(value, bool):
        return None, "UNKNOWN_PRICE"
    if isinstance(value, (int, float, Decimal)):
        number = float(value)
        return (number, None) if number >= 0 else (None, "AMBIGUOUS_NEGATIVE_VALUE")

    original = str(value)
    stripped = original.strip()
    if not stripped:
        return None, "UNKNOWN_PRICE"
    if stripped in {"unknown", "UNKNOWN", "n/a", "N/A", "null", "None", "-"}:
        return None, "UNKNOWN_PRICE"
    if stripped.startswith("-") or re.search(r"(^|[^0-9])-", stripped):
        return None, "AMBIGUOUS_NEGATIVE_VALUE"

    normalized = stripped.replace("٬", "").replace(",", "").replace("٫", ".")
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?", normalized):
        return None, "UNKNOWN_PRICE"
    number = float(normalized)
    return number, None if normalized == original else "NUMERIC_VALUE_NORMALISED"


def _raw_date(value: Any) -> tuple[bool, str | None]:
    """Accept parseable timestamps as soft corrections; reject impossible dates."""
    original = _raw_text(value)
    if not original:
        return False, "INVALID_IMPOSSIBLE_DATE"

    normalized = re.sub(r"\s*([/-])\s*", r"\1", original)
    formats = (
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
    )
    for fmt in formats:
        try:
            parsed = datetime.strptime(normalized, fmt)
            canonical = parsed.strftime("%Y-%m-%d")
            return True, None if original == canonical else "DATE_ISO8601"
        except ValueError:
            continue
    return False, "INVALID_IMPOSSIBLE_DATE"


def _raw_phone(value: Any) -> tuple[bool, str | None]:
    original = _raw_text(value)
    digits = _digits(original)
    digits = re.sub(r"[^0-9]", "", digits)
    if digits.startswith("00"):
        digits = digits[2:]
    if re.fullmatch(r"967(70|71|73|77)[0-9]{7}", digits):
        return True, None if digits == original else "YEMEN_PHONE_NORMALISED"
    if re.fullmatch(r"(70|71|73|77)[0-9]{7}", digits):
        return True, "YEMEN_PHONE_NORMALISED"
    return False, "INVALID_PHONE"


def _raw_email(value: Any) -> tuple[bool, str | None]:
    original = _raw_text(value)
    if not original:
        return False, "INVALID_EMAIL"
    normalized = re.sub(r"\s+", "", original).replace("@@", "@").replace("..", ".")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
        return False, "INVALID_EMAIL"
    if normalized != original:
        return True, "EMAIL_REPEATED_SYMBOLS"
    return True, None


def _raw_enum(value: Any, mapping: dict[str, str]) -> tuple[bool, str | None]:
    original = _raw_text(value)
    if not original:
        return False, None
    canonical = mapping.get(original.lower(), mapping.get(original))
    if canonical is None:
        return False, "INVALID_ENUM"
    return True, None if canonical == original else "ENUM_SYNONYM_NORMALISED"


def _raw_items(value: Any) -> tuple[list[dict[str, Any]] | None, list[dict[str, Any]], list[dict[str, Any]]]:
    """Parse items and return (items, hard_errors, deferred_corrections)."""
    hard: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (TypeError, json.JSONDecodeError):
            _error(hard, "CORRUPTED_ITEMS_JSON", "items_json", "Items JSON cannot be parsed")
            return None, hard, deferred
    else:
        parsed = value

    if not isinstance(parsed, list) or not parsed:
        _error(hard, "EMPTY_ITEMS", "items_json", "No items supplied")
        return None, hard, deferred

    for index, item in enumerate(parsed):
        if not isinstance(item, dict):
            _error(hard, "CORRUPTED_ITEMS_JSON", "items_json", f"Item {index} is not an object")
            continue
        for key, fallback, field in (
            ("qty", "quantity", f"items[{index}].qty"),
            ("unit_price", "price", f"items[{index}].unit_price"),
            ("total", "line_total", f"items[{index}].total"),
        ):
            number, rule = _raw_number(item.get(key, item.get(fallback)))
            if rule in {"UNKNOWN_PRICE", "AMBIGUOUS_NEGATIVE_VALUE"}:
                _error(hard, rule, field, "Value is missing, negative, or cannot be inferred safely")
            elif rule:
                deferred.append({
                    "field": field,
                    "original_value": item.get(key, item.get(fallback)),
                    "rule_code": rule,
                    "reason": "Safe numeric normalization deferred to Cleaning Last",
                })
    return parsed, hard, deferred


def inspect_raw_business_quality(raw: dict[str, Any], is_duplicate: bool = False) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return hard errors and safe corrections to defer; never changes raw values."""
    source = canonicalize_raw_fields(raw)
    hard = validate_raw_schema(source)
    # Use the project-required business codes for missing stable identifiers.
    for error in hard:
        if error.get("code") == "SCHEMA_REQUIRED_FIELD" and error.get("field") == "order_id":
            error["code"] = "MISSING_ORDER_ID"
            error["detail"] = "Order ID is missing and cannot be inferred safely"
        elif error.get("code") == "SCHEMA_REQUIRED_FIELD" and error.get("field") == "customer_id":
            error["code"] = "MISSING_CUSTOMER_ID"
            error["detail"] = "Customer ID is missing"
    deferred: list[dict[str, Any]] = []

    for field in RAW_REQUIRED_BUSINESS_FIELDS:
        if source.get(field) in (None, "") and not any(e.get("field") == field for e in hard):
            _error(hard, f"MISSING_{field.upper()}", field, "Required value is missing in raw data")

    if source.get("order_date") not in (None, ""):
        date_ok, date_rule = _raw_date(source.get("order_date"))
        if not date_ok:
            _error(hard, "INVALID_IMPOSSIBLE_DATE", "order_date", "Date is impossible or cannot be parsed safely")
        elif date_rule:
            deferred.append({
                "field": "order_date",
                "original_value": source.get("order_date"),
                "rule_code": date_rule,
                "reason": "Parseable date format; canonicalization deferred to Cleaning Last",
            })

    for field, mapping in (
        ("status", STATUS_MAP),
        ("payment_method", PAYMENT_METHOD_MAP),
        ("payment_status", PAYMENT_STATUS_MAP),
    ):
        if source.get(field) not in (None, ""):
            enum_ok, enum_rule = _raw_enum(source.get(field), mapping)
            if not enum_ok:
                _error(hard, f"INVALID_{field.upper()}", field, "Value is outside the standard dictionary")
            elif enum_rule:
                deferred.append({
                    "field": field,
                    "original_value": source.get(field),
                    "rule_code": enum_rule,
                    "reason": "Known synonym or surrounding whitespace; normalization deferred",
                })

    phone = source.get("customer_phone")
    if phone not in (None, ""):
        phone_ok, phone_rule = _raw_phone(phone)
        if not phone_ok:
            _error(hard, "INVALID_PHONE", "customer_phone", "Phone is not a safe Yemen number")
        elif phone_rule:
            deferred.append({
                "field": "customer_phone",
                "original_value": phone,
                "rule_code": phone_rule,
                "reason": "Recognized Yemen local number; country code normalization deferred",
            })

    email = source.get("customer_email")
    if email not in (None, ""):
        email_ok, email_rule = _raw_email(email)
        if not email_ok:
            _error(hard, "INVALID_EMAIL", "customer_email", "Email cannot be corrected safely")
        elif email_rule:
            deferred.append({
                "field": "customer_email",
                "original_value": email,
                "rule_code": email_rule,
                "reason": "Safe repeated-symbol/whitespace correction deferred",
            })

    currency = source.get("currency")
    if currency not in (None, ""):
        currency_text = _raw_text(currency)
        if currency_text.upper() not in {"YER", "ر.ي", "ريال يمني", "ريال"}:
            _error(hard, "INVALID_CURRENCY", "currency", "Currency is not a recognized YER synonym")
        elif currency_text != "YER":
            deferred.append({
                "field": "currency",
                "original_value": currency,
                "rule_code": "CURRENCY_TO_YER",
                "reason": "Recognized YER synonym; standardization deferred",
            })

    for field in ("delivery_cost", "payment_amount", "total_amount"):
        if source.get(field) not in (None, ""):
            number, rule = _raw_number(source.get(field))
            if rule in {"UNKNOWN_PRICE", "AMBIGUOUS_NEGATIVE_VALUE"}:
                _error(hard, rule, field, "Number is missing, negative, or cannot be inferred safely")
            elif rule:
                deferred.append({
                    "field": field,
                    "original_value": source.get(field),
                    "rule_code": rule,
                    "reason": "Safe numeric normalization deferred",
                })

    items, item_errors, item_deferred = _raw_items(source.get("items_json"),)
    hard.extend(item_errors)
    deferred.extend(item_deferred)

    # A total mismatch is a deferred warning when all item numbers are usable;
    # Cleaning Last can recalculate it from the preserved raw items.
    if items is not None and not any(e.get("field", "").startswith("items[") for e in hard):
        total, total_rule = _raw_number(source.get("total_amount"))
        delivery, delivery_rule = _raw_number(source.get("delivery_cost", 0))
        if total is not None and delivery is not None:
            line_total = 0.0
            for item in items:
                qty, _ = _raw_number(item.get("qty", item.get("quantity")))
                price, _ = _raw_number(item.get("unit_price", item.get("price")))
                item_total, _ = _raw_number(item.get("total", item.get("line_total")))
                if item_total is not None:
                    line_total += item_total
                elif qty is not None and price is not None:
                    line_total += qty * price
            expected = round(line_total + delivery, 2)
            if round(total, 2) != expected:
                deferred.append({
                    "field": "total_amount",
                    "original_value": source.get("total_amount"),
                    "rule_code": "TOTAL_RECALCULATED",
                    "corrected_value": expected,
                    "reason": "Components are parseable; recalculation deferred to Cleaning Last",
                })

    if is_duplicate:
        _error(hard, "DUPLICATE_ORDER_ID", "order_id", "Order ID appears more than once in raw data")
    return hard, deferred


def validate_raw_business_rules(raw: dict[str, Any], is_duplicate: bool = False) -> list[dict[str, Any]]:
    """Return only hard errors; safe anomalies are deferred to Cleaning Last."""
    hard, _ = inspect_raw_business_quality(raw, is_duplicate=is_duplicate)
    return hard


def build_raw_validated_document(raw: dict[str, Any], deferred_corrections: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    source = canonicalize_raw_fields(raw)
    return {
        "run_id": raw.get("run_id"),
        "source_file": raw.get("source_file"),
        "source_row_number": raw.get("source_row_number"),
        "engine_used": raw.get("engine_used", "pyspark"),
        "processed_at": _now(),
        "order_id": source.get("order_id"),
        "order_date": source.get("order_date"),
        "status": source.get("status"),
        "customer": {
            "customer_id": source.get("customer_id"),
            "name": source.get("customer_name"),
            "phone": source.get("customer_phone"),
            "email": source.get("customer_email"),
            "address": {"city": source.get("city"), "district": source.get("district")},
        },
        "items": source.get("items_json"),
        "payment": {
            "method": source.get("payment_method"),
            "status": source.get("payment_status"),
            "amount": source.get("payment_amount"),
            "currency": source.get("currency"),
        },
        "delivery": {"type": source.get("delivery_type"), "cost": source.get("delivery_cost")},
        "total_amount": source.get("total_amount"),
        "quality_status": "raw_validated",
        "raw_validation_only": True,
        "cleaning_applied": False,
        "validation_stages": ["raw_schema_validation", "raw_business_validation", "raw_duplicate_detection"],
        "schema_valid": True,
        "corrections": [],
        "deferred_corrections": deferred_corrections or [],
        "original_document": deepcopy({k: v for k, v in raw.items() if k not in {"_id", "_is_duplicate", "raw_mongo_id"}}),
        "raw_payload": raw.get("raw_payload"),
    }


def classify_raw_without_cleaning(raw: dict[str, Any], is_duplicate: bool = False) -> dict[str, Any]:
    """Raw-first classification: hard errors quarantine; safe anomalies validate with deferred corrections."""
    source = canonicalize_raw_fields(raw)
    hard_errors, deferred = inspect_raw_business_quality(source, is_duplicate=is_duplicate)
    if hard_errors:
        codes = list(dict.fromkeys(error["code"] for error in hard_errors))
        if len(codes) > 1:
            codes = ["MULTIPLE_CONFLICTING_ERRORS", *codes]
        quarantine = {
            "run_id": raw.get("run_id"),
            "source_file": raw.get("source_file"),
            "source_row_number": raw.get("source_row_number"),
            "order_id": source.get("order_id") or None,
            "quality_status": "raw_quarantined",
            "raw_validation_only": True,
            "cleaning_applied": False,
            "initial_classification": "invalid",
            "schema_valid": not any(e["code"].startswith("SCHEMA_") for e in hard_errors),
            "validation_stages": ["raw_schema_validation", "raw_business_validation", "raw_duplicate_detection"],
            "original_document": deepcopy({k: v for k, v in raw.items() if k not in {"_id", "raw_mongo_id"}}),
            "raw_payload": raw.get("raw_payload"),
            "error_codes": codes,
            "error_code": codes[0],
            "error_details": hard_errors,
            "corrections": [],
            "deferred_corrections": deferred,
        }
        return {
            "raw_valid": False,
            "raw_invalid": True,
            "cleaning_applied": False,
            "validated_document": None,
            "quarantine_document": quarantine,
        }

    return {
        "raw_valid": True,
        "raw_invalid": False,
        "cleaning_applied": False,
        "validated_document": build_raw_validated_document(source, deferred),
        "quarantine_document": None,
    }


__all__ = [
    "FIELD_ALIASES", "canonicalize_raw_fields", "clean_and_validate",
    "validate_raw_schema", "validate_raw_business_rules", "validate_structure_before_cleaning",
    "clean_raw_document", "clean_order_document", "classify_raw_document",
    "classify_order_before_cleaning", "classify_raw_without_cleaning",
    "inspect_raw_business_quality", "build_raw_validated_document",
]
