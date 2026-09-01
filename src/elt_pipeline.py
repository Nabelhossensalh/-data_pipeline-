# """Self-contained Python Batch ELT implementation for the required structure."""

# from __future__ import annotations

# import csv
# import json
# import tempfile
# import uuid
# from collections import Counter
# from copy import deepcopy
# from pathlib import Path
# from typing import Any, Iterable

# from file_router import detect_delimiter
# from metrics import RunMetrics, write_results
# from quality_rules import canonicalize_raw_fields, classify_raw_without_cleaning


# class JsonStore:
#     """Deterministic local store used when MongoDB is not selected."""

#     def __init__(self, path: str | Path = "data/local_store.json") -> None:
#         self.path = Path(path)
#         self.path.parent.mkdir(parents=True, exist_ok=True)
#         if self.path.exists():
#             self.data = json.loads(self.path.read_text(encoding="utf-8"))
#         else:
#             self.data = {"orders_raw": [], "orders_validated": [], "orders_quarantine": []}

#     def _save(self) -> None:
#         self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")

#     def create_indexes(self) -> None:
#         return None

#     def create_training_schema(self) -> None:
#         return None

#     def insert_raw(self, documents: list[dict[str, Any]]) -> None:
#         self.data.setdefault("orders_raw", []).extend(deepcopy(documents))
#         self._save()

#     def _upsert(self, collection: str, key_fields: tuple[str, ...], document: dict[str, Any]) -> str:
#         rows = self.data.setdefault(collection, [])
#         for index, existing in enumerate(rows):
#             if all(existing.get(field) == document.get(field) for field in key_fields):
#                 if existing == document:
#                     return "unchanged"
#                 rows[index] = deepcopy(document)
#                 self._save()
#                 return "updated"
#         rows.append(deepcopy(document))
#         self._save()
#         return "inserted"

#     def upsert_validated(self, document: dict[str, Any]) -> str:
#         self.remove_quarantine(document)
#         return self._upsert("orders_validated", ("order_id",), document)

#     def upsert_quarantine(self, document: dict[str, Any]) -> str:
#         if document.get("order_id"):
#             self.remove_validated(document)
#         return self._upsert("orders_quarantine", ("run_id", "source_row_number"), document)

#     def remove_quarantine(self, document: dict[str, Any]) -> None:
#         rows = self.data.setdefault("orders_quarantine", [])
#         self.data["orders_quarantine"] = [
#             row for row in rows
#             if not (row.get("run_id") == document.get("run_id") and row.get("source_row_number") == document.get("source_row_number"))
#         ]
#         self._save()

#     def remove_validated(self, document: dict[str, Any]) -> None:
#         order_id = document.get("order_id")
#         self.data["orders_validated"] = [row for row in self.data.setdefault("orders_validated", []) if row.get("order_id") != order_id]
#         self._save()

#     def close(self) -> None:
#         self._save()


# def _raw_document(row: dict[str, Any], source_file: Path, run_id: str, row_number: int, engine: str) -> dict[str, Any]:
#     return {
#         **row,
#         "run_id": run_id,
#         "source_file": str(source_file.resolve()),
#         "source_row_number": row_number,
#         "engine_used": engine,
#         "raw_payload": json.dumps(row, ensure_ascii=False, default=str),
#     }


# def load_csv_streaming(
#     source_file: str | Path,
#     store: JsonStore,
#     *,
#     engine: str = "python_batch",
#     batch_size: int = 500,
#     run_id: str | None = None,
#     reports_dir: str | Path = "reports",
# ) -> dict[str, Any]:
#     """Run Raw-first ELT with bounded memory and disk-backed replay passes."""
#     import sqlite3

