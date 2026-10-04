# from __future__ import annotations

# import json
# from datetime import datetime, timezone
# from typing import Any

# from pymongo import ASCENDING, DESCENDING

# from .config import settings


# # ============================================================
# # Helpers
# # ============================================================

# def utcnow() -> datetime:
#     return datetime.now(timezone.utc)


# def _delivered(document: dict[str, Any]) -> bool:
#     return document.get("status") == settings.delivered_status


# def _city_parts(document: dict[str, Any]) -> dict[str, Any]:
#     city = (
#         document.get("customer", {})
#         .get("address", {})
#         .get("city")
#     )
#     try:
#         amount = float(document.get("total_amount") or 0)
#     except (ValueError, TypeError):
#         amount = 0.0

#     if not city:
#         city = "UNKNOWN"

#     return {
#         "city": city,
#         "total_sales": amount,
#         "orders_count": 1,
#     }


# def _delivered_part(doc: dict[str, Any]) -> dict[str, Any] | None:
#     """
#     Extract delivered order contribution for city sales.
#     Returns None if the order is not delivered or has no city.
#     """
#     if not doc or doc.get("status") != settings.delivered_status:
#         return None
#     city = (doc.get("customer") or {}).get("address", {}).get("city")
#     if not city:
#         return None
#     try:
#         amount = float(doc.get("total_amount") or 0)
#     except (ValueError, TypeError):
#         amount = 0.0
#     return {"city": city, "total_sales": amount, "orders_count": 1}


# def _date_part(doc: dict[str, Any]) -> dict[str, Any] | None:
#     """
#     Extract date contribution (YYYY-MM-DD) for daily_sales_summary.
#     """
#     if not doc or doc.get("status") != settings.delivered_status:
#         return None
#     order_date = doc.get("order_date")
#     if not order_date:
#         return None
#     date_str = str(order_date)[:10]
#     if len(date_str) < 10 or "-" not in date_str:
#         return None
#     try:
#         amount = float(doc.get("total_amount") or 0)
#     except (ValueError, TypeError):
#         amount = 0.0
#     return {"date": date_str, "total_sales": amount, "orders_count": 1}


# def _product_parts(document: dict[str, Any]) -> list[dict[str, Any]]:
#     """
#     Extract list of items with SKU, name, qty, and total sales.
#     Handles both array of dicts and serialized JSON string.
#     """
#     if not document or document.get("status") != settings.delivered_status:
#         return []

#     items = document.get("items") or []
#     if isinstance(items, str):
#         try:
#             items = json.loads(items)
#         except Exception:
#             items = []

#     if not isinstance(items, list):
#         return []

#     results = []
#     for item in items:
#         if not isinstance(item, dict):
#             continue
#         sku = item.get("sku")
#         if not sku:
#             continue
#         name = item.get("name") or ""
#         try:
#             qty = int(item.get("qty") or 0)
#         except (ValueError, TypeError):
#             qty = 0
#         try:
#             total = float(item.get("total") or (item.get("unit_price", 0) * qty) or 0)
#         except (ValueError, TypeError):
#             total = 0.0

#         results.append({
#             "sku": sku,
#             "name": name,
#             "units": qty,
#             "sales": total,
#         })
#     return results


# # ============================================================
# # Full Refresh
# # ============================================================

# def full_refresh(db) -> dict[str, Any]:
#     """
#     Rebuild the materialized views and initialize snapshots.
#     Populates:
#       - mv_sales_by_city / daily_sales_summary
#       - mv_top_products / top_products_summary
#     """
#     source = db[settings.source_collection]
#     city_mv = db[settings.mv_city]
#     product_mv = db[settings.mv_products]
#     daily_mv = db["daily_sales_summary"]
#     top_prod_mv = db["top_products_summary"]
#     state = db[settings.state]

#     # Clear target collections
#     city_mv.delete_many({})
#     product_mv.delete_many({})
#     daily_mv.delete_many({})
#     top_prod_mv.delete_many({})

