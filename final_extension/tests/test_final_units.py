# pyrefly: ignore [missing-import]
from final.materialized_views import _delivered_part, _product_parts
# pyrefly: ignore [missing-import]
from final.materialized_views import (
    _document_updated_at,
    _incremental_query,
    _resolve_watermark,
    incremental_refresh,
)
# pyrefly: ignore [missing-import]
from final.reports import REPORTS
# pyrefly: ignore [missing-import]
from final.explain import _sample_query
# pyrefly: ignore [missing-import]
from final.jobs import JOBS
from final.jobs import _run
# pyrefly: ignore [missing-import]
from final import api as api_module
from final.api import app, QUERY_SPECS


def test_five_reports_exist():
    assert len(REPORTS) == 5
    expected = {"sales_by_city", "top_products", "sales_by_period", "top_customers", "orders_by_status"}
    assert set(REPORTS.keys()) == expected


def test_city_contribution_matches_project_schema():
    part = _delivered_part({
        "status": "تم التسليم",
        "total_amount": 125.5,
        "customer": {"address": {"city": "صنعاء"}},
    })
    assert part == {"city": "صنعاء", "total_sales": 125.5, "orders_count": 1}


def test_non_delivered_order_has_no_contribution():
    assert _delivered_part({"status": "ملغي", "total_amount": 10, "customer": {"address": {"city": "صنعاء"}}}) is None


def test_product_contribution_uses_nested_items():
    parts = _product_parts({
        "status": "تم التسليم",
        "items": [{"sku": "SKU-1", "name": "منتج", "qty": 2, "total": 50}],
    })
    assert parts == [{"sku": "SKU-1", "name": "منتج", "units": 2, "sales": 50.0}]


def test_product_contribution_json_string():
    parts = _product_parts({
        "status": "تم التسليم",
        "items": '[{"sku": "SKU-2", "name": "هاتف", "qty": 1, "total": 200.0}]',
    })
    assert len(parts) == 1
    assert parts[0]["sku"] == "SKU-2"
    assert parts[0]["sales"] == 200.0


def test_jobs_registry_contains_required_jobs():
    assert "incremental" in JOBS
    assert "full_refresh" in JOBS
    assert "reports" in JOBS


def test_job_logs_application_error_as_failed():
    class JobCollection:
        def insert_one(self, record):
            self.record = record

    class Database:
        def __init__(self):
            self.jobs = JobCollection()

        def __getitem__(self, collection_name):
            assert collection_name == "job_runs"
            return self.jobs

    database = Database()
    result = _run(
        database,
        "incremental",
        lambda _: {"status": "error", "message": "views are not initialized"},
    )

    assert result["status"] == "failed"
    assert result["started_at"] <= result["finished_at"]
    assert result["error"]["type"] == "JobResultError"
    assert database.jobs.record == result


def test_five_queries_configured():
    assert len(QUERY_SPECS) == 5
    expected_queries = {"orders_by_city", "quarantine_by_error", "corrected_orders", "customer_orders", "recent_orders"}
    assert set(QUERY_SPECS.keys()) == expected_queries


def test_api_routes_contain_all_required_endpoints():
    routes = {r.path for r in app.routes}
    assert "/health" in routes
    assert "/ingest" in routes
    assert "/indexes" in routes
    assert "/queries" in routes
    assert "/queries/{name}" in routes
    assert "/aggregations" in routes
    assert "/aggregations/{name}" in routes
    assert "/refresh-mv" in routes
    assert "/jobs" in routes
    assert "/jobs/{name}/run" in routes
    assert "/explain" in routes


def test_incremental_refresh_supports_midterm_processed_at():
    from datetime import datetime, timezone

    watermark = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert _document_updated_at({"processed_at": watermark}) == watermark
    assert _incremental_query(watermark) == {
        "$or": [
            {"mv_updated_at": {"$gt": watermark}},
            {"processed_at": {"$gt": watermark}},
        ]
    }

    newer = datetime(2026, 1, 2, tzinfo=timezone.utc)
    assert _document_updated_at({"mv_updated_at": watermark, "processed_at": newer}) == newer
    assert _resolve_watermark(None, watermark) == watermark
    assert _resolve_watermark(newer, watermark) == newer
    assert _resolve_watermark(None, None) is not None


def test_incremental_refresh_migrates_null_watermark_without_full_scan(monkeypatch):
    from datetime import datetime, timezone
    from types import SimpleNamespace

    from final import materialized_views

    refresh_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    calls = {}

    class Cursor:
        def sort(self, *args):
            return self

        def __iter__(self):
            return iter(())

    class SourceCollection:
        def find(self, query):
            calls["query"] = query
            return Cursor()

    class StateCollection:
        def find_one(self, query):
            return {"_id": "mv_incremental_all", "watermark": None, "updated_at": refresh_time}

        def update_one(self, query, update):
            calls["watermark_update"] = update["$set"]["watermark"]

        def replace_one(self, query, replacement, upsert):
            calls["state_replacement"] = replacement

    class Database:
        def __getitem__(self, collection_name):
            return {"source": SourceCollection(), "state": StateCollection()}[collection_name]

    monkeypatch.setattr(
        materialized_views,
        "settings",
        SimpleNamespace(source_collection="source", state="state"),
    )
    result = incremental_refresh(Database())

    assert calls["watermark_update"] == refresh_time
    assert calls["query"] == _incremental_query(refresh_time)
    assert result["processed_documents"] == 0


def test_ingest_invokes_existing_midterm_pipeline(tmp_path, monkeypatch):
    import json
    from types import SimpleNamespace

    source_file = tmp_path / "incoming.csv"
    source_file.write_text("order_id\nA-1\n", encoding="utf-8")
    pipeline_script = tmp_path / "midterm" / "src" / "main.py"
    pipeline_script.parent.mkdir(parents=True)
    pipeline_script.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        api_module,
        "settings",
        SimpleNamespace(
            midterm_main_script=pipeline_script,
            mongo_uri="mongodb://localhost:27017",
            database="ecommerce_store",
        ),
    )
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout=json.dumps({"step": "all"}), stderr="")

    monkeypatch.setattr(api_module.subprocess, "run", fake_run)
    result = api_module.ingest(api_module.IngestRequest(source_file=str(source_file)))

    assert result["pipeline"] == "midterm_pipeline"
    assert result["result"] == {"step": "all"}
    assert "--step" in captured["command"]
    assert captured["command"][captured["command"].index("--step") + 1] == "all"
    assert "--storage-backend" in captured["command"]
    assert captured["command"][captured["command"].index("--storage-backend") + 1] == "mongo"


def test_explain_query_uses_values_from_current_data():
    class SampleCollection:
        def find_one(self, query, projection):
            assert query == {
                "customer.address.city": {"$exists": True, "$ne": None}
            }
            return {"customer": {"address": {"city": "مدينة الاختبار"}}}

    assert _sample_query(SampleCollection(), "customer.address.city") == {
        "customer.address.city": "مدينة الاختبار"
    }