#     path = Path(source_file)
#     if batch_size <= 0:
#         raise ValueError("batch_size must be positive")
#     run_id = run_id or str(uuid.uuid4())
#     metrics = RunMetrics(run_id, "python_batch")
#     temp_jsonl = tempfile.NamedTemporaryFile(prefix="midterm_raw_", suffix=".jsonl", delete=False, mode="w", encoding="utf-8")
#     temp_db = tempfile.NamedTemporaryFile(prefix="midterm_ids_", suffix=".sqlite", delete=False)
#     temp_jsonl_path = Path(temp_jsonl.name)
#     temp_db_path = Path(temp_db.name)
#     temp_db.close()
#     id_db = sqlite3.connect(temp_db_path)
#     id_db.execute("CREATE TABLE ids (order_id TEXT PRIMARY KEY, count INTEGER NOT NULL)")
#     id_db.commit()

#     def iter_raw() -> Iterable[dict[str, Any]]:
#         with temp_jsonl_path.open("r", encoding="utf-8") as replay:
#             for line in replay:
#                 if line.strip():
#                     yield json.loads(line)

#     def is_duplicate(order_id: Any) -> bool:
#         value = str(order_id).strip() if order_id not in (None, "") else ""
#         if not value:
#             return False
#         row = id_db.execute("SELECT count FROM ids WHERE order_id = ?", (value,)).fetchone()
#         return bool(row and row[0] > 1)

#     try:
#         delimiter = detect_delimiter(path)
#         raw_buffer: list[dict[str, Any]] = []
#         with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
#             for row_number, row in enumerate(csv.DictReader(handle, delimiter=delimiter), start=2):
#                 raw = _raw_document(row, path, run_id, row_number, engine)
#                 temp_jsonl.write(json.dumps(raw, ensure_ascii=False, default=str) + "\n")
#                 raw_buffer.append(raw)
#                 canonical_row = canonicalize_raw_fields(row)
#                 order_id = str(canonical_row.get("order_id", "")).strip()
#                 if order_id:
#                     id_db.execute("INSERT INTO ids(order_id, count) VALUES (?, 1) ON CONFLICT(order_id) DO UPDATE SET count = count + 1", (order_id,))
#                 if len(raw_buffer) >= batch_size:
#                     store.insert_raw(raw_buffer)
#                     metrics.raw_loaded += len(raw_buffer)
#                     raw_buffer = []
#                     id_db.commit()
#         if raw_buffer:
#             store.insert_raw(raw_buffer)
#             metrics.raw_loaded += len(raw_buffer)
#         temp_jsonl.flush()
#         temp_jsonl.close()
#         id_db.commit()

#         # Pass 1: raw-valid records are written before any cleaning.
#         for raw in iter_raw():
#             item = classify_raw_without_cleaning(raw, is_duplicate(raw.get("order_id")))
#             if not item["raw_valid"]:
#                 continue
#             metrics.raw_valid_count += 1
#             metrics.initial_valid_count += 1
#             metrics.valid_count += 1
#             outcome = store.upsert_validated(item["validated_document"])
#             setattr(metrics, f"{outcome}_count", getattr(metrics, f"{outcome}_count") + 1)

#         # Pass 2: raw-invalid records are written to Quarantine without cleaning.
#         for raw in iter_raw():
#             item = classify_raw_without_cleaning(raw, is_duplicate(raw.get("order_id")))
#             if not item["raw_invalid"]:
#                 continue
#             metrics.raw_invalid_count += 1
#             metrics.initial_invalid_count += 1
#             metrics.quarantine_count += 1
#             final = item["quarantine_document"]
#             for code in final.get("error_codes", []):
#                 metrics.add_error(code)
#             outcome = store.upsert_quarantine(final)
#             setattr(metrics, f"{outcome}_count", getattr(metrics, f"{outcome}_count") + 1)
#         result = metrics.finish()
#         result.update({"engine_used": engine, "source_file": str(path.resolve()), "classification_order": "raw_validated_before_raw_quarantine", "cleaning_applied": False, "next_stage": "cleaning_after_raw_classification", "streaming_batch_size": batch_size, "memory_bounded": True})
#         write_results(result, reports_dir)
#         return result
#     finally:
#         try:
#             temp_jsonl.close()
#         except Exception:
#             pass
#         id_db.close()
#         temp_jsonl_path.unlink(missing_ok=True)
#         temp_db_path.unlink(missing_ok=True)