#     # 1. City Sales MV
#     city_pipeline = [
#         {"$match": {"status": settings.delivered_status}},
#         {
#             "$group": {
#                 "_id": "$customer.address.city",
#                 "total_sales": {
#                     "$sum": {
#                         "$convert": {
#                             "input": "$total_amount",
#                             "to": "double",
#                             "onError": 0.0,
#                             "onNull": 0.0,
#                         }
#                     }
#                 },
#                 "orders_count": {"$sum": 1},
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "city": {"$ifNull": ["$_id", "UNKNOWN"]},
#                 "total_sales": 1,
#                 "orders_count": 1,
#             }
#         },
#     ]
#     city_rows = list(source.aggregate(city_pipeline, allowDiskUse=True))
#     if city_rows:
#         city_mv.insert_many(city_rows)

#     # 2. Daily Sales Summary (doctor's requested view)
#     daily_pipeline = [
#         {"$match": {"status": settings.delivered_status}},
#         {
#             "$set": {
#                 "_date_obj": {
#                     "$convert": {
#                         "input": "$order_date",
#                         "to": "date",
#                         "onError": None,
#                         "onNull": None,
#                     }
#                 }
#             }
#         },
#         {"$match": {"_date_obj": {"$ne": None}}},
#         {
#             "$group": {
#                 "_id": {
#                     "$dateToString": {"format": "%Y-%m-%d", "date": "$_date_obj"}
#                 },
#                 "total_sales": {
#                     "$sum": {
#                         "$convert": {
#                             "input": "$total_amount",
#                             "to": "double",
#                             "onError": 0.0,
#                             "onNull": 0.0,
#                         }
#                     }
#                 },
#                 "orders_count": {"$sum": 1},
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "date": "$_id",
#                 "total_sales": 1,
#                 "orders_count": 1,
#             }
#         },
#         {"$sort": {"date": 1}},
#     ]
#     daily_rows = list(source.aggregate(daily_pipeline, allowDiskUse=True))
#     if daily_rows:
#         daily_mv.insert_many(daily_rows)

#     # 3. Product Summary MV
#     product_map: dict[str, dict[str, Any]] = {}
#     cursor = source.find({"status": settings.delivered_status}, {"items": 1})
#     for doc in cursor:
#         for p in _product_parts(doc):
#             sku = p["sku"]
#             if sku not in product_map:
#                 product_map[sku] = {
#                     "sku": sku,
#                     "name": p["name"],
#                     "units": p["units"],
#                     "sales": p["sales"],
#                 }
#             else:
#                 product_map[sku]["units"] += p["units"]
#                 product_map[sku]["sales"] += p["sales"]
#                 if p["name"]:
#                     product_map[sku]["name"] = p["name"]

#     product_rows = list(product_map.values())
#     if product_rows:
#         product_mv.insert_many(product_rows)
#         # top_products_summary contains top products sorted by sales
#         sorted_top = sorted(product_rows, key=lambda x: x["sales"], reverse=True)[:100]
#         top_prod_mv.insert_many(sorted_top)

#     # 4. Build incremental state snapshots & watermark
#     state.delete_many({})
#     snapshots = []
#     latest_updated_at = None

#     cursor = source.find({}, {"_id": 0})
#     for document in cursor:
#         order_id = document.get("order_id")
#         if not order_id:
#             continue

#         updated_at = document.get("mv_updated_at")
#         if updated_at is not None:
#             if latest_updated_at is None or updated_at > latest_updated_at:
#                 latest_updated_at = updated_at

#         snapshots.append(
#             {
#                 "_id": f"order:{order_id}",
#                 "order_id": order_id,
#                 "document": document,
#             }
#         )

#         if len(snapshots) >= 1000:
#             state.insert_many(snapshots)
#             snapshots = []

#     if snapshots:
#         state.insert_many(snapshots)

#     # Set watermark
#     state.replace_one(
#         {"_id": "mv_incremental_all"},
#         {
#             "_id": "mv_incremental_all",
#             "watermark": latest_updated_at,
#             "updated_at": utcnow(),
#         },
#         upsert=True,
#     )

#     # Ensure indexes on MVs
#     city_mv.create_index([("city", ASCENDING)], name="ix_mv_city")
#     daily_mv.create_index([("date", ASCENDING)], unique=True, name="ux_daily_date")
#     product_mv.create_index([("sku", ASCENDING)], unique=True, name="ux_mv_product_sku")
#     top_prod_mv.create_index([("sku", ASCENDING)], unique=True, name="ux_top_product_sku")

#     return {
#         "status": "ok",
#         "mode": "full",
#         "city_rows": len(city_rows),
#         "daily_rows": len(daily_rows),
#         "product_rows": len(product_rows),
#         "snapshots_initialized": True,
#         "watermark": (latest_updated_at.isoformat() if hasattr(latest_updated_at, "isoformat") else str(latest_updated_at)),
#     }


