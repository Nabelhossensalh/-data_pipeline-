"""Python Batch loader for small and medium CSV inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from elt_pipeline import JsonStore, load_csv_streaming


def load_orders_batch(
    source_file: str | Path,
    store: JsonStore,
    *,
    run_id: str | None = None,
    batch_size: int = 500,
    reports_dir: str | Path = "reports",
) -> dict[str, Any]:
    return load_csv_streaming(
        source_file,
        store,
        engine="python_batch",
        batch_size=batch_size,
        run_id=run_id,
        reports_dir=reports_dir,
    )


load_csv_batch = load_orders_batch

__all__ = ["load_orders_batch", "load_csv_batch"]
