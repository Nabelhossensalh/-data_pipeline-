"""Metrics, reconciliation, and report generation."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RunMetrics:
    run_id: str
    step: str
    started_at: float = field(default_factory=time.perf_counter)
    raw_loaded: int = 0
    initial_valid_count: int = 0
    initial_invalid_count: int = 0
    raw_valid_count: int = 0
    raw_invalid_count: int = 0
    valid_count: int = 0
    corrected_count: int = 0
    quarantine_count: int = 0
    inserted_count: int = 0
    updated_count: int = 0
    unchanged_count: int = 0
    error_case_counts: dict[str, int] = field(default_factory=dict)
    cleaning_applied: bool = False

    def add_error(self, code: str) -> None:
        self.error_case_counts[code] = self.error_case_counts.get(code, 0) + 1

    def finish(self) -> dict[str, Any]:
        elapsed = max(time.perf_counter() - self.started_at, 0.000001)
        reconciliation = (
            self.raw_loaded == self.initial_valid_count + self.initial_invalid_count
            and self.raw_loaded == self.valid_count + self.corrected_count + self.quarantine_count
        )
        return {
            "step": self.step,
            "run_id": self.run_id,
            "raw_loaded": self.raw_loaded,
            "initial_valid_count": self.initial_valid_count,
            "initial_invalid_count": self.initial_invalid_count,
            "raw_valid_count": self.raw_valid_count,
            "raw_invalid_count": self.raw_invalid_count,
            "valid_count": self.valid_count,
            "corrected_count": self.corrected_count,
            "quarantine_count": self.quarantine_count,
            "inserted_count": self.inserted_count,
            "updated_count": self.updated_count,
            "unchanged_count": self.unchanged_count,
            "error_case_counts": self.error_case_counts,
            "cleaning_applied": self.cleaning_applied,
            "elapsed_seconds": round(elapsed, 6),
            "throughput_rows_per_second": round(self.raw_loaded / elapsed, 2),
            "reconciliation_ok": reconciliation,
        }


def write_results(result: dict[str, Any] | RunMetrics, reports_dir: str | Path = "reports") -> dict[str, str]:
    directory = Path(reports_dir)
    directory.mkdir(parents=True, exist_ok=True)
    if isinstance(result, RunMetrics):
        result = result.finish()
    json_path = directory / "results.json"
    md_path = directory / "results.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = ["# Pipeline Results", "", "| Metric | Value |", "|---|---:|"]
    for key, value in result.items():
        if isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False)
        rows.append(f"| `{key}` | {value} |")
    md_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def reconcile(metrics: dict[str, Any]) -> bool:
    return bool(metrics.get("reconciliation_ok"))


__all__ = ["RunMetrics", "write_results", "reconcile"]