# # ============================================================
# # Incremental Update Application
# # ============================================================

# def _apply_city(db, document: dict[str, Any], sign: int) -> None:
#     part = _delivered_part(document)
#     if not part:
#         return

#     city = part["city"]
#     for coll_name in (settings.mv_city,):
#         db[coll_name].update_one(
#             {"city": city},
#             {
#                 "$inc": {
#                     "total_sales": sign * part["total_sales"],
#                     "orders_count": sign * part["orders_count"],
#                 }
#             },
#             upsert=True,
#         )
#         db[coll_name].delete_many({"orders_count": {"$lte": 0}})


# def _apply_daily(db, document: dict[str, Any], sign: int) -> None:
#     part = _date_part(document)
#     if not part:
#         return

#     db["daily_sales_summary"].update_one(
#         {"date": part["date"]},
#         {
#             "$inc": {
#                 "total_sales": sign * part["total_sales"],
#                 "orders_count": sign * part["orders_count"],
#             }
#         },
#         upsert=True,
#     )
#     db["daily_sales_summary"].delete_many({"orders_count": {"$lte": 0}})


# def _apply_products(db, document: dict[str, Any], sign: int) -> None:
#     parts = _product_parts(document)
#     for part in parts:
#         for coll_name in (settings.mv_products, "top_products_summary"):
#             db[coll_name].update_one(
#                 {"sku": part["sku"]},
#                 {
#                     "$set": {"name": part["name"]},
#                     "$inc": {
#                         "units": sign * part["units"],
#                         "sales": sign * part["sales"],
#                     },
#                 },
#                 upsert=True,
#             )
#             db[coll_name].delete_many({"units": {"$lte": 0}})


# def apply_change(
#     db,
#     old_document: dict[str, Any] | None,
#     new_document: dict[str, Any] | None,
# ) -> None:
#     if old_document:
#         _apply_city(db, old_document, -1)
#         _apply_daily(db, old_document, -1)
#         _apply_products(db, old_document, -1)

#     if new_document:
#         _apply_city(db, new_document, 1)
#         _apply_daily(db, new_document, 1)
#         _apply_products(db, new_document, 1)


# # ============================================================
# # Incremental Refresh
# # ============================================================

# def incremental_refresh(db) -> dict[str, Any]:
#     source = db[settings.source_collection]
#     state = db[settings.state]

#     state_doc = state.find_one({"_id": "mv_incremental_all"})
#     if not state_doc:
#         return {
#             "status": "error",
#             "message": "Materialized views are not initialized. Run full refresh first.",
#         }

#     watermark = state_doc.get("watermark")
#     query = {}
#     if watermark is not None:
#         query["mv_updated_at"] = {"$gt": watermark}

#     documents = list(
#         source.find(query).sort("mv_updated_at", ASCENDING)
#     )

#     processed = 0
#     latest_watermark = watermark

#     for new_document in documents:
#         order_id = new_document.get("order_id")
#         if not order_id:
#             continue

#         previous_state = state.find_one({"_id": f"order:{order_id}"})
#         old_document = previous_state.get("document") if previous_state else None

#         apply_change(db, old_document, new_document)

#         state.replace_one(
#             {"_id": f"order:{order_id}"},
#             {
#                 "_id": f"order:{order_id}",
#                 "order_id": order_id,
#                 "document": new_document,
#             },
#             upsert=True,
#         )

#         updated_at = new_document.get("mv_updated_at")
#         if updated_at is not None:
#             if latest_watermark is None or updated_at > latest_watermark:
#                 latest_watermark = updated_at

#         processed += 1

#     state.replace_one(
#         {"_id": "mv_incremental_all"},
#         {
#             "_id": "mv_incremental_all",
#             "watermark": latest_watermark,
#             "updated_at": utcnow(),
#         },
#         upsert=True,
#     )

#     return {
#         "status": "ok",
#         "mode": "incremental",
#         "processed_documents": processed,
#         "previous_watermark": str(watermark),
#         "new_watermark": str(latest_watermark),
#     }


# # ============================================================
# # Top Products From MV
# # ============================================================

