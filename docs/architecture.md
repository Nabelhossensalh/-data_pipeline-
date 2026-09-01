# Architecture

## Exact project structure

This version intentionally contains only the files requested in the course structure. The implementation of discovery, loaders, quality rules, MongoDB operations, metrics, and orchestration is embedded inside those allowed files.

## Execution flow

```text
CSV file
  |
  v
file_router.py: metadata + header + engine selection
  |
  +--> Python Batch --> batch_loader.py / elt_pipeline.py
  |
  `--> PySpark --> spark_loader.py
                    |
                    v
              orders_raw
                    |
                    v
             main.py quality route
                    |
          initial Business Validation
                    |
          +---------+----------+
          |                    |
 valid as-is             initially invalid
          |                    |
 Action 1                 Action 2
          |                    |
 orders_validated   corrected -> orders_validated
                    unsafe    -> orders_quarantine
```

## File responsibilities

`main.py` is the executable entry point. `file_router.py` performs discovery and routing. `create_small_sample.py` creates bounded CSV samples. `batch_loader.py` and `elt_pipeline.py` implement the Python Batch Raw-first route. `spark_loader.py` implements large-file Raw Load through PySpark. `quality_rules.py` contains Business Validation, safe corrections, Audit Trail, initial classification, and Quarantine reasons. `incremental_loader.py` provides the optional watermark-based Path B. `mongo_setup.py` creates MongoDB indexes and performs idempotent writes. `metrics.py` writes JSON and Markdown metrics.

## Data contracts

Every raw row receives a stable `run_id`, source metadata, and `raw_payload` before quality processing. A corrected record contains `quality_status: corrected` and a `corrections` list with `field`, `original_value`, `corrected_value`, and `rule_code`. An unsafe record contains `error_codes`, `error_details`, `original_document`, and `raw_payload` in `orders_quarantine`.

## Idempotency and reconciliation

`orders_validated` uses `order_id` as its business key. `orders_quarantine` uses `run_id` and `source_row_number`. Both routes use upsert semantics, so replaying the same input does not create duplicate business records. Metrics verify:

```text
raw_loaded = initial_valid_count + initial_invalid_count
raw_loaded = valid_count + corrected_count + quarantine_count
```

The exact-only package does not include the large CSV, MongoDB data files, or a connector JAR. Pass the external connector path through `--connector-jar` when running the PySpark route on Windows.

## Validation order

After Raw Load, each record passes through the following ordered stages:

```text
1. Raw record is read from orders_raw.
2. Raw Schema Validation checks required fields and the raw envelope.
3. Business Validation checks dates, enums, phone, email, items, prices, payments, currency, and totals.
4. Duplicate Detection checks the stable order_id business key.
5. Valid records are written to orders_validated.
6. Invalid records are corrected safely or written to orders_quarantine with error_codes and error_details.
```

The MongoDB `orders_validated` collection has a strict `$jsonSchema` validator for required fields, BSON types, allowed values, nested customer/payment objects, arrays, and canonical dates. The `quarantine-view` command displays rejected documents and their reasons:

```powershell
python src\main.py --step quarantine-view --mongo-uri "mongodb://127.0.0.1:27017" --database "ecommerce_store" --view-limit 20
```

## Cleaning is the final stage

The raw classification stage does not normalize dates, emails, phones, currencies, prices, or totals. It checks the raw envelope, raw business rules, and duplicate business key exactly as received. A raw-valid row is written immediately to `orders_validated` with `quality_status: raw_validated` and `cleaning_applied: false`; a raw-invalid row is written immediately to `orders_quarantine` with its original document and raw error details. Cleaning is a later stage that reads `orders_quarantine` only. A safely corrected quarantined row is then upserted into `orders_validated`; an unsafe row remains in `orders_quarantine`.

## Dynamic execution for instructor testing

The router uses the file size and the configured threshold to select Python Batch or PySpark. `--partitions 0` selects a safe partition count from CPU count and file size; a positive value overrides the automatic policy. Batch processing uses a bounded buffer and disk-backed replay passes, while PySpark uses DataFrame partitions and MongoDB partition writes.

The reader detects comma, semicolon, tab, pipe, and colon delimiters. Header aliases such as `orderid`, `order id`, `customer id`, `order_items`, `order total`, and `payment amount` are mapped to canonical business fields. The same code therefore handles very small files, files with only a few rows, and multi-gigabyte files without changing the source code. This dynamic behavior applies to CSV order data that follows the project contract; a file cannot be treated as a valid order dataset when it lacks non-inferable business fields such as the order identifier or items. Unknown or missing fields are not silently discarded; they appear in the Discovery and Schema reports and are quarantined safely.

For a small file, the instructor can run:

```powershell
python src\main.py --step all --engine auto --input "C:\path\small.csv" --partitions 0 --batch-size 500 --storage-backend local --local-store data\local_store.json --reports-dir reports
```

For a large file, the instructor can run Raw Load and Quality separately:

```powershell
python src\main.py --step raw-load --engine auto --input "C:\path\large.csv" --partitions 0 --mongo-uri "mongodb://127.0.0.1:27017" --database "ecommerce_store" --connector-jar "C:\path\mongo-spark-connector_2.12-10.7.0-all.jar" --reports-dir reports
python src\main.py --step quality --run-id "RUN_ID_FROM_RAW_REPORT" --partitions 0 --mongo-uri "mongodb://127.0.0.1:27017" --database "ecommerce_store" --connector-jar "C:\path\mongo-spark-connector_2.12-10.7.0-all.jar" --reports-dir reports
```

Operational failures are written to `reports/error.json` with an error type, message, and recovery hint. A failed run is never reported as a successful reconciliation.

## One-command automatic mode

The default command runs the complete pipeline without a manual transition between stages. The `--step all` mode is the automatic mode; the Notebook remains available for examining each stage separately:

```powershell
python src\main.py --input "C:\path\data.csv" --partitions 0 --batch-size 500 --storage-backend auto --reports-dir reports
```

The program discovers the file, selects Python Batch or PySpark, selects a resource-aware master and partition count, locates the Connector from the explicit argument or `MONGO_SPARK_CONNECTOR_JAR`, chooses MongoDB when reachable and Local Store only when the automatic small-file fallback is safe, then runs Raw Load, Schema, Duplicate, Cleaning Last, final routing, and Metrics. Large PySpark input requires a reachable MongoDB and a valid Connector; it never silently falls back to local memory processing.

## Raw classification before cleaning

The first quality action is intentionally a no-cleaning classification. It reads `orders_raw`, validates the values exactly as received, checks duplicates, and writes raw-valid records to `orders_validated` with `quality_status: raw_validated` and `cleaning_applied: false`. It writes raw-invalid records to `orders_quarantine` with `raw_validation_only: true`, `error_codes`, `error_details`, and the original raw document. The later Cleaning Last action reads only `orders_quarantine`; it never re-cleans the raw-valid records already stored in `orders_validated`. Safely corrected quarantined records receive `quality_status: corrected` and move to `orders_validated`, while uncorrectable records remain quarantined.

The primary first-pass metrics are:

```text
raw_valid_count + raw_invalid_count = raw_loaded
cleaning_applied = false
reconciliation_ok = true
```

Cleaning and correction are a later stage and are not included in the first-pass counts. A date such as `31 / 01 / 2025`, a normalized synonym, or a repeated email symbol is therefore counted as raw-invalid in this first pass rather than silently corrected.
