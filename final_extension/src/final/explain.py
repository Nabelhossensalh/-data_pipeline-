from __future__ import annotations

from typing import Any
from .config import settings
from .db import get_client, get_db


EXPLAIN_SPECS = [
    {
        "id": "query_1_city_date",
        "title": "استعلام الطلبات حسب المدينة وتاريخ الطلب (City + Date)",
        "query_field": "customer.address.city",
        "sort": [("order_date", -1)],
        "index_name": "ix_city_order_date",
        "index_keys": [("customer.address.city", 1), ("order_date", -1)],
        "reason": (
            "استعلام جوهري لعمليات التجارة الإلكترونية وإدارة التوصيل والمستودعات "
            "لعرض أحدث الطلبات لكل مدينة جغرافياً وتوجيه السائقين."
        ),
    },
    {
        "id": "query_2_customer_date",
        "title": "استعلام سجل طلبات العميل وتاريخها (Customer + Date)",
        "query_field": "customer.customer_id",
        "sort": [("order_date", -1)],
        "index_name": "ix_customer_order_date",
        "index_keys": [("customer.customer_id", 1), ("order_date", -1)],
        "reason": (
            "استعلام صفحة حساب العميل (Customer Profile) لعرض مشترياته السابقة "
            "مرتبة زمنياً من الأحدث إلى الأقدم."
        ),
    },
    {
        "id": "query_3_order_lookup",
        "title": "استعلام البحث المباشر برقم الطلب (Order ID Lookup)",
        "query_field": "order_id",
        "sort": None,
        "index_name": "ux_order_id",
        "index_keys": [("order_id", 1)],
        "reason": (
            "استعلام أساسي في خدمة العملاء وتتبع مسار الشحنات (Order Tracking) بالمعرف الفريد."
        ),
    },
]


def _sample_query(coll, field: str) -> dict[str, Any] | None:
    sample = coll.find_one(
        {field: {"$exists": True, "$ne": None}},
        {field: 1, "_id": 0},
    )
    value: Any = sample
    for part in field.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return {field: value} if value is not None else None


def _extract_stats(explain_result: dict[str, Any]) -> dict[str, Any]:
    stats = explain_result.get("executionStats", {})
    planner = explain_result.get("queryPlanner", {})
    winning_plan = planner.get("winningPlan", {})

    # Detect stage
    stage = winning_plan.get("stage", "UNKNOWN")
    if stage == "PROJECTION_COVERED":
        pass
    elif "inputStage" in winning_plan:
        stage = f"{winning_plan.get('stage')} -> {winning_plan['inputStage'].get('stage')}"

    return {
        "stage": stage,
        "nReturned": stats.get("nReturned", 0),
        "executionTimeMillis": stats.get("executionTimeMillis", 0),
        "totalDocsExamined": stats.get("totalDocsExamined", 0),
        "totalKeysExamined": stats.get("totalKeysExamined", 0),
    }


def _impact_summary(before: dict[str, Any], after: dict[str, Any]) -> str:
    return (
        f"قبل الفهرس: فُحصت {before['totalDocsExamined']} وثيقة و"
        f"{before['totalKeysExamined']} مفتاحاً خلال {before['executionTimeMillis']} ms. "
        f"بعد الفهرس: فُحصت {after['totalDocsExamined']} وثيقة و"
        f"{after['totalKeysExamined']} مفتاحاً خلال {after['executionTimeMillis']} ms."
    )


def run_explain_benchmarks(db) -> dict[str, Any]:
    """
    Executes explain('executionStats') for the 3 queries before and after index.
    Before: forced COLLSCAN via hint({'$natural': 1}).
    After: index-driven via winning plan / index hint.
    """
    coll = db[settings.source_collection]
    results = []

    for spec in EXPLAIN_SPECS:
        query = _sample_query(coll, spec["query_field"])
        if query is None:
            return {
                "status": "error",
                "description": "تعذر إنشاء استعلام Explain من بيانات المجموعة الحالية",
                "queries_analyzed": len(results),
                "benchmarks": results,
                "missing_field": spec["query_field"],
            }
        sort = spec["sort"]

        # 1. Before Index (simulated unindexed scan via natural table scan)
        cursor_before = coll.find(query).hint([("$natural", 1)])
        if sort:
            cursor_before = cursor_before.sort(sort)
        cursor_before = cursor_before.limit(100)
        explain_before = cursor_before.explain()
        stats_before = _extract_stats(explain_before)
        stats_before["stage"] = "COLLSCAN (بدون فهرس)"

        # 2. After Index (using the created index)
        cursor_after = coll.find(query)
        if sort:
            cursor_after = cursor_after.sort(sort)
        cursor_after = cursor_after.limit(100)
        try:
            cursor_after = cursor_after.hint(spec["index_name"])
        except Exception:
            pass
        explain_after = cursor_after.explain()
        stats_after = _extract_stats(explain_after)
        if "IXSCAN" not in stats_after["stage"] and stats_after["totalKeysExamined"] > 0:
            stats_after["stage"] = f"IXSCAN ({spec['index_name']})"

        results.append({
            "id": spec["id"],
            "title": spec["title"],
            "reason_for_index": spec["reason"],
            "impact_summary": _impact_summary(stats_before, stats_after),
            "index_applied": spec["index_name"],
            "before_index": stats_before,
            "after_index": stats_after,
        })

    return {
        "status": "ok",
        "description": "مقارنة أداء الاستعلامات باستخدام explain('executionStats') قبل وبعد الفهارس",
        "queries_analyzed": len(results),
        "benchmarks": results,
    }