# __all__ = ["JsonStore", "load_csv_streaming"]



# def _quarantine_original_document(document: dict[str, Any]) -> dict[str, Any]:
#     """Rebuild the original raw row stored inside a quarantine document."""
#     original = deepcopy(document.get("original_document") or {})
#     for field in ("run_id", "source_file", "source_row_number", "engine_used", "raw_payload"):
#         if field not in original and document.get(field) is not None:
#             original[field] = document.get(field)
#     return original


# def clean_after_raw_batch(store: Any, run_id: str, *, reports_dir: str | Path = "reports", raw_valid_count: int | None = None, raw_invalid_count: int | None = None) -> dict[str, Any]:
#     """Clean only rows already quarantined by the raw-only classification stage."""
#     from quality_rules import classify_raw_document

#     if hasattr(store, "data"):
#         quarantine_rows = [row for row in store.data.get("orders_quarantine", []) if row.get("run_id") == run_id]
#     else:
#         quarantine_rows = list(store.quarantine.find({"run_id": run_id}))

#     first_pass_valid = int(raw_valid_count or 0)
#     first_pass_invalid = int(raw_invalid_count or len(quarantine_rows))
#     metrics = RunMetrics(run_id, "python_batch_cleaning")
#     metrics.raw_loaded = first_pass_valid + first_pass_invalid
#     metrics.raw_valid_count = first_pass_valid
#     metrics.raw_invalid_count = first_pass_invalid
#     metrics.initial_valid_count = first_pass_valid
#     metrics.initial_invalid_count = first_pass_invalid
#     # Raw-valid documents were already accepted before this stage and remain valid.
#     metrics.valid_count = first_pass_valid

#     for quarantined in quarantine_rows:
#         raw = _quarantine_original_document(quarantined)
#         is_duplicate = "DUPLICATE_ORDER_ID" in set(quarantined.get("error_codes", []))
#         item = classify_raw_document(raw, is_duplicate=is_duplicate)
#         final = item["final_document"]
#         final["initial_classification"] = "invalid"
#         final["initial_error_codes"] = list(quarantined.get("error_codes", []))
#         final["initial_error_details"] = deepcopy(quarantined.get("error_details", []))
#         final["raw_error_codes"] = list(quarantined.get("error_codes", []))
#         final["raw_error_details"] = deepcopy(quarantined.get("error_details", []))
#         final["cleaning_applied"] = True
#         final["raw_validation_only"] = False
#         final["validation_stages"] = ["raw_schema_validation", "raw_business_validation", "raw_duplicate_detection", "cleaning_last"]
#         if final.get("quality_status") in {"validated", "corrected"}:
#             if final.get("quality_status") == "validated":
#                 metrics.valid_count += 1
#             else:
#                 metrics.corrected_count += 1
#             outcome = store.upsert_validated(final)
#         else:
#             metrics.quarantine_count += 1
#             for code in final.get("error_codes", []):
#                 metrics.add_error(code)
#             outcome = store.upsert_quarantine(final)
#         setattr(metrics, f"{outcome}_count", getattr(metrics, f"{outcome}_count") + 1)

#     result = metrics.finish()
#     result.update({
#         "cleaning_applied": True,
#         "cleaning_input": "orders_quarantine_only",
#         "cleaned_quarantine_count": len(quarantine_rows),
#         "classification_order": "raw_validated_and_raw_quarantined_then_clean_quarantine",
#         "next_stage": "metrics",
#     })
#     write_results(result, reports_dir)
#     return result






"""
Self-contained Python Batch ELT implementation.

Pipeline design:

    Source CSV
        |
        v
    Raw Load
        |
        v
    Raw Classification
       / \
      /   \
   VALID INVALID
    |       |
    v       v
validated quarantine
            |
            v
        Cleaning
            |
       /          \
   validated    quarantine

IMPORTANT:
- One pipeline execution MUST use exactly one run_id.
- run_id is created by the pipeline/main layer.
- load_csv_streaming() NEVER creates a new run_id.
- The same run_id must be used by Raw Load, Quality and Cleaning.
"""

