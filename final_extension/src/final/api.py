from __future__ import annotations

import json
import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from .config import settings
from .db import (
    ensure_indexes,
    get_client,
    get_db,
)
from .explain import run_explain_benchmarks
from .jobs import (
    JOBS,
    scheduler_status,
    start_scheduler,
    stop_scheduler,
)
from .materialized_views import (
    full_refresh,
    incremental_refresh,
)
from .reports import REPORTS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: start background scheduled jobs
    start_scheduler()
    yield
    # Shutdown: safely terminate scheduler
    stop_scheduler()


app = FastAPI(
    title="Al-Razi Data Pipeline API",
    description="Unified API for Big Data Phase 2 Final Extension",
    version="2.0.0",
    lifespan=lifespan,
)


# ============================================================
# Database Helper
# ============================================================

def with_db(fn: Callable):
    client = get_client()
    try:
        return fn(get_db(client))
    finally:
        client.close()


# ============================================================
# Root Redirect
# ============================================================

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# ============================================================
# 1. Health
# ============================================================

@app.get("/health")
def health():
    def check(db):
        db.client.admin.command("ping")
        return {
            "status": "ok",
            "database": settings.database,
            "source_collection": settings.source_collection,
            "scheduler_running": scheduler_status()["running"],
        }

    return with_db(check)


# ============================================================
# 2. Ingestion Gateway (Midterm Pipeline Integration)
# ============================================================


class IngestRequest(BaseModel):
    source_file: str


@app.post("/ingest")
def ingest(payload: IngestRequest):
    """
    POST /ingest
    Runs the existing midterm pipeline for a local input file.
    """
    source_file = Path(payload.source_file).expanduser().resolve()
    if not source_file.is_file():
        raise HTTPException(status_code=400, detail="source_file must be an existing local input file")

    pipeline_script = settings.midterm_main_script.expanduser().resolve()
    if not pipeline_script.is_file():
        raise HTTPException(
            status_code=503,
            detail=f"Midterm pipeline entry point not found: {pipeline_script}",
        )

    command = [
        sys.executable,
        str(pipeline_script),
        "--step", "all",
        "--input", str(source_file),
        "--engine", "auto",
        "--mongo-uri", settings.mongo_uri,
        "--database", settings.database,
        "--storage-backend", "mongo",
    ]
    result = subprocess.run(
        command,
        cwd=pipeline_script.parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )

    try:
        pipeline_result = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Midterm pipeline returned invalid JSON",
                "stderr": result.stderr[-4000:],
            },
        ) from exc

    if result.returncode != 0:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Midterm pipeline failed",
                "pipeline_result": pipeline_result,
            },
        )

    return {
        "status": "ok",
        "pipeline": "midterm_pipeline",
        "source_file": str(source_file),
        "result": pipeline_result,
    }


# ============================================================
# 3. Indexes
# ============================================================

@app.post("/indexes")
def indexes():
    return {
        "status": "ok",
        "indexes": with_db(ensure_indexes),
    }


# ============================================================
# 4. Queries (5 Practical Queries)
# ============================================================

QUERY_SPECS = {
    "orders_by_city": {
        "description": "توزيع الطلبات حسب المدينة",
        "collection": lambda: settings.source_collection,
        "pipeline": lambda limit: [
            {"$group": {"_id": "$customer.address.city", "count": {"$sum": 1}}},
            {"$project": {"_id": 0, "city": {"$ifNull": ["$_id", "UNKNOWN"]}, "count": 1}},
            {"$sort": {"count": -1}},
            {"$limit": limit},
        ],
    },
    "quarantine_by_error": {
        "description": "توزيع أخطاء العزل (Quarantine) حسب نوع الخطأ",
        "collection": lambda: settings.quarantine_collection,
        "pipeline": lambda limit: [
            {"$unwind": "$error_codes"},
            {"$group": {"_id": "$error_codes", "count": {"$sum": 1}}},
            {"$project": {"_id": 0, "error_code": "$_id", "count": 1}},
            {"$sort": {"count": -1}},
            {"$limit": limit},
        ],
    },
    "corrected_orders": {
        "description": "الطلبات المصححة عبر قواعد جودة البيانات",
        "collection": lambda: settings.source_collection,
        "pipeline": lambda limit: [
            {"$match": {"quality_status": "corrected"}},
            {"$limit": limit},
        ],
    },
    "customer_orders": {
        "description": "عدد الطلبات لكل عميل مرتبة تنازلياً",
        "collection": lambda: settings.source_collection,
        "pipeline": lambda limit: [
            {"$group": {"_id": "$customer.customer_id", "count": {"$sum": 1}}},
            {"$project": {"_id": 0, "customer_id": "$_id", "count": 1}},
            {"$sort": {"count": -1}},
            {"$limit": limit},
        ],
    },
    "recent_orders": {
        "description": "أحدث الطلبات المعالجة في النظام",
        "collection": lambda: settings.source_collection,
        "pipeline": lambda limit: [
            {"$sort": {"processed_at": -1}},
            {"$limit": limit},
        ],
    },
}