# def top_products_from_mv(
#     db,
#     limit: int = 20,
# ) -> dict[str, Any]:
#     limit = max(1, min(limit, 1000))
#     rows = list(
#         db[settings.mv_products]
#         .find({}, {"_id": 0})
#         .sort("sales", DESCENDING)
#         .limit(limit)
#     )
#     return {
#         "name": "top_products_from_mv",
#         "limit": limit,
#         "rows": len(rows),
#         "data": rows,
#     }










from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING, DESCENDING

from .config import settings


# ============================================================
# Helpers
# ============================================================

def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _delivered(document: dict[str, Any]) -> bool:
    return document.get("status") == settings.delivered_status


def _city_parts(document: dict[str, Any]) -> dict[str, Any]:
    city = (
        document.get("customer", {})
        .get("address", {})
        .get("city")
    )
    try:
        amount = float(document.get("total_amount") or 0)
    except (ValueError, TypeError):
        amount = 0.0

    if not city:
        city = "UNKNOWN"

    return {
        "city": city,
        "total_sales": amount,
        "orders_count": 1,
    }


def _delivered_part(doc: dict[str, Any]) -> dict[str, Any] | None:
    """
    Extract delivered order contribution for city sales.
    Returns None if the order is not delivered or has no city.
    """
    if not doc or doc.get("status") != settings.delivered_status:
        return None
    city = (doc.get("customer") or {}).get("address", {}).get("city")
    if not city:
        return None
    try:
        amount = float(doc.get("total_amount") or 0)
    except (ValueError, TypeError):
        amount = 0.0
    return {"city": city, "total_sales": amount, "orders_count": 1}


def _date_part(doc: dict[str, Any]) -> dict[str, Any] | None:
    """
    Extract date contribution (YYYY-MM-DD) for daily_sales_summary.
    """
    if not doc or doc.get("status") != settings.delivered_status:
        return None
    order_date = doc.get("order_date")
    if not order_date:
        return None
    date_str = str(order_date)[:10]
    if len(date_str) < 10 or "-" not in date_str:
        return None
    try:
        amount = float(doc.get("total_amount") or 0)
    except (ValueError, TypeError):
        amount = 0.0
    return {"date": date_str, "total_sales": amount, "orders_count": 1}