from __future__ import annotations

import csv
import json
import sqlite3
import tempfile
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

from file_router import detect_delimiter
from metrics import RunMetrics, write_results
from quality_rules import (
    canonicalize_raw_fields,
    classify_raw_without_cleaning,
)


# ============================================================
# JsonStore
# ============================================================


class JsonStore:
    """
    Deterministic local store used when MongoDB is not selected.

    Collections:
        orders_raw
        orders_validated
        orders_quarantine
    """

    def __init__(
        self,
        path: str | Path = "data/local_store.json",
    ) -> None:

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.path.exists():
            self.data = json.loads(
                self.path.read_text(
                    encoding="utf-8"
                )
            )
        else:
            self.data = {
                "orders_raw": [],
                "orders_validated": [],
                "orders_quarantine": [],
            }

    # --------------------------------------------------------
    # Internal save
    # --------------------------------------------------------

    def _save(self) -> None:

        self.path.write_text(
            json.dumps(
                self.data,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
            + "\n",
            encoding="utf-8",
        )

    # --------------------------------------------------------
    # Compatibility methods
    # --------------------------------------------------------

    def create_indexes(self) -> None:
        return None

    def create_training_schema(self) -> None:
        return None

    # --------------------------------------------------------
    # Raw
    # --------------------------------------------------------

    def insert_raw(
        self,
        documents: list[dict[str, Any]],
    ) -> None:

        if not documents:
            return

        self.data.setdefault(
            "orders_raw",
            [],
        ).extend(
            deepcopy(documents)
        )

        self._save()

    # --------------------------------------------------------
    # Generic upsert
    # --------------------------------------------------------

    def _upsert(
        self,
        collection: str,
        key_fields: tuple[str, ...],
        document: dict[str, Any],
    ) -> str:

        rows = self.data.setdefault(
            collection,
            [],
        )

        for index, existing in enumerate(rows):

            same_key = all(
                existing.get(field)
                == document.get(field)
                for field in key_fields
            )

            if not same_key:
                continue

            if existing == document:
                return "unchanged"

            rows[index] = deepcopy(
                document
            )

            self._save()

            return "updated"

        rows.append(
            deepcopy(document)
        )

        self._save()

        return "inserted"

    # --------------------------------------------------------
    # Validated
    # --------------------------------------------------------

    def upsert_validated(
        self,
        document: dict[str, Any],
    ) -> str:

        self.remove_quarantine(
            document
        )

        return self._upsert(
            "orders_validated",
            ("order_id",),
            document,
        )

    # --------------------------------------------------------
    # Quarantine
    # --------------------------------------------------------

    def upsert_quarantine(
        self,
        document: dict[str, Any],
    ) -> str:

        if document.get("order_id"):
            self.remove_validated(
                document
            )

        return self._upsert(
            "orders_quarantine",
            (
                "run_id",
                "source_row_number",
            ),
            document,
        )

    # --------------------------------------------------------
    # Remove quarantine
    # --------------------------------------------------------

    def remove_quarantine(
        self,
        document: dict[str, Any],
    ) -> None:

        rows = self.data.setdefault(
            "orders_quarantine",
            [],
        )

        run_id = document.get(
            "run_id"
        )

        source_row_number = document.get(
            "source_row_number"
        )

        self.data["orders_quarantine"] = [
            row
            for row in rows
            if not (
                row.get("run_id") == run_id
                and row.get("source_row_number")
                == source_row_number
            )
        ]

        self._save()

    # --------------------------------------------------------
    # Remove validated
    # --------------------------------------------------------

    def remove_validated(
        self,
        document: dict[str, Any],
    ) -> None:

        order_id = document.get(
            "order_id"
        )

        rows = self.data.setdefault(
            "orders_validated",
            [],
        )

        self.data["orders_validated"] = [
            row
            for row in rows
            if row.get("order_id")
            != order_id
        ]

        self._save()

    # --------------------------------------------------------
    # Close
    # --------------------------------------------------------

    def close(self) -> None:
        self._save()


# ============================================================
# Raw document construction
# ============================================================


def _raw_document(
    row: dict[str, Any],
    source_file: Path,
    run_id: str,
    row_number: int,
    engine: str,
) -> dict[str, Any]:

    return {
        **row,

        # Pipeline identity
        "run_id": run_id,

        # Source lineage
        "source_file": str(
            source_file.resolve()
        ),

        "source_row_number": row_number,

        # Processing metadata
        "engine_used": engine,

        # Original payload
        "raw_payload": json.dumps(
            row,
            ensure_ascii=False,
            default=str,
        ),
    }


# ============================================================
# Run ID validation
# ============================================================


def _validate_run_id(
    run_id: str | None,
) -> str:

    if run_id is None:
        raise ValueError(
            "run_id is required. "
            "The pipeline must create one shared run_id "
            "and pass it to every stage."
        )

    run_id = str(run_id).strip()

    if not run_id:
        raise ValueError(
            "run_id cannot be empty."
        )

    return run_id


# ============================================================
# Raw Load + Raw Classification
# ============================================================


def load_csv_streaming(
    source_file: str | Path,
    store: JsonStore,
    *,
    engine: str = "python_batch",
    batch_size: int = 500,
    run_id: str,
    reports_dir: str | Path = "reports",
) -> dict[str, Any]:
    """
    Run Raw-first ELT with bounded memory and replay passes.

    IMPORTANT:
        run_id is mandatory.

    This function NEVER creates a new run_id.

    The caller must create the run_id once:

        run_id = existing_run_id or str(uuid.uuid4())

    and then pass it here.
    """

    path = Path(source_file)

    # --------------------------------------------------------
    # Validate arguments
    # --------------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Input path is not a file: {path}"
        )

    if batch_size <= 0:
        raise ValueError(
            "batch_size must be positive."
        )

    run_id = _validate_run_id(
        run_id
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    metrics = RunMetrics(
        run_id,
        "python_batch",
    )

    # --------------------------------------------------------
    # Temporary replay file
    # --------------------------------------------------------

    temp_jsonl = tempfile.NamedTemporaryFile(
        prefix="midterm_raw_",
        suffix=".jsonl",
        delete=False,
        mode="w",
        encoding="utf-8",
    )

    temp_jsonl_path = Path(
        temp_jsonl.name
    )

    # --------------------------------------------------------
    # Temporary duplicate index
    # --------------------------------------------------------

    temp_db = tempfile.NamedTemporaryFile(
        prefix="midterm_ids_",
        suffix=".sqlite",
        delete=False,
    )

    temp_db_path = Path(
        temp_db.name
    )

    temp_db.close()

    id_db = sqlite3.connect(
        temp_db_path
    )

    id_db.execute(
        """
        CREATE TABLE ids (
            order_id TEXT PRIMARY KEY,
            count INTEGER NOT NULL
        )
        """
    )

    id_db.commit()

    # --------------------------------------------------------
    # Replay iterator
    # --------------------------------------------------------

    def iter_raw() -> Iterable[
        dict[str, Any]
    ]:

        with temp_jsonl_path.open(
            "r",
            encoding="utf-8",
        ) as replay:

            for line in replay:

                if not line.strip():
                    continue

                yield json.loads(
                    line
                )

    # --------------------------------------------------------
    # Duplicate detection
    # --------------------------------------------------------

    def is_duplicate(
        order_id: Any,
    ) -> bool:

        value = (
            str(order_id).strip()
            if order_id not in (None, "")
            else ""
        )

        if not value:
            return False

        row = id_db.execute(
            """
            SELECT count
            FROM ids
            WHERE order_id = ?
            """,
            (value,),
        ).fetchone()

        return bool(
            row
            and row[0] > 1
        )

    # --------------------------------------------------------
    # Main processing
    # --------------------------------------------------------

    try:

        # ====================================================
        # Stage 1 — Discover delimiter
        # ====================================================

        delimiter = detect_delimiter(
            path
        )

        raw_buffer: list[
            dict[str, Any]
        ] = []

        # ====================================================
        # Stage 2 — Raw Load
        # ====================================================

        with path.open(
            "r",
            encoding="utf-8-sig",
            errors="replace",
            newline="",
        ) as handle:

            reader = csv.DictReader(
                handle,
                delimiter=delimiter,
            )

            for row_number, row in enumerate(
                reader,
                start=2,
            ):

                raw = _raw_document(
                    row=row,
                    source_file=path,
                    run_id=run_id,
                    row_number=row_number,
                    engine=engine,
                )

                # ------------------------------------------------
                # Replay copy
                # ------------------------------------------------

                temp_jsonl.write(
                    json.dumps(
                        raw,
                        ensure_ascii=False,
                        default=str,
                    )
                    + "\n"
                )

                # ------------------------------------------------
                # Memory-bounded buffer
                # ------------------------------------------------

                raw_buffer.append(
                    raw
                )

                # ------------------------------------------------
                # Duplicate index
                # ------------------------------------------------

                canonical_row = (
                    canonicalize_raw_fields(
                        row
                    )
                )

                order_id = str(
                    canonical_row.get(
                        "order_id",
                        "",
                    )
                ).strip()

                if order_id:

                    id_db.execute(
                        """
                        INSERT INTO ids(
                            order_id,
                            count
                        )
                        VALUES (?, 1)

                        ON CONFLICT(order_id)
                        DO UPDATE SET
                            count = count + 1
                        """,
                        (order_id,),
                    )

                # ------------------------------------------------
                # Batch write
                # ------------------------------------------------

                if len(raw_buffer) >= batch_size:

                    store.insert_raw(
                        raw_buffer
                    )

                    metrics.raw_loaded += (
                        len(raw_buffer)
                    )

                    raw_buffer = []

                    id_db.commit()

        # ====================================================
        # Remaining batch
        # ====================================================

        if raw_buffer:

            store.insert_raw(
                raw_buffer
            )

            metrics.raw_loaded += (
                len(raw_buffer)
            )

            raw_buffer = []

            id_db.commit()

        # ----------------------------------------------------
        # Flush replay file
        # ----------------------------------------------------

        temp_jsonl.flush()
        temp_jsonl.close()

        id_db.commit()

        # ====================================================
        # Safety check
        # ====================================================



        # ====================================================
        # Pass 1
        #
        # Raw-valid records are accepted BEFORE cleaning.
        # ====================================================

        for raw in iter_raw():

            duplicate = is_duplicate(
                raw.get("order_id")
            )

            item = (
                classify_raw_without_cleaning(
                    raw,
                    duplicate,
                )
            )

            if not item["raw_valid"]:
                continue

            metrics.raw_valid_count += 1
            metrics.initial_valid_count += 1
            metrics.valid_count += 1

            outcome = (
                store.upsert_validated(
                    item[
                        "validated_document"
                    ]
                )
            )

            setattr(
                metrics,
                f"{outcome}_count",
                getattr(
                    metrics,
                    f"{outcome}_count",
                )
                + 1,
            )

        # ====================================================
        # Pass 2
        #
        # Raw-invalid records go to quarantine.
        # NO cleaning is applied here.
        # ====================================================

        for raw in iter_raw():

            duplicate = is_duplicate(
                raw.get("order_id")
            )

            item = (
                classify_raw_without_cleaning(
                    raw,
                    duplicate,
                )
            )

            if not item["raw_invalid"]:
                continue

            metrics.raw_invalid_count += 1
            metrics.initial_invalid_count += 1
            metrics.quarantine_count += 1

            final = item[
                "quarantine_document"
            ]

            for code in final.get(
                "error_codes",
                [],
            ):

                metrics.add_error(
                    code
                )

            outcome = (
                store.upsert_quarantine(
                    final
                )
            )

            setattr(
                metrics,
                f"{outcome}_count",
                getattr(
                    metrics,
                    f"{outcome}_count",
                )
                + 1,
            )

        # ====================================================
        # Reconciliation
        # ====================================================

        classified_total = (
            metrics.raw_valid_count
            + metrics.raw_invalid_count
        )

        reconciliation_ok = (
            classified_total
            == metrics.raw_loaded
        )

        if not reconciliation_ok:

            raise RuntimeError(
                "Raw classification reconciliation failed: "
                f"raw_loaded={metrics.raw_loaded}, "
                f"raw_valid={metrics.raw_valid_count}, "
                f"raw_invalid={metrics.raw_invalid_count}, "
                f"classified_total={classified_total}"
            )

        # ====================================================
        # Finish metrics
        # ====================================================

        result = metrics.finish()

        result.update(
            {
                "engine_used": engine,
                "source_file": str(
                    path.resolve()
                ),

                # CRITICAL:
                # Same run_id must remain throughout pipeline.
                "run_id": run_id,

                "classification_order": (
                    "raw_validated_before_raw_quarantine"
                ),

                "cleaning_applied": False,

                "next_stage": (
                    "cleaning_after_raw_classification"
                ),

                "streaming_batch_size": batch_size,

                "memory_bounded": True,

                "reconciliation_ok": (
                    reconciliation_ok
                ),

                "classified_total": (
                    classified_total
                ),
            }
        )

        write_results(
            result,
            reports_dir,
        )

        return result

    finally:

        try:
            temp_jsonl.close()
        except Exception:
            pass

        try:
            id_db.close()
        except Exception:
            pass

        temp_jsonl_path.unlink(
            missing_ok=True
        )

        temp_db_path.unlink(
            missing_ok=True
        )


# ============================================================
# Reconstruct original document
# ============================================================


def _quarantine_original_document(
    document: dict[str, Any],
) -> dict[str, Any]:
    """
    Rebuild the original raw row stored inside
    a quarantine document.
    """

    original = deepcopy(
        document.get(
            "original_document"
        )
        or {}
    )

    metadata_fields = (
        "run_id",
        "source_file",
        "source_row_number",
        "engine_used",
        "raw_payload",
    )

    for field in metadata_fields:

        if (
            field not in original
            and document.get(field)
            is not None
        ):

            original[field] = (
                document.get(field)
            )

    return original


# ============================================================
# Cleaning
# ============================================================


def clean_after_raw_batch(
    store: Any,
    run_id: str,
    *,
    reports_dir: str | Path = "reports",
    raw_valid_count: int | None = None,
    raw_invalid_count: int | None = None,
) -> dict[str, Any]:
    """
    Clean ONLY rows that were classified as raw-invalid.

    Raw-valid rows have already been accepted and remain valid.

    Cleaning happens AFTER:
        raw schema validation
        raw business validation
        raw duplicate detection
    """

    from quality_rules import (
        classify_raw_document,
    )

    run_id = _validate_run_id(
        run_id
    )

    # ========================================================
    # Load quarantine rows
    # ========================================================

    if hasattr(store, "data"):

        quarantine_rows = [
            row
            for row in store.data.get(
                "orders_quarantine",
                [],
            )
            if row.get("run_id")
            == run_id
        ]

    else:

        quarantine_rows = list(
            store.quarantine.find(
                {
                    "run_id": run_id
                }
            )
        )

    # ========================================================
    # IMPORTANT FIX
    #
    # Do NOT use:
    #
    # raw_invalid_count or len(...)
    #
    # because zero is a valid value.
    # ========================================================

    if raw_valid_count is not None:

        first_pass_valid = int(
            raw_valid_count
        )

    else:

        first_pass_valid = 0

    if raw_invalid_count is not None:

        first_pass_invalid = int(
            raw_invalid_count
        )

    else:

        first_pass_invalid = len(
            quarantine_rows
        )

    # ========================================================
    # Metrics
    # ========================================================

    metrics = RunMetrics(
        run_id,
        "python_batch_cleaning",
    )

    metrics.raw_loaded = (
        first_pass_valid
        + first_pass_invalid
    )

    metrics.raw_valid_count = (
        first_pass_valid
    )

    metrics.raw_invalid_count = (
        first_pass_invalid
    )

    metrics.initial_valid_count = (
        first_pass_valid
    )

    metrics.initial_invalid_count = (
        first_pass_invalid
    )

    # Raw-valid documents were already accepted.
    metrics.valid_count = (
        first_pass_valid
    )

    # ========================================================
    # Clean quarantined records
    # ========================================================

    for quarantined in quarantine_rows:

        raw = (
            _quarantine_original_document(
                quarantined
            )
        )

        is_duplicate = (
            "DUPLICATE_ORDER_ID"
            in set(
                quarantined.get(
                    "error_codes",
                    [],
                )
            )
        )

        item = classify_raw_document(
            raw,
            is_duplicate=is_duplicate,
        )

        final = item[
            "final_document"
        ]

        # ----------------------------------------------------
        # Preserve first-pass classification
        # ----------------------------------------------------

        final[
            "initial_classification"
        ] = "invalid"

        final[
            "initial_error_codes"
        ] = list(
            quarantined.get(
                "error_codes",
                [],
            )
        )

        final[
            "initial_error_details"
        ] = deepcopy(
            quarantined.get(
                "error_details",
                [],
            )
        )

        final[
            "raw_error_codes"
        ] = list(
            quarantined.get(
                "error_codes",
                [],
            )
        )

        final[
            "raw_error_details"
        ] = deepcopy(
            quarantined.get(
                "error_details",
                [],
            )
        )

        # ----------------------------------------------------
        # Cleaning metadata
        # ----------------------------------------------------

        final[
            "cleaning_applied"
        ] = True

        final[
            "raw_validation_only"
        ] = False

        final[
            "validation_stages"
        ] = [
            "raw_schema_validation",
            "raw_business_validation",
            "raw_duplicate_detection",
            "cleaning_last",
        ]

        # Ensure pipeline identity survives cleaning.
        final["run_id"] = run_id

        # ====================================================
        # Final routing
        # ====================================================

        if final.get(
            "quality_status"
        ) in {
            "validated",
            "corrected",
        }:

            if (
                final.get(
                    "quality_status"
                )
                == "validated"
            ):

                metrics.valid_count += 1

            else:

                metrics.corrected_count += 1

            outcome = (
                store.upsert_validated(
                    final
                )
            )

        else:

            metrics.quarantine_count += 1

            for code in final.get(
                "error_codes",
                [],
            ):

                metrics.add_error(
                    code
                )

            outcome = (
                store.upsert_quarantine(
                    final
                )
            )

        setattr(
            metrics,
            f"{outcome}_count",
            getattr(
                metrics,
                f"{outcome}_count",
            )
            + 1,
        )

    # ========================================================
    # Reconciliation
    # ========================================================

    expected_input = (
        first_pass_valid
        + first_pass_invalid
    )

    if metrics.raw_loaded != expected_input:

        raise RuntimeError(
            "Cleaning input reconciliation failed: "
            f"raw_loaded={metrics.raw_loaded}, "
            f"expected={expected_input}"
        )

    # ========================================================
    # Finish
    # ========================================================

    result = metrics.finish()

    result.update(
        {
            "run_id": run_id,

            "cleaning_applied": True,

            "cleaning_input": (
                "orders_quarantine_only"
            ),

            "cleaned_quarantine_count": (
                len(quarantine_rows)
            ),

            "classification_order": (
                "raw_validated_and_raw_quarantined_then_clean_quarantine"
            ),

            "next_stage": "metrics",

            "reconciliation_ok": True,
        }
    )

    write_results(
        result,
        reports_dir,
    )

    return result


# ============================================================
# Public API
# ============================================================


__all__ = [
    "JsonStore",
    "load_csv_streaming",
    "clean_after_raw_batch",
]