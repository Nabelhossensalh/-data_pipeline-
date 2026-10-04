from __future__ import annotations

from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler

from .config import settings
from .db import get_client, get_db, utcnow
from .materialized_views import incremental_refresh, full_refresh


# ============================================================
# Job Logging
# ============================================================

def _run(
    db,
    name: str,
    fn,
) -> dict[str, Any]:

    started = utcnow()

    record: dict[str, Any] = {
        "job_name": name,
        "started_at": started,
    }

    try:
        result = fn(db)
        failed_result = isinstance(result, dict) and result.get("status") in {"error", "failed"}

        record.update(
            {
                "finished_at": utcnow(),
                "status": "failed" if failed_result else "success",
                "result": result,
                "error": (
                    {
                        "type": "JobResultError",
                        "message": result.get("message", "Job returned a failure status"),
                    }
                    if failed_result
                    else None
                ),
            }
        )

    except Exception as exc:

        record.update(
            {
                "finished_at": utcnow(),
                "status": "failed",
                "result": None,
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
            }
        )

        db[settings.jobs].insert_one(record)

        raise

    db[settings.jobs].insert_one(record)

    return record


# ============================================================
# Incremental Materialized View Job
# ============================================================

def run_incremental() -> dict[str, Any]:

    client = get_client()

    try:
        db = get_db(client)

        return _run(
            db,
            "refresh_materialized_views_incremental",
            incremental_refresh,
        )

    finally:
        client.close()


# ============================================================
# Full Materialized View Refresh Job
# ============================================================

def run_full_refresh() -> dict[str, Any]:

    client = get_client()

    try:
        db = get_db(client)

        return _run(
            db,
            "refresh_materialized_views_full",
            full_refresh,
        )

    finally:
        client.close()


# ============================================================
# Aggregation Report Job
# ============================================================

def run_reports() -> dict[str, Any]:

    from .reports import REPORTS

    client = get_client()

    try:
        db = get_db(client)

        def execute_reports(database):
            results = {}
            for name, report_function in REPORTS.items():
                results[name] = report_function(database)
            return {
                "reports": results,
                "count": len(results),
            }

        return _run(
            db,
            "refresh_aggregation_reports",
            execute_reports,
        )

    finally:
        client.close()


# ============================================================
# Manual Jobs Registry
# ============================================================

JOBS = {
    "incremental": run_incremental,
    "full_refresh": run_full_refresh,
    "reports": run_reports,
}


# ============================================================
# Fixed Scheduler
# ============================================================

_scheduler: BackgroundScheduler | None = None


def start_scheduler() -> BackgroundScheduler:
    """
    Start the fixed scheduled jobs.

    Job 1:
        Incremental Materialized View refresh every N minutes.

    Job 2:
        Aggregation reports refresh every N minutes.
    """

    global _scheduler

    if _scheduler is not None and _scheduler.running:
        return _scheduler

    scheduler = BackgroundScheduler(timezone="UTC")

    # Job 1: Incremental MV Refresh
    scheduler.add_job(
        run_incremental,
        trigger="interval",
        minutes=settings.incremental_schedule_minutes,
        id="incremental_mv_refresh",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    # Job 2: Aggregation Reports
    scheduler.add_job(
        run_reports,
        trigger="interval",
        minutes=settings.report_schedule_minutes,
        id="aggregation_reports_refresh",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    _scheduler = scheduler

    return scheduler


def stop_scheduler() -> None:
    """
    Stop the scheduler safely.
    """

    global _scheduler

    if _scheduler is not None:
        if _scheduler.running:
            _scheduler.shutdown(wait=False)
        _scheduler = None


def scheduler_status() -> dict[str, Any]:

    if _scheduler is None:
        return {
            "running": False,
            "jobs": [],
        }

    return {
        "running": _scheduler.running,
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run_time": (
                    job.next_run_time.isoformat()
                    if job.next_run_time
                    else None
                ),
            }
            for job in _scheduler.get_jobs()
        ],
    }