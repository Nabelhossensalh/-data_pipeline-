from __future__ import annotations

from time import perf_counter
from typing import Any

from .config import settings


def _run(db, name: str, pipeline: list[dict[str, Any]]) -> dict[str, Any]:
    started = perf_counter()
    data = list(db[settings.source_collection].aggregate(pipeline, allowDiskUse=True))
    for row in data:
        row.pop("_id", None)
    return {
        "report_name": name,
        "rows": len(data),
        "elapsed_seconds": round(perf_counter() - started, 6),
        "data": data,
    }


def _amount_expr() -> dict[str, Any]:
    return {
        "$convert": {
            "input": "$total_amount",
            "to": "double",
            "onError": 0.0,
            "onNull": 0.0,
        }
    }


def sales_by_city(db):
    return _run(db, "sales_by_city", [
        {"$match": {"status": settings.delivered_status}},
        {
            "$group": {
                "_id": "$customer.address.city",
                "total_sales": {"$sum": _amount_expr()},
                "orders_count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "city": {"$ifNull": ["$_id", "UNKNOWN"]},
                "total_sales": 1,
                "orders_count": 1,
            }
        },
        {"$sort": {"total_sales": -1}},
    ])


def top_products(db):
    """
    Returns top products.
    First tries directly from mv_top_products or aggregated items.
    """
    # If materialized view mv_top_products has data, read from it directly
    if db[settings.mv_products].count_documents({}) > 0:
        started = perf_counter()
        data = list(
            db[settings.mv_products]
            .find({}, {"_id": 0})
            .sort("sales", -1)
            .limit(20)
        )
        return {
            "report_name": "top_products",
            "rows": len(data),
            "elapsed_seconds": round(perf_counter() - started, 6),
            "data": data,
        }

    # Fallback to source aggregation
    return _run(db, "top_products", [
        {"$match": {"status": settings.delivered_status}},
        {"$unwind": "$items"},
        {
            "$group": {
                "_id": {"sku": "$items.sku", "name": "$items.name"},
                "units": {"$sum": {"$convert": {"input": "$items.qty", "to": "double", "onError": 0.0, "onNull": 0.0}}},
                "sales": {"$sum": {"$convert": {"input": "$items.total", "to": "double", "onError": 0.0, "onNull": 0.0}}},
            }
        },
        {"$project": {"_id": 0, "sku": "$_id.sku", "name": "$_id.name", "units": 1, "sales": 1}},
        {"$sort": {"sales": -1}},
        {"$limit": 20},
    ])


def sales_by_period(db):
    return _run(db, "sales_by_period", [
        {"$match": {"status": settings.delivered_status}},
        {"$set": {"_date": {"$convert": {"input": "$order_date", "to": "date", "onError": None, "onNull": None}}}},
        {"$match": {"_date": {"$ne": None}}},
        {
            "$group": {
                "_id": {"year": {"$year": "$_date"}, "month": {"$month": "$_date"}},
                "total_sales": {"$sum": _amount_expr()},
                "orders_count": {"$sum": 1},
            }
        },
        {"$project": {"_id": 0, "year": "$_id.year", "month": "$_id.month", "total_sales": 1, "orders_count": 1}},
        {"$sort": {"year": 1, "month": 1}},
    ])


def top_customers(db):
    return _run(db, "top_customers", [
        {"$match": {"status": settings.delivered_status}},
        {
            "$group": {
                "_id": "$customer.customer_id",
                "total_sales": {"$sum": _amount_expr()},
                "orders_count": {"$sum": 1},
            }
        },
        {"$project": {"_id": 0, "customer_id": "$_id", "total_sales": 1, "orders_count": 1}},
        {"$sort": {"total_sales": -1}},
        {"$limit": 20},
    ])


def orders_by_status(db):
    return _run(db, "orders_by_status", [
        {
            "$group": {
                "_id": "$status",
                "orders_count": {"$sum": 1},
                "total_sales": {"$sum": _amount_expr()},
            }
        },
        {"$project": {"_id": 0, "status": "$_id", "orders_count": 1, "total_sales": 1}},
        {"$sort": {"orders_count": -1}},
    ])


REPORTS = {
    "sales_by_city": sales_by_city,
    "top_products": top_products,
    "sales_by_period": sales_by_period,
    "top_customers": top_customers,
    "orders_by_status": orders_by_status,
}
