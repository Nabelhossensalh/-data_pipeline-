"""File discovery and automatic Python Batch/PySpark routing."""

from __future__ import annotations

import csv
import json
import re
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_THRESHOLD_MB = 200.0
REQUIRED_GROUPS = {
    "order_id": ("order_id", "orderid", "order id", "id"),
    "customer_id": ("customer_id", "customerid", "customer id"),
    "items": ("items_json", "items", "items_raw", "items_data", "order_items"),
}


@dataclass(frozen=True)
class DiscoveryResult:
    run_id: str
    source_file: str
    file_name: str
    file_size_bytes: int
    file_size_mb: float
    engine_used: str
    routing_reason: str
    header_columns: list[str]
    header_column_count: int
    missing_required_groups: list[str]
    header_check: str
    delimiter: str
    discovered_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def detect_delimiter(source_file: str | Path) -> str:
    path = Path(source_file)
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        sample = handle.read(8192)
    header_line = next((line for line in sample.splitlines() if line.strip()), "")
    candidates = [",", ";", "\t", "|", ":"]
    counts = {delimiter: header_line.count(delimiter) for delimiter in candidates}
    best = max(candidates, key=lambda delimiter: counts[delimiter])
    if counts[best] > 0:
        return best
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|:").delimiter
    except csv.Error:
        return ","


def read_csv_header(source_file: str | Path) -> list[str]:
    path = Path(source_file)
    delimiter = detect_delimiter(path)
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        header = next(csv.reader(handle, delimiter=delimiter), None)
    if not header:
        raise ValueError(f"CSV file has no header: {path}")
    return [column.strip().lstrip("\ufeff") for column in header]


def discover_file(source_file: str | Path, threshold_mb: float = DEFAULT_THRESHOLD_MB) -> DiscoveryResult:
    path = Path(source_file).expanduser()
    if not path.is_file():
        raise FileNotFoundError(path)
    if threshold_mb <= 0:
        raise ValueError("threshold_mb must be positive")
    size_bytes = path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)
    engine = "python_batch" if size_mb <= threshold_mb else "pyspark"
    reason = f"file_size_mb={size_mb:.2f} {'<=' if engine == 'python_batch' else '>'} threshold_mb={threshold_mb:.2f}"
    header = read_csv_header(path)
    delimiter = detect_delimiter(path)
    names = {re.sub(r"[^a-z0-9]", "", column.lower()) for column in header}
    missing = [name for name, aliases in REQUIRED_GROUPS.items() if not any(re.sub(r"[^a-z0-9]", "", alias.lower()) in names for alias in aliases)]
    return DiscoveryResult(
        run_id=str(uuid.uuid4()),
        source_file=str(path.resolve()),
        file_name=path.name,
        file_size_bytes=size_bytes,
        file_size_mb=round(size_mb, 6),
        engine_used=engine,
        routing_reason=reason,
        header_columns=header,
        header_column_count=len(header),
        missing_required_groups=missing,
        header_check="pass" if not missing else "needs_mapping_or_review",
        delimiter=delimiter,
        discovered_at=datetime.now(timezone.utc).isoformat(),
    )


def choose_engine(source_file: str | Path, threshold_mb: float = DEFAULT_THRESHOLD_MB) -> str:
    return discover_file(source_file, threshold_mb).engine_used


def write_discovery_report(result: DiscoveryResult, report_path: str | Path) -> None:
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


__all__ = ["DiscoveryResult", "discover_file", "choose_engine", "read_csv_header", "detect_delimiter", "write_discovery_report"]