@app.get("/queries")
def queries():
    return {
        "names": sorted(QUERY_SPECS.keys()),
        "details": {
            k: v["description"] for k, v in QUERY_SPECS.items()
        },
    }


@app.get("/queries/{name}")
def query(name: str, limit: int = 20):
    if name not in QUERY_SPECS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown query: {name}. Available: {list(QUERY_SPECS.keys())}",
        )

    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    def execute(db):
        spec = QUERY_SPECS[name]
        collection_name = spec["collection"]()
        pipeline = spec["pipeline"](limit)

        data = list(
            db[collection_name].aggregate(pipeline, allowDiskUse=True)
        )
        for row in data:
            row.pop("_id", None)

        return {
            "name": name,
            "description": spec["description"],
            "collection": collection_name,
            "limit": limit,
            "rows": len(data),
            "data": data,
        }

    return with_db(execute)


# ============================================================
# 5. Aggregation Reports (5 Required Reports)
# ============================================================

@app.get("/aggregations")
def aggregations():
    return {
        "names": sorted(REPORTS.keys()),
        "descriptions": {
            "sales_by_city": "إجمالي المبيعات وعدد الطلبات لكل مدينة",
            "top_products": "المنتجات الأكثر مبيعاً حسب الكميات والمبالغ",
            "sales_by_period": "المبيعات الشهرية عبر السنوات",
            "top_customers": "أفضل العملاء من حيث إجمالي المشتريات",
            "orders_by_status": "توزيع الطلبات والمبالغ حسب حالة الطلب",
        },
    }


@app.get("/aggregations/{name}")
def aggregation(name: str):
    alias_map = {
        "customer_orders": "top_customers",
        "sales_by_status": "orders_by_status",
    }
    actual_name = alias_map.get(name, name)
    if actual_name not in REPORTS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown aggregation: {name}. Available: {list(REPORTS.keys())}",
        )

    return with_db(REPORTS[actual_name])


# ============================================================
# 6. Materialized Views
# ============================================================

@app.post("/refresh-mv")
def refresh_mv(mode: str = "incremental"):
    if mode not in {"full", "incremental"}:
        raise HTTPException(
            status_code=400,
            detail="mode must be full or incremental",
        )

    if mode == "full":
        return with_db(full_refresh)

    return with_db(incremental_refresh)


# ============================================================
# 7. Scheduled & Manual Jobs
# ============================================================

@app.get("/jobs")
def jobs():
    def read(db):
        records = list(
            db[settings.jobs]
            .find({}, {"_id": 0})
            .sort("started_at", -1)
            .limit(50)
        )
        return {
            "jobs": records,
            "scheduler": scheduler_status(),
        }

    return with_db(read)


@app.post("/jobs/{name}/run")
def run_job(name: str):
    if name not in JOBS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown job: {name}. Available: {list(JOBS.keys())}",
        )

    return JOBS[name]()


# ============================================================
# 8. Explain executionStats Benchmarks
# ============================================================

@app.get("/explain")
def explain():
    """
    Runs explain('executionStats') for 3 queries before and after indexes.
    Shows the reason and impact of each index.
    """
    return with_db(run_explain_benchmarks)