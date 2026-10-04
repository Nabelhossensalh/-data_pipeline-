# from __future__ import annotations

# import os
# from dataclasses import dataclass
# from pathlib import Path


# @dataclass(frozen=True)
# class Settings:
#     mongo_uri: str = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
#     database: str = os.getenv("DATABASE", "ecommerce_store")
#     source_collection: str = os.getenv("SOURCE_COLLECTION", "orders_validated")
#     mv_city: str = os.getenv("MV_CITY", "mv_sales_by_city")
#     mv_products: str = os.getenv("MV_PRODUCTS", "mv_top_products")
#     events: str = os.getenv("MV_EVENTS", "mv_processed_events")
#     state: str = os.getenv("MV_STATE", "mv_state")
#     jobs: str = os.getenv("JOB_RUNS", "job_runs")
#     delivered_status: str = os.getenv("DELIVERED_STATUS", "تم التسليم")
#     reports_dir: Path = Path(os.getenv("REPORTS_DIR", "reports"))


# settings = Settings()













from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


DEFAULT_MIDTERM_MAIN_SCRIPT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "main.py"
)


@dataclass(frozen=True)
class Settings:
    # ========================================================
    # MongoDB
    # ========================================================

    mongo_uri: str = os.getenv(
        "MONGO_URI",
        "mongodb://127.0.0.1:27017",
    )

    database: str = os.getenv(
        "DATABASE",
        "ecommerce_store",
    )

    # ========================================================
    # Final Project Source
    # ========================================================
    # Read from the validated collection produced by the midterm pipeline.

    source_collection: str = os.getenv(
        "SOURCE_COLLECTION",
        "orders_validated",
    )

    midterm_main_script: Path = Path(
        os.getenv("MIDTERM_MAIN_SCRIPT", str(DEFAULT_MIDTERM_MAIN_SCRIPT))
    )

    original_collection: str = os.getenv(
        "ORIGINAL_COLLECTION",
        "orders_validated",
    )

    # ========================================================
    # Quarantine
    # ========================================================

    quarantine_collection: str = os.getenv(
        "QUARANTINE_COLLECTION",
        "orders_quarantine",
    )

    # ========================================================
    # Materialized Views
    # ========================================================

    mv_city: str = os.getenv(
        "MV_CITY",
        "mv_sales_by_city",
    )

    mv_products: str = os.getenv(
        "MV_PRODUCTS",
        "mv_top_products",
    )

    # ========================================================
    # Incremental Processing
    # ========================================================

    events: str = os.getenv(
        "MV_EVENTS",
        "mv_processed_events",
    )

    state: str = os.getenv(
        "MV_STATE",
        "mv_state",
    )

    # ========================================================
    # Scheduled Jobs
    # ========================================================

    jobs: str = os.getenv(
        "JOB_RUNS",
        "job_runs",
    )

    # ========================================================
    # Data Rules
    # ========================================================

    delivered_status: str = os.getenv(
        "DELIVERED_STATUS",
        "تم التسليم",
    )

    # ========================================================
    # Scheduling
    # ========================================================

    incremental_schedule_minutes: int = int(
        os.getenv(
            "INCREMENTAL_SCHEDULE_MINUTES",
            "5",
        )
    )

    report_schedule_minutes: int = int(
        os.getenv(
            "REPORT_SCHEDULE_MINUTES",
            "60",
        )
    )

    # ========================================================
    # Reports
    # ========================================================

    reports_dir: Path = Path(
        os.getenv(
            "REPORTS_DIR",
            "reports",
        )
    )


settings = Settings()