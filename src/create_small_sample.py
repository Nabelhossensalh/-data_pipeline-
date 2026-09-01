"""Create a bounded CSV sample without loading the source file into memory."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from file_router import detect_delimiter


def create_sample(source_file: str | Path, output_file: str | Path, rows: int) -> int:
    if rows <= 0:
        raise ValueError("rows must be positive")
    source = Path(source_file)
    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with source.open("r", encoding="utf-8-sig", newline="") as source_handle, output.open("w", encoding="utf-8", newline="") as output_handle:
        reader = csv.reader(source_handle, delimiter=detect_delimiter(source))
        writer = csv.writer(output_handle)
        header = next(reader, None)
        if header is None:
            raise ValueError("source CSV has no header")
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)
            count += 1
            if count >= rows:
                break
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a bounded CSV sample")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/orders_small_sample.csv")
    parser.add_argument("--rows", type=int, default=100000)
    args = parser.parse_args()
    print(f"sample_rows={create_sample(args.input, args.output, args.rows)}")


if __name__ == "__main__":
    main()
