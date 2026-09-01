




"""Single executable entry point for the exact-only project structure."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_loader import load_orders_batch
from elt_pipeline import JsonStore, clean_after_raw_batch
from file_router import discover_file, write_discovery_report
from metrics import write_results
from mongo_setup import MongoStore, view_quarantine
from quality_rules import FIELD_ALIASES, classify_raw_document, classify_raw_without_cleaning
from spark_loader import load_orders_raw_spark


def recommended_partitions(file_size_mb: float | None = None, requested: int = 0) -> int:
    if requested > 0:
        return requested
    cpu = max(os.cpu_count() or 2, 2)
    if file_size_mb is not None and file_size_mb >= 10240:
        return min(max(cpu * 8, 64), 512)
    if file_size_mb is not None and file_size_mb >= 1024:
        return min(max(cpu * 4, 32), 256)
    return min(max(cpu * 2, 8), 128)


def _canonicalize_spark_columns(frame: Any, functions: Any) -> Any:
    normalized = {re.sub(r"[^a-z0-9]", "", column.lower()): column for column in frame.columns}
    for canonical, aliases in FIELD_ALIASES.items():
        if canonical in frame.columns:
            continue
        source = next((normalized.get(re.sub(r"[^a-z0-9]", "", alias.lower())) for alias in aliases if normalized.get(re.sub(r"[^a-z0-9]", "", alias.lower()))), None)
        if source:
            frame = frame.withColumn(canonical, functions.col(source))
        else:
            frame = frame.withColumn(canonical, functions.lit(None).cast("string"))
    return frame


def _bulk_upsert(collection: Any, documents: list[dict[str, Any]], key: str) -> Counter:
    from pymongo import UpdateOne
    if not documents:
        return Counter()
    operations = [UpdateOne({key: doc.get(key)}, {"$set": doc}, upsert=True) for doc in documents]
    result = collection.bulk_write(operations, ordered=False)
    inserted = int(result.upserted_count)
    updated = int(result.modified_count)
    unchanged = max(int(result.matched_count) - updated, 0)
    return Counter(inserted_count=inserted, updated_count=updated, unchanged_count=unchanged)


def _bulk_upsert_quarantine(collection: Any, documents: list[dict[str, Any]]) -> Counter:
    from pymongo import UpdateOne
    if not documents:
        return Counter()
    operations = [
        UpdateOne(
            {"run_id": doc.get("run_id"), "source_row_number": doc.get("source_row_number")},
            {"$set": doc},
            upsert=True,
        )
        for doc in documents
    ]
    result = collection.bulk_write(operations, ordered=False)
    return Counter(inserted_count=int(result.upserted_count), updated_count=int(result.modified_count), unchanged_count=max(int(result.matched_count) - int(result.modified_count), 0))


def _write_raw_validated_partition(rows: Iterable[Any], config: dict[str, Any]) -> None:
    """Write rows that pass raw validation without cleaning or correction."""
    from pymongo import MongoClient
    from pyspark import TaskContext
    client = MongoClient(config["mongo_uri"], serverSelectionTimeoutMS=10000)
    db = client[config["database"]]
    validated = db[config["validated_collection"]]
    valid_buffer: list[dict[str, Any]] = []
    counts: Counter = Counter()
    partition_id = TaskContext.get().partitionId() if TaskContext.get() else 0
    try:
        for row in rows:
            raw = row.asDict(recursive=True)
            result = classify_raw_without_cleaning(raw, bool(raw.get("_is_duplicate")))
            counts["raw_loaded"] += 1
            if not result["raw_valid"]:
                continue
            counts["raw_valid_count"] += 1
            valid_buffer.append(result["validated_document"])
            if len(valid_buffer) >= config["batch_size"]:
                counts.update(_bulk_upsert(validated, valid_buffer, "order_id"))
                valid_buffer = []
        counts.update(_bulk_upsert(validated, valid_buffer, "order_id"))
        db[config["metrics_collection"]].replace_one(
            {"_id": f"{config['run_id']}:raw_validated:{partition_id}"},
            {"_id": f"{config['run_id']}:raw_validated:{partition_id}", "run_id": config["run_id"], "stage": "raw_classification_without_cleaning", "partition_id": partition_id, **dict(counts)},
            upsert=True,
        )
    finally:
        client.close()


def _write_raw_invalid_partition(rows: Iterable[Any], config: dict[str, Any]) -> None:
    """Write raw-invalid rows to Quarantine without cleaning or correction."""
    from pymongo import MongoClient
    from pyspark import TaskContext
    client = MongoClient(config["mongo_uri"], serverSelectionTimeoutMS=10000)
    db = client[config["database"]]
    quarantine = db[config["quarantine_collection"]]
    invalid_buffer: list[dict[str, Any]] = []
    counts: Counter = Counter()
    errors: Counter = Counter()
    partition_id = TaskContext.get().partitionId() if TaskContext.get() else 0
    try:
        for row in rows:
            raw = row.asDict(recursive=True)
            result = classify_raw_without_cleaning(raw, bool(raw.get("_is_duplicate")))
            counts["raw_loaded"] += 1
            if not result["raw_invalid"]:
                continue
            counts["raw_invalid_count"] += 1
            invalid = result["quarantine_document"]
            invalid_buffer.append(invalid)
            for code in invalid.get("error_codes", []):
                errors[code] += 1
            if len(invalid_buffer) >= config["batch_size"]:
                counts.update(_bulk_upsert_quarantine(quarantine, invalid_buffer))
                invalid_buffer = []
        counts.update(_bulk_upsert_quarantine(quarantine, invalid_buffer))
        db[config["metrics_collection"]].replace_one(
            {"_id": f"{config['run_id']}:raw_invalid:{partition_id}"},
            {"_id": f"{config['run_id']}:raw_invalid:{partition_id}", "run_id": config["run_id"], "stage": "raw_classification_without_cleaning", "partition_id": partition_id, **dict(counts), "error_case_counts": dict(errors)},
            upsert=True,
        )
    finally:
        client.close()


def _write_validated_partition(rows: Iterable[Any], config: dict[str, Any]) -> None:
    from pymongo import MongoClient
    from pyspark import TaskContext
    client = MongoClient(config["mongo_uri"], serverSelectionTimeoutMS=10000)
    db = client[config["database"]]
    validated = db[config["validated_collection"]]
    quarantine = db[config["quarantine_collection"]]
    valid_buffer: list[dict[str, Any]] = []
    quarantine_buffer: list[dict[str, Any]] = []
    counts: Counter = Counter()
    errors: Counter = Counter()
    partition_id = TaskContext.get().partitionId() if TaskContext.get() else 0
    try:
        for row in rows:
            raw = row.asDict(recursive=True)
            result = classify_raw_document(raw, bool(raw.get("_is_duplicate")))
            if not result.get("structure_passed"):
                continue
            counts["initial_valid_count"] += 1
            final = result["final_document"]
            if final.get("quality_status") in {"validated", "corrected"}:
                if final.get("quality_status") == "validated":
                    counts["valid_count"] += 1
                else:
                    counts["corrected_count"] += 1
                quarantine.delete_one({"run_id": final.get("run_id"), "source_row_number": final.get("source_row_number")})
                valid_buffer.append(final)
            else:
                counts["quarantine_count"] += 1
                if final.get("order_id"):
                    validated.delete_many({"order_id": final.get("order_id")})
                quarantine_buffer.append(final)
                for code in final.get("error_codes", []):
                    errors[code] += 1
            if len(valid_buffer) + len(quarantine_buffer) >= config["batch_size"]:
                counts.update(_bulk_upsert(validated, valid_buffer))
                counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
                valid_buffer, quarantine_buffer = [], []
        counts.update(_bulk_upsert(validated, valid_buffer))
        counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
        db[config["metrics_collection"]].replace_one(
            {"_id": f"{config['run_id']}:validated:{partition_id}"},
            {"_id": f"{config['run_id']}:validated:{partition_id}", "run_id": config["run_id"], "stage": "schema_duplicate_then_clean", "partition_id": partition_id, **dict(counts), "error_case_counts": dict(errors)},
            upsert=True,
        )
    finally:
        client.close()


def _write_invalid_partition(rows: Iterable[Any], config: dict[str, Any]) -> None:
    from pymongo import MongoClient
    from pyspark import TaskContext
    client = MongoClient(config["mongo_uri"], serverSelectionTimeoutMS=10000)
    db = client[config["database"]]
    validated = db[config["validated_collection"]]
    quarantine = db[config["quarantine_collection"]]
    valid_buffer: list[dict[str, Any]] = []
    quarantine_buffer: list[dict[str, Any]] = []
    counts: Counter = Counter()
    errors: Counter = Counter()
    partition_id = TaskContext.get().partitionId() if TaskContext.get() else 0
    try:
        for row in rows:
            raw = row.asDict(recursive=True)
            result = classify_raw_document(raw, bool(raw.get("_is_duplicate")))
            if result["initial_classification"] != "invalid":
                continue
            counts["initial_invalid_count"] += 1
            initial = result["initial_quarantine"]
            final = result["final_document"]
            final["initial_classification"] = "invalid"
            final["initial_error_codes"] = initial.get("error_codes", [])
            final["initial_error_details"] = initial.get("error_details", [])
            if final.get("quality_status") == "corrected":
                counts["corrected_count"] += 1
                quarantine.delete_one({"run_id": final.get("run_id"), "source_row_number": final.get("source_row_number")})
                valid_buffer.append(final)
            else:
                counts["quarantine_count"] += 1
                if final.get("order_id"):
                    validated.delete_many({"order_id": final.get("order_id")})
                quarantine_buffer.append(final)
                for code in final.get("error_codes", []):
                    errors[code] += 1
            if len(valid_buffer) + len(quarantine_buffer) >= config["batch_size"]:
                counts.update(_bulk_upsert(validated, valid_buffer))
                counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
                valid_buffer, quarantine_buffer = [], []
        counts.update(_bulk_upsert(validated, valid_buffer))
        counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
        db[config["metrics_collection"]].replace_one(
            {"_id": f"{config['run_id']}:invalid:{partition_id}"},
            {"_id": f"{config['run_id']}:invalid:{partition_id}", "run_id": config["run_id"], "stage": "invalid_after_validated", "partition_id": partition_id, **dict(counts), "error_case_counts": dict(errors)},
            upsert=True,
        )
    finally:
        client.close()


def _write_quarantine_cleaning_partition(rows: Iterable[Any], config: dict[str, Any]) -> None:
    """Clean only documents already stored in orders_quarantine."""
    from copy import deepcopy
    from pymongo import MongoClient
    from pyspark import TaskContext

    client = MongoClient(config["mongo_uri"], serverSelectionTimeoutMS=10000)
    db = client[config["database"]]
    validated = db[config["validated_collection"]]
    quarantine = db[config["quarantine_collection"]]
    valid_buffer: list[dict[str, Any]] = []
    quarantine_buffer: list[dict[str, Any]] = []
    counts: Counter = Counter()
    errors: Counter = Counter()
    partition_id = TaskContext.get().partitionId() if TaskContext.get() else 0
    try:
        for row in rows:
            quarantined = row.asDict(recursive=True)
            original = deepcopy(quarantined.get("original_document") or {})
            for field in ("run_id", "source_file", "source_row_number", "engine_used", "raw_payload"):
                if field not in original and quarantined.get(field) is not None:
                    original[field] = quarantined.get(field)
            is_duplicate = "DUPLICATE_ORDER_ID" in set(quarantined.get("error_codes") or [])
            item = classify_raw_document(original, is_duplicate=is_duplicate)
            final = item["final_document"]
            final["initial_classification"] = "invalid"
            final["initial_error_codes"] = list(quarantined.get("error_codes") or [])
            final["initial_error_details"] = deepcopy(quarantined.get("error_details") or [])
            final["raw_error_codes"] = list(quarantined.get("error_codes") or [])
            final["raw_error_details"] = deepcopy(quarantined.get("error_details") or [])
            final["cleaning_applied"] = True
            final["raw_validation_only"] = False
            final["validation_stages"] = ["raw_schema_validation", "raw_business_validation", "raw_duplicate_detection", "cleaning_last"]
            counts["cleaned_quarantine_count"] += 1
            if final.get("quality_status") in {"validated", "corrected"}:
                if final.get("quality_status") == "validated":
                    counts["valid_count"] += 1
                else:
                    counts["corrected_count"] += 1
                quarantine.delete_one({"run_id": final.get("run_id"), "source_row_number": final.get("source_row_number")})
                valid_buffer.append(final)
            else:
                counts["quarantine_count"] += 1
                for code in final.get("error_codes", []):
                    errors[code] += 1
                quarantine_buffer.append(final)
            if len(valid_buffer) + len(quarantine_buffer) >= config["batch_size"]:
                counts.update(_bulk_upsert(validated, valid_buffer, "order_id"))
                counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
                valid_buffer, quarantine_buffer = [], []
        counts.update(_bulk_upsert(validated, valid_buffer, "order_id"))
        counts.update(_bulk_upsert_quarantine(quarantine, quarantine_buffer))
        db[config["metrics_collection"]].replace_one(
            {"_id": f"{config['run_id']}:quarantine_cleaning:{partition_id}"},
            {"_id": f"{config['run_id']}:quarantine_cleaning:{partition_id}", "run_id": config["run_id"], "stage": "cleaning_quarantine_only", "partition_id": partition_id, **dict(counts), "error_case_counts": dict(errors)},
            upsert=True,
        )
    finally:
        client.close()



def _run_quality_pyspark_dataframe(
    spark: Any,
    *,
    run_id: str,
    mongo_uri: str,
    database: str,
    effective_partitions: int,
    batch_size: int,
    connector_jar: str | None,
    reports_dir: str | Path,
    raw_collection: str,
    validated_collection: str,
    quarantine_collection: str,
    limit: int,
    started: float,
) -> dict[str, Any]:
    """Run raw-only Quality classification with bounded MongoDB writes.

    The order is deliberately:
        1. Read unchanged raw documents from orders_raw.
        2. Detect duplicate order_id values.
        3. Apply schema/business validation without cleaning.
        4. Upsert valid rows into orders_validated.
        5. Upsert invalid rows into orders_quarantine with reasons.

    Cleaning is not called by this function. It must run later and read only
    orders_quarantine.
    """
    from pyspark.sql import functions as F
    from pymongo import MongoClient

    # Duplicate detection is performed once in MongoDB. Only duplicate keys,
    # not raw documents, are collected and broadcast to Spark workers.
    probe = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
    
    # try:
    #     duplicate_rows = probe[database][raw_collection].aggregate(
    #         [
    #             {"$match": {"run_id": run_id}},
    #             {
    #                 "$group": {
    #                     "_id": "$order_id",
    #                     "n": {"$sum": 1},
    #                 }
    #             },
    #             {
    #                 "$match": {
    #                     "_id": {"$nin": [None, ""]},
    #                     "n": {"$gt": 1},
    #                 }
    #             },
    #             {"$project": {"_id": 1}},
    #         ],
    #         allowDiskUse=True,
    #     )
    #     duplicate_ids = {str(item["_id"]) for item in duplicate_rows}
    # finally:
    #     probe.close()


    try:
        duplicate_pipeline = [
            {"$match": {"run_id": run_id}},
        ]

        # في العينة نفحص التكرارات داخل أول limit سجل فقط.
        # في التشغيل الكامل limit=0، لذلك نفحص جميع السجلات.
        if limit:
            duplicate_pipeline.append({"$limit": int(limit)})

        duplicate_pipeline.extend(
            [
                {
                    "$group": {
                        "_id": "$order_id",
                        "n": {"$sum": 1},
                    }
                },
                {
                    "$match": {
                        "_id": {"$nin": [None, ""]},
                        "n": {"$gt": 1},
                    }
                },
                {"$project": {"_id": 1}},
            ]
        )

        duplicate_rows = probe[database][raw_collection].aggregate(
            duplicate_pipeline,
            allowDiskUse=True,
        )
        duplicate_ids = {
            str(item["_id"])
            for item in duplicate_rows
        }
    finally:
        probe.close()


    print("duplicate order_id keys:", len(duplicate_ids))

    # IMPORTANT: put $limit inside MongoDB's aggregation pipeline. The second
    # DataFrame-side limit below remains as a safety guard.
    quality_pipeline = [
        {"$match": {"run_id": run_id}},
    ]
    if limit:
        quality_pipeline.append({"$limit": int(limit)})




    reader = (
        spark.read
        .format("mongodb")
        .option("connection.uri", mongo_uri)
        .option("database", database)
        .option("collection", raw_collection)
        .option(
            "aggregation.pipeline",
            json.dumps(quality_pipeline),
        )
    )

    # A bounded smoke test must use one connector partition so the limit is
    # global rather than independently applied by several partitions.
    if limit:
        reader = reader.option(
            "partitioner",
            "com.mongodb.spark.sql.connector.read.partitioner.SinglePartitionPartitioner",
        )

    raw = reader.load().drop("_id")
    raw = _canonicalize_spark_columns(raw, F)

    # Ensure metadata exists even if an older raw document lacks a field.
    if "run_id" not in raw.columns:
        raw = raw.withColumn("run_id", F.lit(run_id))
    if "source_file" not in raw.columns:
        raw = raw.withColumn("source_file", F.lit(""))
    if "source_row_number" not in raw.columns:
        raw = raw.withColumn("source_row_number", F.monotonically_increasing_id())
    if "engine_used" not in raw.columns:
        raw = raw.withColumn("engine_used", F.lit("pyspark"))
    if "raw_payload" not in raw.columns:
        raw = raw.withColumn(
            "raw_payload",
            F.to_json(F.struct(*[F.col(column) for column in raw.columns])),
        )

    # Safety guard: never process more than the requested sample size.
    if limit:
        raw = raw.limit(int(limit))

    # Do not write the internal duplicate helper to MongoDB. Duplicate status
    # is calculated inside each worker from the broadcast key set.
    source_columns = [
        column for column in raw.columns
        if column != "_is_duplicate"
    ]
    raw = raw.select(*[F.col(column) for column in source_columns])

    duplicate_broadcast = spark.sparkContext.broadcast(duplicate_ids)
    config = {
        "mongo_uri": mongo_uri,
        "database": database,
        "validated_collection": validated_collection,
        "quarantine_collection": quarantine_collection,
        "metrics_collection": "quality_partition_metrics",
        "run_id": run_id,
        "batch_size": max(int(batch_size), 1),
        "duplicate_ids": duplicate_broadcast,
    }

    def classify_and_write_partition(rows: Iterable[Any]) -> Iterable[dict[str, Any]]:
        """Classify one Spark partition and write bounded MongoDB upserts."""
        from pymongo import MongoClient, UpdateOne
        from pyspark import TaskContext
        from quality_rules import classify_raw_without_cleaning

        client = MongoClient(
            config["mongo_uri"],
            serverSelectionTimeoutMS=10000,
        )
        db = client[config["database"]]
        validated = db[config["validated_collection"]]
        quarantine = db[config["quarantine_collection"]]
        duplicate_ids_local = config["duplicate_ids"].value
        batch_limit = config["batch_size"]

        valid_ops: list[Any] = []
        quarantine_ops: list[Any] = []
        counts: Counter = Counter()
        errors: Counter = Counter()
        task_context = TaskContext.get()
        partition_id = task_context.partitionId() if task_context else 0

        def flush() -> None:
            if valid_ops:
                result = validated.bulk_write(
                    valid_ops,
                    ordered=False,
                )
                counts["inserted_count"] += int(result.upserted_count)
                counts["updated_count"] += int(result.modified_count)
                counts["unchanged_count"] += max(
                    int(result.matched_count)
                    - int(result.modified_count),
                    0,
                )
                valid_ops.clear()

            if quarantine_ops:
                result = quarantine.bulk_write(
                    quarantine_ops,
                    ordered=False,
                )
                counts["inserted_count"] += int(result.upserted_count)
                counts["updated_count"] += int(result.modified_count)
                counts["unchanged_count"] += max(
                    int(result.matched_count)
                    - int(result.modified_count),
                    0,
                )
                quarantine_ops.clear()

        try:
            for row in rows:
                raw_document = row.asDict(recursive=True)
                counts["raw_loaded"] += 1

                order_id = raw_document.get("order_id")
                is_duplicate = bool(
                    order_id is not None
                    and str(order_id) in duplicate_ids_local
                )

                classified = classify_raw_without_cleaning(
                    raw_document,
                    is_duplicate=is_duplicate,
                )

                if classified.get("raw_valid"):
                    counts["raw_valid_count"] += 1
                    document = classified["validated_document"]
                    valid_ops.append(
                        UpdateOne(
                            {"order_id": document.get("order_id")},
                            {"$set": document},
                            upsert=True,
                        )
                    )
                else:
                    counts["raw_invalid_count"] += 1
                    document = classified["quarantine_document"]
                    quarantine_ops.append(
                        UpdateOne(
                            {
                                "run_id": document.get("run_id"),
                                "source_row_number": document.get(
                                    "source_row_number"
                                ),
                            },
                            {"$set": document},
                            upsert=True,
                        )
                    )
                    for code in document.get("error_codes", []):
                        errors[str(code)] += 1

                if len(valid_ops) + len(quarantine_ops) >= batch_limit:
                    flush()

            flush()
            yield {
                "partition_id": partition_id,
                **dict(counts),
                "error_case_counts": dict(errors),
            }
        finally:
            client.close()

    try:
        summaries = raw.rdd.mapPartitions(
            classify_and_write_partition
        ).collect()
    finally:
        duplicate_broadcast.destroy()

    totals: Counter = Counter()
    error_case_counts: Counter = Counter()

    for summary in summaries:
        for key, value in summary.items():
            if key == "error_case_counts":
                error_case_counts.update(value or {})
            elif key != "partition_id":
                totals[key] += int(value or 0)

    raw_loaded = int(totals.get("raw_loaded", 0))
    raw_valid_count = int(totals.get("raw_valid_count", 0))
    raw_invalid_count = int(totals.get("raw_invalid_count", 0))

    if limit and raw_loaded > int(limit):
        raise RuntimeError(
            f"LIMIT protection failed: returned={raw_loaded}, limit={limit}"
        )

    if raw_loaded != raw_valid_count + raw_invalid_count:
        raise RuntimeError(
            "Raw Classification reconciliation failed: "
            f"{raw_loaded} != {raw_valid_count} + {raw_invalid_count}"
        )

    elapsed = round(time.perf_counter() - started, 6)
    result: dict[str, Any] = {
        "step": "data_quality",
        "mode": (
            "bounded_pyspark_direct_partition_upsert"
            if limit
            else "full_pyspark_direct_partition_upsert"
        ),
        "run_id": run_id,
        "classification_order": "raw_validated_before_raw_quarantine",
        "cleaning_applied": False,
        "partitions": effective_partitions,
        "requested_partitions": effective_partitions,
        "batch_size": batch_size,
        "raw_loaded": raw_loaded,
        "raw_valid_count": raw_valid_count,
        "raw_invalid_count": raw_invalid_count,
        "initial_valid_count": raw_valid_count,
        "initial_invalid_count": raw_invalid_count,
        "valid_count": raw_valid_count,
        "corrected_count": 0,
        "quarantine_count": raw_invalid_count,
        "inserted_count": int(totals.get("inserted_count", 0)),
        "updated_count": int(totals.get("updated_count", 0)),
        "unchanged_count": int(totals.get("unchanged_count", 0)),
        "error_case_counts": dict(error_case_counts),
        "elapsed_seconds": elapsed,
        "throughput_rows_per_second": round(
            raw_loaded / max(elapsed, 0.000001),
            2,
        ),
        "reconciliation_ok": True,
        "next_stage": "cleaning_after_raw_classification",
        "write_mode": "spark_partition_bounded_mongodb_upsert",
    }

    metric_store = MongoStore(mongo_uri, database)
    try:
        metric_store.db["quality_partition_metrics"].replace_one(
            {"_id": f"{run_id}:raw_classification_without_cleaning"},
            {
                "_id": f"{run_id}:raw_classification_without_cleaning",
                "run_id": run_id,
                "stage": "raw_classification_without_cleaning",
                **result,
            },
            upsert=True,
        )
    finally:
        metric_store.close()

    write_results(result, reports_dir)
    return result


    def classify_and_write_partition(rows: Iterable[Any]) -> Iterable[dict[str, Any]]:
        """Classify and write one Spark partition; return only a tiny summary."""
        from pymongo import MongoClient, UpdateOne
        from pyspark import TaskContext
        from quality_rules import classify_raw_without_cleaning

        client = MongoClient(config["mongo_uri"], serverSelectionTimeoutMS=10000)
        db = client[config["database"]]
        validated = db[config["validated_collection"]]
        quarantine = db[config["quarantine_collection"]]
        duplicate_ids_local = config["duplicate_ids"].value
        batch_limit = config["batch_size"]

        valid_ops: list[Any] = []
        quarantine_ops: list[Any] = []
        counts: Counter = Counter()
        errors: Counter = Counter()
        partition_id = (
            TaskContext.get().partitionId()
            if TaskContext.get() is not None
            else 0
        )

        def flush() -> None:
            if valid_ops:
                result = validated.bulk_write(valid_ops, ordered=False)
                counts["inserted_count"] += int(result.upserted_count)
                counts["updated_count"] += int(result.modified_count)
                counts["unchanged_count"] += max(
                    int(result.matched_count) - int(result.modified_count),
                    0,
                )
                valid_ops.clear()

            if quarantine_ops:
                result = quarantine.bulk_write(quarantine_ops, ordered=False)
                counts["inserted_count"] += int(result.upserted_count)
                counts["updated_count"] += int(result.modified_count)
                counts["unchanged_count"] += max(
                    int(result.matched_count) - int(result.modified_count),
                    0,
                )
                quarantine_ops.clear()

        try:
            for row in rows:
                raw_document = row.asDict(recursive=True)
                counts["raw_loaded"] += 1
                order_id = raw_document.get("order_id")
                is_duplicate = bool(
                    order_id is not None
                    and str(order_id) in duplicate_ids_local
                )
                classified = classify_raw_without_cleaning(
                    raw_document,
                    is_duplicate=is_duplicate,
                )

                if classified.get("raw_valid"):
                    counts["raw_valid_count"] += 1
                    document = classified["validated_document"]
                    valid_ops.append(
                        UpdateOne(
                            {"order_id": document.get("order_id")},
                            {"$set": document},
                            upsert=True,
                        )
                    )
                else:
                    counts["raw_invalid_count"] += 1
                    document = classified["quarantine_document"]
                    quarantine_ops.append(
                        UpdateOne(
                            {
                                "run_id": document.get("run_id"),
                                "source_row_number": document.get(
                                    "source_row_number"
                                ),
                            },
                            {"$set": document},
                            upsert=True,
                        )
                    )
                    for code in document.get("error_codes", []):
                        errors[str(code)] += 1

                if len(valid_ops) + len(quarantine_ops) >= batch_limit:
                    flush()

            flush()
            summary = {
                "partition_id": partition_id,
                **dict(counts),
                "error_case_counts": dict(errors),
            }
            yield summary
        finally:
            client.close()

    try:
        summaries = raw.rdd.mapPartitions(
            classify_and_write_partition
        ).collect()
    finally:
        duplicate_broadcast.destroy()

    totals: Counter = Counter()
    error_case_counts: Counter = Counter()
    for summary in summaries:
        for key, value in summary.items():
            if key == "error_case_counts":
                error_case_counts.update(value or {})
            elif key != "partition_id":
                totals[key] += int(value or 0)

    raw_loaded = int(totals.get("raw_loaded", 0))
    raw_valid_count = int(totals.get("raw_valid_count", 0))
    raw_invalid_count = int(totals.get("raw_invalid_count", 0))

    if limit and raw_loaded > int(limit):
        raise RuntimeError(
            f"LIMIT protection failed: returned={raw_loaded}, limit={limit}"
        )
    if raw_loaded != raw_valid_count + raw_invalid_count:
        raise RuntimeError(
            "Raw Classification reconciliation failed: "
            f"{raw_loaded} != {raw_valid_count} + {raw_invalid_count}"
        )

    elapsed = round(time.perf_counter() - started, 6)
    result: dict[str, Any] = {
        "step": "data_quality",
        "mode": (
            "bounded_pyspark_direct_partition_upsert"
            if limit
            else "full_pyspark_direct_partition_upsert"
        ),
        "run_id": run_id,
        "classification_order": "raw_validated_before_raw_quarantine",
        "cleaning_applied": False,
        "partitions": effective_partitions,
        "requested_partitions": effective_partitions,
        "batch_size": batch_size,
        "raw_loaded": raw_loaded,
        "raw_valid_count": raw_valid_count,
        "raw_invalid_count": raw_invalid_count,
        "initial_valid_count": raw_valid_count,
        "initial_invalid_count": raw_invalid_count,
        "valid_count": raw_valid_count,
        "corrected_count": 0,
        "quarantine_count": raw_invalid_count,
        "inserted_count": int(totals.get("inserted_count", 0)),
        "updated_count": int(totals.get("updated_count", 0)),
        "unchanged_count": int(totals.get("unchanged_count", 0)),
        "error_case_counts": dict(error_case_counts),
        "elapsed_seconds": elapsed,
        "throughput_rows_per_second": round(
            raw_loaded / max(elapsed, 0.000001),
            2,
        ),
        "reconciliation_ok": True,
        "next_stage": "cleaning_after_raw_classification",
        "write_mode": "spark_partition_bounded_mongodb_upsert",
    }

    metric_store = MongoStore(mongo_uri, database)
    try:
        metric_store.db["quality_partition_metrics"].replace_one(
            {"_id": f"{run_id}:raw_classification_without_cleaning"},
            {
                "_id": f"{run_id}:raw_classification_without_cleaning",
                "run_id": run_id,
                "stage": "raw_classification_without_cleaning",
                **result,
            },
            upsert=True,
        )
    finally:
        metric_store.close()

    write_results(result, reports_dir)
    return result

def run_quality_pyspark(
    run_id: str,
    *,
    mongo_uri: str,
    database: str,
    partitions: int,
    batch_size: int,
    master: str,
    connector_jar: str | None,
    reports_dir: str | Path,
    raw_collection: str = "orders_raw",
    validated_collection: str = "orders_validated",
    quarantine_collection: str = "orders_quarantine",
    limit: int = 0,
) -> dict[str, Any]:
    """Run Spark Quality without caching the full classified DataFrame."""
    try:
        from pyspark.sql import SparkSession
    except ImportError as exc:
        raise RuntimeError("PySpark is required for the full quality path") from exc

    effective_partitions = recommended_partitions(requested=partitions)

    # Resolve Hadoop from the environment or from the standard project layout.
    hadoop_candidates = []
    if os.getenv("HADOOP_HOME"):
        hadoop_candidates.append(Path(os.environ["HADOOP_HOME"]))
    hadoop_candidates.extend(
        [
            ROOT.parent / "hadoop",
            Path(r"C:\hadoop"),
        ]
    )
    hadoop_home = next(
        (path.resolve() for path in hadoop_candidates if (path / "bin" / "winutils.exe").is_file()),
        None,
    )
    if hadoop_home is None:
        raise FileNotFoundError(
            "winutils.exe غير موجود. تحقق من HADOOP_HOME أو مجلد hadoop بجانب المشروع."
        )

    spark_tmp = Path(
        os.getenv("SPARK_LOCAL_DIRS", r"E:\spark-tmp")
    ).resolve()
    spark_tmp.mkdir(parents=True, exist_ok=True)

    hadoop_home_java = str(hadoop_home).replace("\\", "/")
    os.environ["HADOOP_HOME"] = str(hadoop_home)
    os.environ["HADOOP_HOME_DIR"] = str(hadoop_home)
    os.environ["SPARK_LOCAL_DIRS"] = str(spark_tmp)
    os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
    os.environ["PYSPARK_PYTHON"] = os.environ.get("PYSPARK_PYTHON", sys.executable)
    os.environ["PYSPARK_DRIVER_PYTHON"] = os.environ.get("PYSPARK_DRIVER_PYTHON", sys.executable)

    java_home_option = f"-Dhadoop.home.dir={hadoop_home_java}"
    builder = (
        SparkSession.builder
        .appName("Midterm-Data-Quality-Direct-PySpark")
        .master(master)
        .config("spark.local.dir", str(spark_tmp))
        .config("spark.hadoop.hadoop.home.dir", hadoop_home_java)
        .config("spark.driver.extraJavaOptions", java_home_option)
        .config("spark.executor.extraJavaOptions", java_home_option)
        .config("spark.driver.memory", os.getenv("SPARK_DRIVER_MEMORY", "8g"))
        .config("spark.executor.memory", os.getenv("SPARK_EXECUTOR_MEMORY", "8g"))
        .config("spark.default.parallelism", str(effective_partitions))
        .config("spark.sql.shuffle.partitions", str(effective_partitions))
        .config("spark.python.worker.reuse", "true")
        .config("spark.pyspark.python", os.environ["PYSPARK_PYTHON"])
        .config("spark.pyspark.driver.python", os.environ["PYSPARK_DRIVER_PYTHON"])
        .config("spark.executorEnv.PYSPARK_PYTHON", os.environ["PYSPARK_PYTHON"])
        .config("spark.mongodb.read.connection.uri", mongo_uri)
    )
    if connector_jar:
        builder = builder.config(
            "spark.jars",
            str(Path(connector_jar).resolve()),
        )

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Ship project modules to Python workers.
    src_dir = Path(__file__).resolve().parent
    for py_file in src_dir.glob("*.py"):
        spark.sparkContext.addPyFile(str(py_file))

    started = time.perf_counter()
    try:
        return _run_quality_pyspark_dataframe(
            spark,
            run_id=run_id,
            mongo_uri=mongo_uri,
            database=database,
            effective_partitions=effective_partitions,
            batch_size=batch_size,
            connector_jar=connector_jar,
            reports_dir=reports_dir,
            raw_collection=raw_collection,
            validated_collection=validated_collection,
            quarantine_collection=quarantine_collection,
            limit=limit,
            started=started,
        )
    finally:
        spark.stop()



def run_cleaning_pyspark(
    run_id: str,
    *,
    mongo_uri: str,
    database: str,
    partitions: int,
    batch_size: int,
    master: str,
    connector_jar: str | None,
    reports_dir: str | Path,
    raw_collection: str = "orders_raw",
    validated_collection: str = "orders_validated",
    quarantine_collection: str = "orders_quarantine",
    limit: int = 0,
) -> dict[str, Any]:
    """Run Cleaning Last on orders_quarantine only, without persist/cache.

    Raw documents are not read here. orders_raw and already validated documents
    are never used as the cleaning input. Rows that become safe are upserted to
    orders_validated and removed from quarantine; unsafe rows remain in
    orders_quarantine with their audit fields.
    """
    try:
        from pyspark.sql import SparkSession
    except ImportError as exc:
        raise RuntimeError("PySpark is required for the cleaning stage") from exc

    effective_partitions = recommended_partitions(requested=partitions)

    hadoop_candidates: list[Path] = []
    if os.getenv("HADOOP_HOME"):
        hadoop_candidates.append(Path(os.environ["HADOOP_HOME"]))
    hadoop_candidates.extend(
        [
            ROOT.parent / "hadoop",
            Path(r"C:\hadoop"),
        ]
    )
    hadoop_home = next(
        (
            path.resolve()
            for path in hadoop_candidates
            if (path / "bin" / "winutils.exe").is_file()
        ),
        None,
    )
    if hadoop_home is None:
        raise FileNotFoundError(
            "winutils.exe غير موجود. تحقق من HADOOP_HOME أو مجلد hadoop."
        )

    spark_tmp = Path(
        os.getenv("SPARK_LOCAL_DIRS", r"E:\spark-tmp")
    ).resolve()
    spark_tmp.mkdir(parents=True, exist_ok=True)

    hadoop_home_java = str(hadoop_home).replace("\\", "/")
    os.environ["HADOOP_HOME"] = str(hadoop_home)
    os.environ["HADOOP_HOME_DIR"] = str(hadoop_home)
    os.environ["SPARK_LOCAL_DIRS"] = str(spark_tmp)
    os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
    os.environ["PYSPARK_PYTHON"] = os.environ.get(
        "PYSPARK_PYTHON",
        sys.executable,
    )
    os.environ["PYSPARK_DRIVER_PYTHON"] = os.environ.get(
        "PYSPARK_DRIVER_PYTHON",
        sys.executable,
    )

    java_home_option = f"-Dhadoop.home.dir={hadoop_home_java}"
    builder = (
        SparkSession.builder
        .appName("Midterm-Cleaning-After-Raw-Classification")
        .master(master)
        .config("spark.local.dir", str(spark_tmp))
        .config("spark.hadoop.hadoop.home.dir", hadoop_home_java)
        .config("spark.driver.extraJavaOptions", java_home_option)
        .config("spark.executor.extraJavaOptions", java_home_option)
        .config("spark.driver.memory", os.getenv("SPARK_DRIVER_MEMORY", "8g"))
        .config("spark.executor.memory", os.getenv("SPARK_EXECUTOR_MEMORY", "8g"))
        .config("spark.default.parallelism", str(effective_partitions))
        .config("spark.sql.shuffle.partitions", str(effective_partitions))
        .config("spark.python.worker.reuse", "true")
        .config(
            "spark.pyspark.python",
            os.environ["PYSPARK_PYTHON"],
        )
        .config(
            "spark.pyspark.driver.python",
            os.environ["PYSPARK_DRIVER_PYTHON"],
        )
        .config(
            "spark.executorEnv.PYSPARK_PYTHON",
            os.environ["PYSPARK_PYTHON"],
        )
        .config("spark.mongodb.read.connection.uri", mongo_uri)
    )
    if connector_jar:
        builder = builder.config(
            "spark.jars",
            str(Path(connector_jar).resolve()),
        )

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Ship project modules to Python workers used by foreachPartition.
    src_dir = Path(__file__).resolve().parent
    for py_file in src_dir.glob("*.py"):
        spark.sparkContext.addPyFile(str(py_file))

    started = time.perf_counter()
    try:
        probe = MongoStore(mongo_uri, database)
        try:
            raw_metric_docs = list(
                probe.db["quality_partition_metrics"].find(
                    {
                        "run_id": run_id,
                        "stage": "raw_classification_without_cleaning",
                    },
                    {"_id": 0},
                )
            )
            quarantine_exists = (
                probe.db[quarantine_collection].find_one(
                    {"run_id": run_id},
                    {"_id": 1},
                )
                is not None
            )
        finally:
            probe.close()

        raw_valid_count = sum(
            int(doc.get("raw_valid_count", 0))
            for doc in raw_metric_docs
        )
        raw_invalid_count = sum(
            int(doc.get("raw_invalid_count", 0))
            for doc in raw_metric_docs
        )
        raw_loaded = raw_valid_count + raw_invalid_count

        # If there is no quarantine input, cleaning has nothing to process.
        if not quarantine_exists:
            result: dict[str, Any] = {
                "step": "cleaning_after_raw_classification",
                "mode": (
                    "bounded_pyspark_cleaning"
                    if limit
                    else "full_pyspark_cleaning"
                ),
                "run_id": run_id,
                "classification_order": (
                    "raw_validated_and_raw_quarantined_then_clean_quarantine"
                ),
                "cleaning_input": "orders_quarantine_only",
                "cleaning_applied": True,
                "partitions": effective_partitions,
                "requested_partitions": partitions,
                "batch_size": batch_size,
                "raw_valid_count": raw_valid_count,
                "raw_invalid_count": raw_invalid_count,
                "raw_loaded": raw_loaded,
                "initial_valid_count": raw_valid_count,
                "initial_invalid_count": raw_invalid_count,
                "cleaned_quarantine_count": 0,
                "valid_count": raw_valid_count,
                "corrected_count": 0,
                "quarantine_count": 0,
                "inserted_count": 0,
                "updated_count": 0,
                "unchanged_count": 0,
                "error_case_counts": {},
            }
            result["elapsed_seconds"] = round(
                time.perf_counter() - started,
                6,
            )
            result["throughput_rows_per_second"] = round(
                raw_loaded / max(result["elapsed_seconds"], 0.000001),
                2,
            )
            result["reconciliation_ok"] = True
            write_results(result, reports_dir)
            return result

        # Read only the previously quarantined documents. No orders_raw read.
        cleaning_pipeline: list[dict[str, Any]] = [
            {"$match": {"run_id": run_id}},
            {"$project": {"raw_payload": 0}},
        ]
        if limit:
            cleaning_pipeline.append({"$limit": int(limit)})

        reader = (
            spark.read
            .format("mongodb")
            .option("connection.uri", mongo_uri)
            .option("database", database)
            .option("collection", quarantine_collection)
            .option(
                "aggregation.pipeline",
                json.dumps(cleaning_pipeline),
            )
        )
        if limit:
            reader = reader.option(
                "partitioner",
                "com.mongodb.spark.sql.connector.read.partitioner.SinglePartitionPartitioner",
            )

        quarantined = reader.load().drop("raw_payload", "_id")
        if limit:
            quarantined = quarantined.limit(int(limit))

        # Deliberately no persist/cache. A single downstream action consumes
        # the DataFrame and writes bounded batches directly from partitions.
        prepared = quarantined.repartition(effective_partitions)
        config = {
            "run_id": run_id,
            "mongo_uri": mongo_uri,
            "database": database,
            "validated_collection": validated_collection,
            "quarantine_collection": quarantine_collection,
            "metrics_collection": "quality_partition_metrics",
            "batch_size": max(int(batch_size), 1),
        }
        prepared.rdd.foreachPartition(
            lambda rows: _write_quarantine_cleaning_partition(rows, config)
        )

        store = MongoStore(mongo_uri, database)
        try:
            metric_docs = list(
                store.db["quality_partition_metrics"].find(
                    {"run_id": run_id},
                    {"_id": 0},
                )
            )
        finally:
            store.close()

        cleaning_docs = [
            doc
            for doc in metric_docs
            if doc.get("stage") == "cleaning_quarantine_only"
        ]
        cleaned_quarantine_count = sum(
            int(doc.get("cleaned_quarantine_count", 0))
            for doc in cleaning_docs
        )
        cleaned_valid_count = sum(
            int(doc.get("valid_count", 0))
            for doc in cleaning_docs
        )
        corrected_count = sum(
            int(doc.get("corrected_count", 0))
            for doc in cleaning_docs
        )
        quarantine_count = sum(
            int(doc.get("quarantine_count", 0))
            for doc in cleaning_docs
        )
        inserted_count = sum(
            int(doc.get("inserted_count", 0))
            for doc in cleaning_docs
        )
        updated_count = sum(
            int(doc.get("updated_count", 0))
            for doc in cleaning_docs
        )
        unchanged_count = sum(
            int(doc.get("unchanged_count", 0))
            for doc in cleaning_docs
        )
        error_case_counts: Counter = Counter()
        for doc in cleaning_docs:
            error_case_counts.update(
                doc.get("error_case_counts", {}) or {}
            )

        result = {
            "step": "cleaning_after_raw_classification",
            "mode": (
                "bounded_pyspark_cleaning"
                if limit
                else "full_pyspark_cleaning"
            ),
            "run_id": run_id,
            "classification_order": (
                "raw_validated_and_raw_quarantined_then_clean_quarantine"
            ),
            "cleaning_input": "orders_quarantine_only",
            "cleaning_applied": True,
            "partitions": effective_partitions,
            "requested_partitions": partitions,
            "batch_size": batch_size,
            "raw_valid_count": raw_valid_count,
            "raw_invalid_count": raw_invalid_count,
            "raw_loaded": raw_loaded,
            "initial_valid_count": raw_valid_count,
            "initial_invalid_count": raw_invalid_count,
            "cleaned_quarantine_count": cleaned_quarantine_count,
            "valid_count": raw_valid_count + cleaned_valid_count,
            "corrected_count": corrected_count,
            "quarantine_count": quarantine_count,
            "inserted_count": inserted_count,
            "updated_count": updated_count,
            "unchanged_count": unchanged_count,
            "error_case_counts": dict(error_case_counts),
        }
        result["elapsed_seconds"] = round(
            time.perf_counter() - started,
            6,
        )
        result["throughput_rows_per_second"] = round(
            cleaned_quarantine_count
            / max(result["elapsed_seconds"], 0.000001),
            2,
        )
        result["reconciliation_ok"] = (
            raw_loaded
            == result["valid_count"]
            + result["quarantine_count"]
        )
        write_results(result, reports_dir)
        return result
    finally:
        spark.stop()



def auto_connector_jar(explicit: str | None = None) -> str | None:
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    env_value = os.getenv("MONGO_SPARK_CONNECTOR_JAR")
    if env_value:
        candidates.append(Path(env_value))
    candidates.extend([
        ROOT / "tools" / "mongo-spark-connector_2.12-10.7.0-all.jar",
        ROOT.parent / "tools" / "mongo-spark-connector_2.12-10.7.0-all.jar",
        Path.cwd() / "tools" / "mongo-spark-connector_2.12-10.7.0-all.jar",
    ])
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate.resolve())
    return None


def resolve_master(value: str, selected_engine: str) -> str:
    if value and value != "auto":
        return value
    return "local[2]" if selected_engine == "pyspark" else "local[*]"


def open_store(args: argparse.Namespace, selected_engine: str) -> tuple[Any, str]:
    if selected_engine == "pyspark" and args.storage_backend == "local":
        raise ValueError("PySpark large-file route requires MongoDB; use --storage-backend auto or mongo")
    if args.storage_backend in {"auto", "mongo"}:
        try:
            return MongoStore(args.mongo_uri, args.database), "mongo"
        except Exception:
            if args.storage_backend == "mongo" or selected_engine == "pyspark":
                raise
    return JsonStore(args.local_store), "local"


def run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    discovery = None
    if args.step == "quarantine-view":
        if args.storage_backend == "local":
            local = JsonStore(args.local_store)
            rows = local.data.get("orders_quarantine", [])
            if args.run_id:
                rows = [row for row in rows if row.get("run_id") == args.run_id]
            rows = rows[: max(args.view_limit, 1)]
            local.close()
        else:
            rows = view_quarantine(args.mongo_uri, args.database, limit=args.view_limit, run_id=args.run_id)
        return {"step": "quarantine-view", "count": len(rows), "rows": rows}
    if args.step in {"discover", "raw-load", "all"}:
        if not args.input:
            raise ValueError("--input is required for this step")
        discovery = discover_file(args.input, args.threshold_mb)
        write_discovery_report(discovery, reports_dir / "discovery.json")
        # A different Header is not a crash condition. The discovery report
        # records missing groups; Schema Validation handles those rows safely.
    if args.step == "discover":
        return {"discovery": discovery.to_dict()}
    if args.step == "quality":
        if not args.run_id:
            raise ValueError("--run-id is required for quality")
        connector = auto_connector_jar(args.connector_jar)
        master = resolve_master(args.master, "pyspark")
        return {"raw_classification": run_quality_pyspark(args.run_id, mongo_uri=args.mongo_uri, database=args.database, partitions=args.partitions, batch_size=args.batch_size, master=master, connector_jar=connector, reports_dir=reports_dir, limit=args.limit)}
    if args.step == "cleaning":
        if not args.run_id:
            raise ValueError("--run-id is required for cleaning")
        connector = auto_connector_jar(args.connector_jar)
        master = resolve_master(args.master, "pyspark")
        return {"cleaning": run_cleaning_pyspark(args.run_id, mongo_uri=args.mongo_uri, database=args.database, partitions=args.partitions, batch_size=args.batch_size, master=master, connector_jar=connector, reports_dir=reports_dir, limit=args.limit)}
    selected_engine = args.engine if args.engine != "auto" else discovery.engine_used
    selected_partitions = recommended_partitions(discovery.file_size_mb if discovery else None, args.partitions)
    selected_master = resolve_master(args.master, selected_engine)
    connector = auto_connector_jar(args.connector_jar)
    store, backend_used = open_store(args, selected_engine)
    try:
        if selected_engine == "python_batch":
            result = load_orders_batch(args.input, store, run_id=discovery.run_id if discovery else args.run_id, batch_size=args.batch_size, reports_dir=reports_dir)
        elif selected_engine == "pyspark":
            store.close()
            result = load_orders_raw_spark(args.input, mongo_uri=args.mongo_uri, database=args.database, partitions=selected_partitions, master=selected_master, connector_jar=connector, report_path=reports_dir / "raw_load.json", run_id=discovery.run_id if discovery else args.run_id)
            backend_used = "mongo"
        else:
            raise ValueError(f"Unsupported engine: {selected_engine}")
    finally:
        if selected_engine == "python_batch":
            store.close()
    output: dict[str, Any] = {"step": args.step, "engine_selected": selected_engine, "backend_used": backend_used, "partitions": selected_partitions, "master": selected_master, "connector_jar": connector, "discovery": discovery.to_dict() if discovery else None, "raw_load": result}
    if args.step == "all":
        if selected_engine == "pyspark":
            output["raw_classification"] = run_quality_pyspark(result["run_id"], mongo_uri=args.mongo_uri, database=args.database, partitions=selected_partitions, batch_size=args.batch_size, master=selected_master, connector_jar=connector, reports_dir=reports_dir, limit=args.limit)
            output["cleaning"] = run_cleaning_pyspark(result["run_id"], mongo_uri=args.mongo_uri, database=args.database, partitions=selected_partitions, batch_size=args.batch_size, master=selected_master, connector_jar=connector, reports_dir=reports_dir, limit=args.limit)
        else:
            output["raw_classification"] = result
            clean_store, _ = open_store(args, selected_engine)
            try:
                output["cleaning"] = clean_after_raw_batch(clean_store, result["run_id"], reports_dir=reports_dir, raw_valid_count=result.get("raw_valid_count"), raw_invalid_count=result.get("raw_invalid_count"))
            finally:
                clean_store.close()
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Exact-only hybrid data pipeline")
    parser.add_argument("--step", choices=["discover", "raw-load", "quality", "cleaning", "all", "quarantine-view"], default="all")
    parser.add_argument("--input")
    parser.add_argument("--run-id")
    parser.add_argument("--engine", choices=["auto", "python_batch", "pyspark"], default="auto")
    parser.add_argument("--threshold-mb", type=float, default=200.0)
    parser.add_argument("--mongo-uri", default="mongodb://127.0.0.1:27017")
    parser.add_argument("--database", default="ecommerce_store")
    parser.add_argument("--partitions", type=int, default=0, help="0=auto based on CPU and file size")
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--master", default="auto", help="auto=resource-aware local master")
    parser.add_argument("--connector-jar")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--local-store", default="data/local_store.json")
    parser.add_argument("--view-limit", type=int, default=20, help="Rows to show with --step quarantine-view")
    parser.add_argument("--storage-backend", choices=["auto", "mongo", "local"], default="auto")
    return parser


def _write_error_report(error: Exception, args: argparse.Namespace) -> dict[str, Any]:
    payload = {
        "step": getattr(args, "step", None),
        "input": getattr(args, "input", None),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "recovery": "Check the reported resource, path, schema, MongoDB, Java, or Connector requirement; no partial JSON result is treated as successful.",
    }
    reports_dir = Path(getattr(args, "reports_dir", "reports"))
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "error.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    args = build_parser().parse_args()
    try:
        print(json.dumps(run_pipeline(args), ensure_ascii=False, indent=2, default=str))
    except Exception as error:
        print(json.dumps(_write_error_report(error, args), ensure_ascii=False, indent=2))
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
