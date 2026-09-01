# Pipeline Results

| Metric | Value |
|---|---:|
| `step` | cleaning_after_raw_classification |
| `mode` | full_pyspark_cleaning |
| `run_id` | c1d9bdac-ed2d-434d-8c5d-2cb53475bdd5 |
| `classification_order` | raw_validated_and_raw_quarantined_then_clean_quarantine |
| `cleaning_input` | orders_quarantine_only |
| `cleaning_applied` | True |
| `partitions` | 2 |
| `requested_partitions` | 2 |
| `batch_size` | 500 |
| `raw_valid_count` | 23664580 |
| `raw_invalid_count` | 6335420 |
| `raw_loaded` | 30000000 |
| `initial_valid_count` | 23664580 |
| `initial_invalid_count` | 6335420 |
| `cleaned_quarantine_count` | 6335420 |
| `valid_count` | 23664580 |
| `corrected_count` | 1990816 |
| `quarantine_count` | 4344604 |
| `inserted_count` | 1990816 |
| `updated_count` | 4344604 |
| `unchanged_count` | 0 |
| `error_case_counts` | {"INVALID_PAYMENT_STATUS": 221163, "INVALID_IMPOSSIBLE_DATE": 872569, "INVALID_EMAIL": 207761, "SCHEMA_REQUIRED_FIELD": 628866, "INVALID_PHONE": 208594, "UNKNOWN_PRICE": 748443, "INVALID_STATUS": 208666, "DUPLICATE_ORDER_ID": 417584, "AMBIGUOUS_NEGATIVE_VALUE": 207653, "INVALID_CURRENCY": 208736, "CORRUPTED_ITEMS_JSON": 208978, "EMPTY_ITEMS": 208471} |
| `elapsed_seconds` | 4781.543309 |
| `throughput_rows_per_second` | 1324.97 |
| `reconciliation_ok` | False |
