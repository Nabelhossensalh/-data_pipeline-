# from __future__ import annotations

# from datetime import datetime, timezone
# from typing import Any

# from pymongo import ASCENDING, DESCENDING, MongoClient

# from .config import settings


# def utcnow() -> datetime:
#     return datetime.now(timezone.utc)


# def get_client() -> MongoClient:
#     return MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=10000)


# def get_db(client: MongoClient | None = None):
#     return (client or get_client())[settings.database]


# def ensure_indexes(db) -> dict[str, Any]:
#     result = {}
#     result["validated_order_id"] = db[settings.source_collection].create_index(
#         [("order_id", ASCENDING)], unique=True, name="ux_order_id"
#     )
#     result["validated_city_date"] = db[settings.source_collection].create_index(
#         [("customer.address.city", ASCENDING), ("order_date", DESCENDING)],
#         name="ix_city_order_date",
#     )
#     result["validated_customer_date"] = db[settings.source_collection].create_index(
#         [("customer.customer_id", ASCENDING), ("order_date", DESCENDING)],
#         name="ix_customer_order_date",
#     )
#     result["quarantine_run_errors"] = db["orders_quarantine"].create_index(
#         [("run_id", ASCENDING), ("error_codes", ASCENDING)],
#         name="ix_quarantine_run_errors",
#     )
#     result["events"] = db[settings.events].create_index(
#         [("event_id", ASCENDING)], unique=True, name="ux_event_id"
#     )
#     result["state"] = db[settings.state].create_index(
#         [("_id", ASCENDING)], unique=True, name="ux_mv_state"
#     )
#     return result








from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING, DESCENDING, MongoClient

from .config import settings


def utcnow() -> datetime:
    """
    Return the current UTC time as a timezone-aware datetime.
    """
    return datetime.now(timezone.utc)


def get_client() -> MongoClient:
    """
    Create a MongoDB client using the configured connection string.
    """
    return MongoClient(
        settings.mongo_uri,
        serverSelectionTimeoutMS=10000,
    )


def get_db(client: MongoClient | None = None):
    """
    Return the configured database.

    If a client is supplied, it is reused.
    Otherwise, a new client is created.
    """
    return (client or get_client())[settings.database]


def ensure_indexes(db) -> dict[str, Any]:
    """
    Create all indexes required by the final-phase extension.

    The indexes are created on the independent final-analysis
    collection configured by settings.source_collection.
    """

    result: dict[str, Any] = {}

    # =========================================================
    # 1. Unique lookup by order_id
    # =========================================================
    result["validated_order_id"] = db[
        settings.source_collection
    ].create_index(
        [("order_id", ASCENDING)],
        unique=True,
        name="ux_order_id",
    )

    # =========================================================
    # 2. Compound index:
    #    city + order_date
    #
    # Used for queries such as:
    # - orders from a specific city
    # - recent orders in a specific city
    # =========================================================
    result["validated_city_date"] = db[
        settings.source_collection
    ].create_index(
        [
            ("customer.address.city", ASCENDING),
            ("order_date", DESCENDING),
        ],
        name="ix_city_order_date",
    )

    # =========================================================
    # 3. Compound index:
    #    customer_id + order_date
    #
    # Used for queries such as:
    # - customer's orders
    # - recent orders for a specific customer
    # =========================================================
    result["validated_customer_date"] = db[
        settings.source_collection
    ].create_index(
        [
            ("customer.customer_id", ASCENDING),
            ("order_date", DESCENDING),
        ],
        name="ix_customer_order_date",
    )

    # =========================================================
    # 4. Quarantine collection index
    # =========================================================
    result["quarantine_run_errors"] = db[
        settings.quarantine_collection
    ].create_index(
        [
            ("run_id", ASCENDING),
            ("error_codes", ASCENDING),
        ],
        name="ix_quarantine_run_errors",
    )

    # =========================================================
    # 5. Event id index
    #
    # Used by incremental Materialized View processing
    # to prevent processing the same event twice.
    # =========================================================
    result["events"] = db[
        settings.events
    ].create_index(
        [("event_id", ASCENDING)],
        unique=True,
        name="ux_event_id",
    )

    # =========================================================
    # 6. Materialized View state index
    #
    # MongoDB already creates a unique _id index automatically.
    # This explicit call is kept idempotent and documents the
    # requirement clearly.
    # =========================================================
    # _id is already uniquely indexed by MongoDB automatically
    result["state"] = "_id_"

    return result