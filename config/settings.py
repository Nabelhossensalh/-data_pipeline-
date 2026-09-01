"""Central configuration for the hybrid orders data pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    project_root: Path = PROJECT_ROOT
    small_file_threshold_mb: int = int(os.getenv("SMALL_FILE_THRESHOLD_MB", "200"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "500"))
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_database: str = os.getenv("MONGO_DATABASE", "midterm_pipeline")
    storage_backend: str = os.getenv("STORAGE_BACKEND", "local")
    local_store_path: Path = Path(
        os.getenv("LOCAL_STORE_PATH", str(PROJECT_ROOT / "data" / "local_store.json"))
    )
    reports_dir: Path = Path(
        os.getenv("REPORTS_DIR", str(PROJECT_ROOT / "reports"))
    )
    raw_collection: str = "orders_raw"
    validated_collection: str = "orders_validated"
    quarantine_collection: str = "orders_quarantine"
    spark_master: str = os.getenv("SPARK_MASTER", "local[*]")

    def ensure_directories(self) -> None:
        self.local_store_path.parent.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
