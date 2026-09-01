from __future__ import annotations

import csv
import json

from elt_pipeline import JsonStore, clean_after_raw_batch, load_csv_streaming
from file_router import discover_file
from quality_rules import classify_raw_document, classify_raw_without_cleaning, validate_raw_schema


def canonical_raw() -> dict[str, object]:
    return {
        "run_id": "run-test",
        "source_file": "orders.csv",
        "source_row_number": 2,
        "engine_used": "pyspark",
        "order_id": "ORD-1",
        "order_date": "2025-01-31",
        "status": "مؤكد",
        "customer_id": "C-1",
        "customer_name": "Test User",
        "customer_phone": "967771234567",
        "customer_email": "user@mail.com",
        "city": "صنعاء",
        "district": "حدة",
        "delivery_type": "عادي",
        "delivery_cost": "500.00",
        "payment_method": "نقدًا عند التسليم",
        "payment_status": "تم الدفع",
        "payment_amount": "25.00",
        "currency": "YER",
        "total_amount": "1750.00",
        "items_json": json.dumps([{"sku": "P-1", "name": "Product", "qty": 1, "unit_price": 1250.00, "total": 1250.00}], ensure_ascii=False),
    }


def test_schema_validation_checks_required_fields():
    errors = validate_raw_schema({"order_id": "ORD-1", "customer_id": "C-1"})
    assert {item["field"] for item in errors} >= {"order_date", "items_json"}


def test_duplicate_detection_is_recorded_after_validation():
    result = classify_raw_document(canonical_raw(), is_duplicate=True)
    assert result["initial_classification"] == "invalid"
    assert "DUPLICATE_ORDER_ID" in result["initial_quarantine"]["error_codes"]
    assert result["final_document"]["validation_stages"] == ["schema_validation", "duplicate_detection"]
    assert result["final_document"]["cleaning_applied"] is False


def test_batch_replay_is_idempotent(tmp_path):
    source = tmp_path / "replay.csv"
    source.write_text("order_id,order_date,status,customer_id,customer_phone,customer_email,city,district,delivery_cost,payment_method,payment_status,payment_amount,currency,total_amount,items_json\nREPLAY-1,2025-01-31,مؤكد,C-1,967771234567,user@mail.com,صنعاء,حدة,500,نقدًا عند التسليم,تم الدفع,25,YER,1750,\"[{\\\"sku\\\":\\\"P\\\",\\\"qty\\\":1,\\\"unit_price\\\":1250,\\\"total\\\":1250}]\"\n", encoding="utf-8")
    store = JsonStore(tmp_path / "store.json")
    load_csv_streaming(source, store, run_id="replay-run", batch_size=1, reports_dir=tmp_path / "reports")
    first_final = len(store.data["orders_validated"]) + len(store.data["orders_quarantine"])
    load_csv_streaming(source, store, run_id="replay-run", batch_size=1, reports_dir=tmp_path / "reports")
    second_final = len(store.data["orders_validated"]) + len(store.data["orders_quarantine"])
    assert second_final == first_final


def test_raw_then_cleaning_updates_final_state(tmp_path):
    source = tmp_path / "raw_then_clean.csv"
    raw = canonical_raw()
    quarantined = canonical_raw()
    quarantined["order_id"] = "ORD-2"
    quarantined["items_json"] = ""
    headers = [
        "order_id", "order_date", "status", "customer_id", "customer_name", "customer_phone", "customer_email",
        "city", "district", "delivery_type", "delivery_cost", "payment_method", "payment_status", "payment_amount",
        "currency", "total_amount", "items_json",
    ]
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerow({header: raw.get(header, "") for header in headers})
        writer.writerow({header: quarantined.get(header, "") for header in headers})
    store = JsonStore(tmp_path / "sequence_store.json")
    raw_result = load_csv_streaming(source, store, run_id="sequence-run", batch_size=1, reports_dir=tmp_path / "reports")
    assert raw_result["raw_valid_count"] == 1
    assert raw_result["raw_invalid_count"] == 1
    assert raw_result["cleaning_applied"] is False
    assert len(store.data["orders_validated"]) == 1
    assert store.data["orders_validated"][0]["quality_status"] == "raw_validated"
    assert store.data["orders_validated"][0]["cleaning_applied"] is False
    assert len(store.data["orders_quarantine"]) == 1
    final = clean_after_raw_batch(store, "sequence-run", reports_dir=tmp_path / "reports", raw_valid_count=1, raw_invalid_count=1)
    assert final["cleaning_applied"] is True
    assert final["cleaning_input"] == "orders_quarantine_only"
    assert final["valid_count"] == 1
    assert final["corrected_count"] == 0
    assert final["quarantine_count"] == 1
    assert len(store.data["orders_validated"]) == 1
    original = next(row for row in store.data["orders_validated"] if row["order_id"] == "ORD-1")
    assert original["cleaning_applied"] is False
    assert len(store.data["orders_quarantine"]) == 1
    assert store.data["orders_quarantine"][0]["cleaning_applied"] is True
    assert any(code in store.data["orders_quarantine"][0]["error_codes"] for code in ("SCHEMA_REQUIRED_FIELD", "EMPTY_ITEMS"))


