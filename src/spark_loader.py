"""PySpark Raw Load for large CSV inputs."""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from file_router import detect_delimiter


def load_orders_raw_spark(
    source_file: str | Path,
    *,
    mongo_uri: str,
    database: str,
    collection: str = "orders_raw",
    partitions: int = 32,
    master: str = "local[*]",
    connector_jar: str | Path | None = None,
    report_path: str | Path = "reports/raw_load.json",
    run_id: str | None = None,
    write_mongo: bool = True,
) -> dict[str, Any]:
    try:
        from pyspark.sql import SparkSession, functions as F
    except ImportError as exc:
        raise RuntimeError("PySpark is required for the large-file route") from exc
    path = Path(source_file)
    if not path.is_file():
        raise FileNotFoundError(path)
    if partitions <= 0:
        size_mb = path.stat().st_size / (1024 * 1024)
        cpu = max(os.cpu_count() or 2, 2)
        if size_mb >= 10240:
            partitions = min(max(cpu * 8, 64), 512)
        elif size_mb >= 1024:
            partitions = min(max(cpu * 4, 32), 256)
        else:
            partitions = min(max(cpu * 2, 8), 128)
    if connector_jar and not Path(connector_jar).is_file() and write_mongo:
        raise FileNotFoundError(f"MongoDB Spark Connector not found: {connector_jar}")
    run_id = run_id or str(uuid.uuid4())
    delimiter = detect_delimiter(path)
    started = time.perf_counter()
    builder = (
        SparkSession.builder.appName("Midterm-Raw-Load")
        .master(master)
        .config("spark.default.parallelism", str(partitions))
        .config("spark.sql.shuffle.partitions", str(partitions))
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.local.dir", os.getenv("SPARK_LOCAL_DIRS", r"E:\spark-tmp"))
    )
    if connector_jar:
        builder = builder.config("spark.jars", str(Path(connector_jar).resolve()))
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    try:
        frame = (
            spark.read
            .option("header", True)
            .option("inferSchema", False)
            .option("sep", delimiter)
            .option("quote", '"')
            .option("escape", '"')
            .option("multiLine", False)
            .option("mode", "PERMISSIVE")
            .csv(str(path))
        )
        columns = frame.columns
        payload = F.to_json(F.struct(*[F.col(column) for column in columns]))
        raw = (
            frame.withColumn("run_id", F.lit(run_id))
            .withColumn("source_file", F.lit(str(path.resolve())))
            .withColumn("source_row_number", F.monotonically_increasing_id())
            .withColumn("ingested_at", F.current_timestamp())
            .withColumn("engine_used", F.lit("pyspark"))
            .withColumn("raw_payload", payload)
            .repartition(partitions)
        )
        row_count = raw.count()
        if write_mongo:
            (
                raw.write.format("mongodb")
                .mode("append")
                .option("connection.uri", mongo_uri)
                .option("database", database)
                .option("collection", collection)
                .save()
            )
        elapsed = max(time.perf_counter() - started, 0.000001)
        result = {
            "step": "raw_load",
            "run_id": run_id,
            "source_file": str(path.resolve()),
            "header_columns": columns,
            "delimiter": delimiter,
            "raw_loaded": int(row_count),
            "input_partitions": raw.rdd.getNumPartitions(),
            "engine_used": "pyspark",
            "mongo_target": f"{database}.{collection}",
            "write_mongo": write_mongo,
            "elapsed_seconds": round(elapsed, 6),
            "throughput_rows_per_second": round(row_count / elapsed, 2),
        }
        report = Path(report_path)
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return result
    finally:
        spark.stop()


load_csv_with_spark = load_orders_raw_spark

__all__ = ["load_orders_raw_spark", "load_csv_with_spark"]