def _product_parts(document: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Extract list of items with SKU, name, qty, and total sales.
    Handles both array of dicts and serialized JSON string.
    """
    if not document or document.get("status") != settings.delivered_status:
        return []

    items = document.get("items") or []
    if isinstance(items, str):
        try:
            items = json.loads(items)
        except Exception:
            items = []

    if not isinstance(items, list):
        return []

    results = []
    for item in items:
        if not isinstance(item, dict):
            continue
        sku = item.get("sku")
        if not sku:
            continue
        name = item.get("name") or ""
        try:
            qty = int(item.get("qty") or 0)
        except (ValueError, TypeError):
            qty = 0
        try:
            total = float(item.get("total") or (item.get("unit_price", 0) * qty) or 0)
        except (ValueError, TypeError):
            total = 0.0

        results.append({
            "sku": sku,
            "name": name,
            "units": qty,
            "sales": total,
        })
    return results


# ============================================================
# Full Refresh
# ============================================================

def full_refresh(db) -> dict[str, Any]:
    """
    Rebuild the materialized views and initialize snapshots.
    Populates:
      - mv_sales_by_city / daily_sales_summary
      - mv_top_products / top_products_summary
    """
    source = db[settings.source_collection]
    city_mv = db[settings.mv_city]
    product_mv = db[settings.mv_products]
    daily_mv = db["daily_sales_summary"]
    top_prod_mv = db["top_products_summary"]
    state = db[settings.state]

    # Clear target collections
    city_mv.delete_many({})
    product_mv.delete_many({})
    daily_mv.delete_many({})
    top_prod_mv.delete_many({})

    # 1. City Sales MV
    city_pipeline = [
        {"$match": {"status": settings.delivered_status}},
        {
            "$group": {
                "_id": "$customer.address.city",
                "total_sales": {
                    "$sum": {
                        "$convert": {
                            "input": "$total_amount",
                            "to": "double",
                            "onError": 0.0,
                            "onNull": 0.0,
                        }
                    }
                },
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
    ]
    city_rows = list(source.aggregate(city_pipeline, allowDiskUse=True))
    if city_rows:
        city_mv.insert_many(city_rows)

    # 2. Daily Sales Summary (doctor's requested view)
    daily_pipeline = [
        {"$match": {"status": settings.delivered_status}},
        {
            "$set": {
                "_date_obj": {
                    "$convert": {
                        "input": "$order_date",
                        "to": "date",
                        "onError": None,
                        "onNull": None,
                    }
                }
            }
        },
        {"$match": {"_date_obj": {"$ne": None}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$_date_obj"}
                },
                "total_sales": {
                    "$sum": {
                        "$convert": {
                            "input": "$total_amount",
                            "to": "double",
                            "onError": 0.0,
                            "onNull": 0.0,
                        }
                    }
                },
                "orders_count": {"$sum": 1},
            }
        },
        {
            "$project": {
                "_id": 0,
                "date": "$_id",
                "total_sales": 1,
                "orders_count": 1,
            }
        },
        {"$sort": {"date": 1}},
    ]
    daily_rows = list(source.aggregate(daily_pipeline, allowDiskUse=True))
    if daily_rows:
        daily_mv.insert_many(daily_rows)

    # 3. Product Summary MV
    product_map: dict[str, dict[str, Any]] = {}
    cursor = source.find({"status": settings.delivered_status}, {"items": 1})
    for doc in cursor:
        for p in _product_parts(doc):
            sku = p["sku"]
            if sku not in product_map:
                product_map[sku] = {
                    "sku": sku,
                    "name": p["name"],
                    "units": p["units"],
                    "sales": p["sales"],
                }
            else:
                product_map[sku]["units"] += p["units"]
                product_map[sku]["sales"] += p["sales"]
                if p["name"]:
                    product_map[sku]["name"] = p["name"]

    product_rows = list(product_map.values())
    if product_rows:
        product_mv.insert_many(product_rows)
        # top_products_summary contains top products sorted by sales
        sorted_top = sorted(product_rows, key=lambda x: x["sales"], reverse=True)[:100]
        top_prod_mv.insert_many(sorted_top)

    # 4. Build incremental state snapshots & watermark
    state.delete_many({})
    snapshots = []
    latest_updated_at = None

    cursor = source.find({}, {"_id": 0})
    for document in cursor:
        order_id = document.get("order_id")
        if not order_id:
            continue

        updated_at = _document_updated_at(document)
        if updated_at is not None:
            if latest_updated_at is None or updated_at > latest_updated_at:
                latest_updated_at = updated_at

        snapshots.append(
            {
                "_id": f"order:{order_id}",
                "order_id": order_id,
                "document": document,
            }
        )

        if len(snapshots) >= 1000:
            state.insert_many(snapshots)
            snapshots = []

    if snapshots:
        state.insert_many(snapshots)

    latest_updated_at = _resolve_watermark(latest_updated_at, None)

    # Set watermark
    state.replace_one(
        {"_id": "mv_incremental_all"},
        {
            "_id": "mv_incremental_all",
            "watermark": latest_updated_at,
            "updated_at": utcnow(),
        },
        upsert=True,
    )

    # Ensure indexes on MVs
    city_mv.create_index([("city", ASCENDING)], name="ix_mv_city")
    daily_mv.create_index([("date", ASCENDING)], unique=True, name="ux_daily_date")
    product_mv.create_index([("sku", ASCENDING)], unique=True, name="ux_mv_product_sku")
    top_prod_mv.create_index([("sku", ASCENDING)], unique=True, name="ux_top_product_sku")

    return {
        "status": "ok",
        "mode": "full",
        "city_rows": len(city_rows),
        "daily_rows": len(daily_rows),
        "product_rows": len(product_rows),
        "snapshots_initialized": True,
        "watermark": (latest_updated_at.isoformat() if hasattr(latest_updated_at, "isoformat") else str(latest_updated_at)),
    }


# ============================================================
# Incremental Update Application
# ============================================================


def _document_updated_at(document: dict[str, Any]):
    timestamps = [
        document.get("mv_updated_at"),
        document.get("processed_at"),
    ]
    timestamps = [timestamp for timestamp in timestamps if timestamp is not None]
    return max(timestamps) if timestamps else None


def _resolve_watermark(watermark, refreshed_at):
    if watermark is not None:
        return watermark
    return refreshed_at or utcnow()


def _incremental_query(watermark):
    if watermark is None:
        return {}
    return {
        "$or": [
            {"mv_updated_at": {"$gt": watermark}},
            {"processed_at": {"$gt": watermark}},
        ]
    }


def _apply_city(db, document: dict[str, Any], sign: int) -> None:
    part = _delivered_part(document)
    if not part:
        return

    city = part["city"]
    for coll_name in (settings.mv_city,):
        db[coll_name].update_one(
            {"city": city},
            {
                "$inc": {
                    "total_sales": sign * part["total_sales"],
                    "orders_count": sign * part["orders_count"],
                }
            },
            upsert=True,
        )
        db[coll_name].delete_many({"orders_count": {"$lte": 0}})


def _apply_daily(db, document: dict[str, Any], sign: int) -> None:
    part = _date_part(document)
    if not part:
        return

    db["daily_sales_summary"].update_one(
        {"date": part["date"]},
        {
            "$inc": {
                "total_sales": sign * part["total_sales"],
                "orders_count": sign * part["orders_count"],
            }
        },
        upsert=True,
    )
    db["daily_sales_summary"].delete_many({"orders_count": {"$lte": 0}})


def _apply_products(db, document: dict[str, Any], sign: int) -> None:
    parts = _product_parts(document)
    for part in parts:
        for coll_name in (settings.mv_products, "top_products_summary"):
            db[coll_name].update_one(
                {"sku": part["sku"]},
                {
                    "$set": {"name": part["name"]},
                    "$inc": {
                        "units": sign * part["units"],
                        "sales": sign * part["sales"],
                    },
                },
                upsert=True,
            )
            db[coll_name].delete_many({"units": {"$lte": 0}})


def apply_change(
    db,
    old_document: dict[str, Any] | None,
    new_document: dict[str, Any] | None,
) -> None:
    if old_document:
        _apply_city(db, old_document, -1)
        _apply_daily(db, old_document, -1)
        _apply_products(db, old_document, -1)

    if new_document:
        _apply_city(db, new_document, 1)
        _apply_daily(db, new_document, 1)
        _apply_products(db, new_document, 1)


# ============================================================
# Incremental Refresh
# ============================================================

def incremental_refresh(db) -> dict[str, Any]:
    source = db[settings.source_collection]
    state = db[settings.state]

    state_doc = state.find_one({"_id": "mv_incremental_all"})
    if not state_doc:
        return {
            "status": "error",
            "message": "Materialized views are not initialized. Run full refresh first.",
        }

    watermark = _resolve_watermark(
        state_doc.get("watermark"),
        state_doc.get("updated_at"),
    )
    if state_doc.get("watermark") is None:
        state.update_one(
            {"_id": "mv_incremental_all"},
            {"$set": {"watermark": watermark}},
        )
    query = _incremental_query(watermark)

    documents = list(
        source.find(query).sort("mv_updated_at", ASCENDING)
    )

    processed = 0
    latest_watermark = watermark

    for new_document in documents:
        order_id = new_document.get("order_id")
        if not order_id:
            continue

        previous_state = state.find_one({"_id": f"order:{order_id}"})
        old_document = previous_state.get("document") if previous_state else None

        apply_change(db, old_document, new_document)

        state.replace_one(
            {"_id": f"order:{order_id}"},
            {
                "_id": f"order:{order_id}",
                "order_id": order_id,
                "document": new_document,
            },
            upsert=True,
        )

        updated_at = _document_updated_at(new_document)
        if updated_at is not None:
            if latest_watermark is None or updated_at > latest_watermark:
                latest_watermark = updated_at

        processed += 1

    state.replace_one(
        {"_id": "mv_incremental_all"},
        {
            "_id": "mv_incremental_all",
            "watermark": latest_watermark,
            "updated_at": utcnow(),
        },
        upsert=True,
    )

    return {
        "status": "ok",
        "mode": "incremental",
        "processed_documents": processed,
        "previous_watermark": str(watermark),
        "new_watermark": str(latest_watermark),
    }


# ============================================================
# Top Products From MV
# ============================================================

def top_products_from_mv(
    db,
    limit: int = 20,
) -> dict[str, Any]:
    limit = max(1, min(limit, 1000))
    rows = list(
        db[settings.mv_products]
        .find({}, {"_id": 0})
        .sort("sales", DESCENDING)
        .limit(limit)
    )
    return {
        "name": "top_products_from_mv",
        "limit": limit,
        "rows": len(rows),
        "data": rows,
    }
