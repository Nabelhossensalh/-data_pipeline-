from __future__ import annotations

import json

from quality_rules import clean_and_validate


def test_cleaning_rules_keep_audit_trail():
    result = clean_and_validate(
        {
            "order_id": "ORD-1",
            "customer_id": "C-1",
            "order_date": "31/01/2025",
            "items": json.dumps([{"sku": "P-1", "name": "Product"}], ensure_ascii=False),
            "customer_email": "user@@mail..com",
        }
    )
    assert result["quality_status"] == "corrected"
    assert result["corrections"]
    assert any(item["rule_code"] == "EMAIL_REPEATED_SYMBOLS" for item in result["corrections"])


def test_cleaning_rules_quarantine_missing_business_key():
    result = clean_and_validate({"order_id": "", "customer_id": "C-1", "order_date": "2025-01-31", "items": "[]"})
    assert result["quality_status"] == "quarantined"
    assert result["error_code"] in {"MISSING_ORDER_ID", "EMPTY_ITEMS"}
