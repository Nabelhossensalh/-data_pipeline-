"""Optional Path B: watermark-based incremental loading."""

from __future__ import annotations

import csv
import uuid
from pathlib import Path
from typing import Any

from elt_pipeline import JsonStore, _raw_document
from metrics import RunMetrics, write_results
from quality_rules import classify_raw_document


def run_incremental(
    source_file: str | Path,
    store: JsonStore,
    *,
    watermark: int = 0,
    run_id: str | None = None,
    reports_dir: str | Path = "reports",
) -> dict[str, Any]:
    path = Path(source_file)
    run_id = run_id or str(uuid.uuid4())
    raw_rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for source_row_number, row in enumerate(csv.DictReader(handle), start=2):
            if source_row_number > watermark:
                raw_rows.append(_raw_document(row, path, run_id, source_row_number, "python_incremental"))
    store.insert_raw(raw_rows)
    metrics = RunMetrics(run_id, "incremental")
    metrics.raw_loaded = len(raw_rows)
    classified = [classify_raw_document(row) for row in raw_rows]
    for item in classified:
        if item["initial_classification"] == "valid":
            metrics.initial_valid_count += 1
            metrics.valid_count += 1
            outcome = store.upsert_validated(item["final_document"])
            setattr(metrics, f"{outcome}_count", getattr(metrics, f"{outcome}_count") + 1)
    for item in classified:
        if item["initial_classification"] != "invalid":
            continue
        metrics.initial_invalid_count += 1
        final = item["final_document"]
        if final.get("quality_status") == "corrected":
            metrics.corrected_count += 1
            store.remove_quarantine(final)
            outcome = store.upsert_validated(final)
        else:
            metrics.quarantine_count += 1
            for code in final.get("error_codes", []):
                metrics.add_error(code)
            outcome = store.upsert_quarantine(final)
        setattr(metrics, f"{outcome}_count", getattr(metrics, f"{outcome}_count") + 1)
    result = metrics.finish()
    result.update({"engine_used": "python_incremental", "watermark": watermark, "classification_order": "validated_before_quarantine"})
    write_results(result, reports_dir)
    return result


__all__ = ["run_incremental"]