def test_uncorrectable_quarantine_remains_after_cleaning(tmp_path):
    source = tmp_path / "uncorrectable.csv"
    raw = canonical_raw()
    raw["items_json"] = ""
    headers = [
        "order_id", "order_date", "status", "customer_id", "customer_name", "customer_phone", "customer_email",
        "city", "district", "delivery_type", "delivery_cost", "payment_method", "payment_status", "payment_amount",
        "currency", "total_amount", "items_json",
    ]
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerow({header: raw.get(header, "") for header in headers})
    store = JsonStore(tmp_path / "uncorrectable_store.json")
    raw_result = load_csv_streaming(source, store, run_id="uncorrectable-run", batch_size=1, reports_dir=tmp_path / "reports")
    assert raw_result["raw_valid_count"] == 0
    assert raw_result["raw_invalid_count"] == 1
    final = clean_after_raw_batch(store, "uncorrectable-run", reports_dir=tmp_path / "reports", raw_valid_count=0, raw_invalid_count=1)
    assert final["corrected_count"] == 0
    assert final["quarantine_count"] == 1
    assert len(store.data["orders_validated"]) == 0
    assert len(store.data["orders_quarantine"]) == 1
    assert store.data["orders_quarantine"][0]["cleaning_applied"] is True
    assert any(code in store.data["orders_quarantine"][0]["error_codes"] for code in ("SCHEMA_REQUIRED_FIELD", "EMPTY_ITEMS"))


def test_raw_valid_record_is_saved_without_cleaning():
    result = classify_raw_without_cleaning(canonical_raw())
    assert result["raw_valid"] is True
    assert result["raw_invalid"] is False
    assert result["validated_document"]["quality_status"] == "raw_validated"
    assert result["validated_document"]["cleaning_applied"] is False
    assert result["validated_document"]["corrections"] == []


def test_raw_invalid_record_is_quarantined_without_cleaning():
    raw = canonical_raw()
    raw["order_id"] = ""
    result = classify_raw_without_cleaning(raw)
    assert result["raw_valid"] is False
    assert result["raw_invalid"] is True
    assert result["quarantine_document"]["cleaning_applied"] is False
    assert any(code in result["quarantine_document"]["error_codes"] for code in ("SCHEMA_REQUIRED_FIELD", "MISSING_ORDER_ID"))
    assert result["quarantine_document"]["corrections"] == []


def test_business_error_is_quarantined_before_cleaning():
    raw = canonical_raw()
    raw["customer_email"] = "invalid-email-no-domain"
    result = classify_raw_without_cleaning(raw)
    assert result["raw_valid"] is False
    assert result["raw_invalid"] is True
    assert result["cleaning_applied"] is False
    assert "INVALID_EMAIL" in result["quarantine_document"]["error_codes"]
    assert result["quarantine_document"]["quality_status"] == "raw_quarantined"



def test_valid_record_is_classified_before_writing():
    result = classify_raw_document(canonical_raw())
    assert result["initial_classification"] == "valid"
    assert result["initial_quarantine"] is None
    assert result["final_document"]["cleaning_applied"] is True
    assert result["final_document"]["validation_stages"] == ["schema_validation", "duplicate_detection", "business_validation", "cleaning_last"]


def test_dirty_record_is_cleaned_last_then_quarantined():
    raw = canonical_raw()
    raw["customer_email"] = "bad-email"
    result = classify_raw_document(raw)
    assert result["initial_classification"] == "valid"
    assert result["final_document"]["cleaning_applied"] is True
    assert result["final_document"]["quality_status"] == "quarantined"
    assert "INVALID_EMAIL" in result["final_document"]["error_codes"]


def test_dynamic_discovery_supports_small_semicolon_alias_file(tmp_path):
    source = tmp_path / "tiny_semicolon.csv"
    source.write_text("order id;order date;customer id;order_items\nA-1;2025-01-31;C-1;[]\n", encoding="utf-8")
    discovery = discover_file(source, threshold_mb=200)
    assert discovery.engine_used == "python_batch"
    assert discovery.delimiter == ";"
    assert discovery.header_check == "pass"


def test_dynamic_batch_handles_header_only_file(tmp_path):
    source = tmp_path / "header_only.csv"
    source.write_text("order_id,order_date,customer_id,items_json\n", encoding="utf-8")
    store = JsonStore(tmp_path / "empty_store.json")
    result = load_csv_streaming(source, store, run_id="empty-run", batch_size=2, reports_dir=tmp_path / "reports")
    assert result["raw_loaded"] == 0
    assert result["raw_valid_count"] == 0
    assert result["raw_invalid_count"] == 0
    assert result["reconciliation_ok"] is True
