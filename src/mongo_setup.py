"""MongoDB connection, indexes, schema contract, and idempotent writes."""

from __future__ import annotations

from typing import Any, Iterable


class MongoStore:
    def __init__(
        self,
        mongo_uri: str = "mongodb://127.0.0.1:27017",
        database: str = "ecommerce_store",
        raw_collection: str = "orders_raw",
        validated_collection: str = "orders_validated",
        quarantine_collection: str = "orders_quarantine",
    ) -> None:
        try:
            from pymongo import MongoClient
        except ImportError as exc:
            raise RuntimeError("pymongo is required for MongoDB execution") from exc
        self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
        self.client.admin.command("ping")
        self.db = self.client[database]
        self.raw = self.db[raw_collection]
        self.validated = self.db[validated_collection]
        self.quarantine = self.db[quarantine_collection]
        self.ensure_indexes()
        self.ensure_schema_validator()

    def ensure_indexes(self) -> None:
        self.raw.create_index([("run_id", 1), ("source_row_number", 1)])
        self.validated.create_index("order_id", unique=True)
        self.quarantine.create_index([("run_id", 1), ("source_row_number", 1)], unique=True)

    def ensure_schema_validator(self) -> None:
        # Schema branch 1: raw-valid documents before cleaning.
        # It validates the envelope and BSON structure, but intentionally allows
        # non-canonical business values because Cleaning Last has not run yet.
        raw_schema = {
            "bsonType": "object",
            "required": [
                "order_id", "order_date", "status", "customer", "items",
                "payment", "total_amount", "quality_status",
                "raw_validation_only", "cleaning_applied",
            ],
            "properties": {
                "order_id": {"bsonType": "string", "minLength": 1},
                "order_date": {"bsonType": ["string", "null"]},
                "status": {"bsonType": ["string", "null"]},
                "customer": {
                    "bsonType": "object",
                    "required": ["customer_id", "phone", "email", "address"],
                    "properties": {
                        "customer_id": {"bsonType": ["string", "null"]},
                        "name": {"bsonType": ["string", "null"]},
                        "phone": {"bsonType": ["string", "null"]},
                        "email": {"bsonType": ["string", "null"]},
                        "address": {
                            "bsonType": "object",
                            "required": ["city", "district"],
                            "properties": {
                                "city": {"bsonType": ["string", "null"]},
                                "district": {"bsonType": ["string", "null"]},
                            },
                        },
                    },
                },
                "items": {"bsonType": ["string", "array", "object", "null"]},
                "payment": {
                    "bsonType": "object",
                    "required": ["method", "status", "amount", "currency"],
                    "properties": {
                        "method": {"bsonType": ["string", "null"]},
                        "status": {"bsonType": ["string", "null"]},
                        "amount": {"bsonType": ["string", "double", "int", "long", "decimal", "null"]},
                        "currency": {"bsonType": ["string", "null"]},
                    },
                },
                "delivery": {"bsonType": ["object", "null"]},
                "total_amount": {"bsonType": ["string", "double", "int", "long", "decimal", "null"]},
                "quality_status": {"enum": ["raw_validated"]},
                "raw_validation_only": {"enum": [True]},
                "cleaning_applied": {"enum": [False]},
            },
        }

        # Schema branch 2: final documents after Cleaning Last.
        final_schema = {
            "bsonType": "object",
            "required": ["order_id", "order_date", "status", "customer", "items", "payment", "total_amount", "quality_status"],
            "properties": {
                "order_id": {"bsonType": "string", "minLength": 1},
                "order_date": {"bsonType": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:[0-9]{2}:[0-9]{2}([.][0-9]+)?)?$"},
                "status": {"enum": ["قيد الانتظار", "مؤكد", "قيد الشحن", "تم التسليم", "مرتجع", "ملغي"]},
                "customer": {"bsonType": "object", "required": ["customer_id", "phone", "email", "address"], "properties": {
                    "customer_id": {"bsonType": "string", "minLength": 1},
                    "phone": {"bsonType": "string", "pattern": "^(?:967)?(70|71|73|77)[0-9]{7}$"},
                    "email": {"bsonType": "string", "pattern": "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"},
                    "address": {"bsonType": "object", "required": ["city", "district"]},
                }},
                "items": {"bsonType": "array", "minItems": 1},
                "payment": {"bsonType": "object", "required": ["method", "status", "amount", "currency"], "properties": {
                    "currency": {"enum": ["YER"]}, "amount": {"bsonType": ["double", "int", "long", "decimal"], "minimum": 0},
                }},
                "total_amount": {"bsonType": ["double", "int", "long", "decimal"], "minimum": 0},
                "quality_status": {"enum": ["validated", "corrected"]},
            },
        }

        # MongoDB chooses exactly one branch by quality_status and the raw flags.
        validator = {"$jsonSchema": {"bsonType": "object", "oneOf": [raw_schema, final_schema]}}
        if self.validated.name not in self.db.list_collection_names():
            self.db.create_collection(self.validated.name, validator=validator, validationLevel="strict", validationAction="error")
        else:
            self.db.command("collMod", self.validated.name, validator=validator, validationLevel="strict", validationAction="error")

    def view_quarantine(self, limit: int = 20, run_id: str | None = None) -> list[dict[str, Any]]:
        query = {"run_id": run_id} if run_id else {}
        return list(self.quarantine.find(query, {"_id": 0}).sort("source_row_number", 1).limit(max(limit, 1)))

    def insert_raw(self, documents: Iterable[dict[str, Any]], batch_size: int = 500) -> int:
        from pymongo import InsertOne
        operations = []
        count = 0
        for document in documents:
            operations.append(InsertOne(document))
            count += 1
            if len(operations) >= batch_size:
                self.raw.bulk_write(operations, ordered=False)
                operations = []
        if operations:
            self.raw.bulk_write(operations, ordered=False)
        return count

    def upsert_validated(self, document: dict[str, Any]) -> str:
        from pymongo import UpdateOne
        self.quarantine.delete_one({"run_id": document.get("run_id"), "source_row_number": document.get("source_row_number")})
        previous = self.validated.find_one({"order_id": document.get("order_id")}, {"_id": 0})
        if previous is None:
            outcome = "inserted"
        elif {k: v for k, v in previous.items() if k != "processed_at"} == {k: v for k, v in document.items() if k != "processed_at"}:
            return "unchanged"
        else:
            outcome = "updated"
        self.validated.bulk_write([UpdateOne({"order_id": document.get("order_id")}, {"$set": document}, upsert=True)], ordered=False)
        return outcome

    def upsert_quarantine(self, document: dict[str, Any]) -> str:
        from pymongo import UpdateOne
        if document.get("order_id"):
            self.validated.delete_many({"order_id": document.get("order_id")})
        key = {"run_id": document.get("run_id"), "source_row_number": document.get("source_row_number")}
        previous = self.quarantine.find_one(key, {"_id": 0})
        outcome = "inserted" if previous is None else "updated"
        if previous is not None and {k: v for k, v in previous.items() if k != "processed_at"} == {k: v for k, v in document.items() if k != "processed_at"}:
            return "unchanged"
        self.quarantine.bulk_write([UpdateOne(key, {"$set": document}, upsert=True)], ordered=False)
        return outcome

    def remove_quarantine(self, document: dict[str, Any]) -> None:
        self.quarantine.delete_one({"run_id": document.get("run_id"), "source_row_number": document.get("source_row_number")})

    def close(self) -> None:
        self.client.close()


def view_quarantine(mongo_uri: str = "mongodb://127.0.0.1:27017", database: str = "ecommerce_store", limit: int = 20, run_id: str | None = None) -> list[dict[str, Any]]:
    store = MongoStore(mongo_uri, database)
    try:
        return store.view_quarantine(limit=limit, run_id=run_id)
    finally:
        store.close()


def setup_mongo(
    mongo_uri: str = "mongodb://127.0.0.1:27017",
    database: str = "ecommerce_store",
) -> dict[str, Any]:
    store = MongoStore(mongo_uri, database)
    try:
        return {"database": database, "indexes_ready": True, "validated_key": "order_id", "quarantine_key": "run_id+source_row_number"}
    finally:
        store.close()


__all__ = ["MongoStore", "setup_mongo", "view_quarantine"]
