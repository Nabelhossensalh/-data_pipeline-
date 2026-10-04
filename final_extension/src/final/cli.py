from __future__ import annotations

import argparse
import json

from .db import get_client, get_db, ensure_indexes
from .explain import run_explain_benchmarks
from .jobs import JOBS
from .reports import REPORTS


def main():
    parser = argparse.ArgumentParser(description="Final project reports, materialized views and explain")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("indexes")
    report = sub.add_parser("report")
    report.add_argument("name", choices=sorted(REPORTS))
    sub.add_parser("refresh-full")
    sub.add_parser("refresh-incremental")
    sub.add_parser("explain")

    args = parser.parse_args()
    client = get_client()
    try:
        db = get_db(client)
        if args.command == "indexes":
            out = {"status": "ok", "indexes": ensure_indexes(db)}
        elif args.command == "report":
            out = REPORTS[args.name](db)
        elif args.command == "refresh-full":
            out = JOBS["full_refresh"]()
        elif args.command == "refresh-incremental":
            out = JOBS["incremental"]()
        elif args.command == "explain":
            out = run_explain_benchmarks(db)
        else:
            out = {"error": f"Unknown command: {args.command}"}
        print(json.dumps(out, ensure_ascii=False, default=str, indent=2))
    finally:
        client.close()


if __name__ == "__main__":
    main()
