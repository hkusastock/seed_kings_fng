#!/usr/bin/env python3

import csv
import io
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/whit3rabbit/fear-greed-data/main/fear-greed.csv"

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "CNN_FGI.csv"


def fetch_csv_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 TradingView-PineSeeds-FGI-Updater"
        },
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def find_column(fieldnames, candidates):
    normalized = {
        name.strip().lower().replace("_", " ").replace("-", " "): name
        for name in fieldnames
    }

    for candidate in candidates:
        key = candidate.strip().lower().replace("_", " ").replace("-", " ")
        if key in normalized:
            return normalized[key]

    return None


def parse_date(value: str) -> str:
    value = value.strip()

    possible_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]

    for fmt in possible_formats:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%Y%m%dT")
        except ValueError:
            pass

    raise ValueError(f"Unsupported date format: {value}")


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    raw_text = fetch_csv_text(SOURCE_URL)
    reader = csv.DictReader(io.StringIO(raw_text))

    if not reader.fieldnames:
        raise RuntimeError("Source CSV has no header.")

    date_col = find_column(reader.fieldnames, ["date"])
    score_col = find_column(
        reader.fieldnames,
        [
            "fear greed",
            "fear greed index",
            "fear_greed",
            "fear_greed_index",
            "value",
            "score",
            "index",
        ],
    )

    if not date_col:
        raise RuntimeError(f"Cannot find date column. Columns: {reader.fieldnames}")

    if not score_col:
        raise RuntimeError(f"Cannot find score column. Columns: {reader.fieldnames}")

    rows = []
    seen_dates = set()

    for row in reader:
        try:
            date_tv = parse_date(row[date_col])
            score = float(str(row[score_col]).strip())
        except Exception as exc:
            print(f"Skipping bad row: {row} error={exc}", file=sys.stderr)
            continue

        if score < 0 or score > 100:
            print(f"Skipping out-of-range score: {date_tv} {score}", file=sys.stderr)
            continue

        if date_tv in seen_dates:
            raise RuntimeError(f"Duplicate date found: {date_tv}")

        seen_dates.add(date_tv)

        # TradingView Pine Seeds OHLCV format:
        # date, open, high, low, close, volume
        rows.append((date_tv, score, score, score, score, 0))

    rows.sort(key=lambda x: x[0])

    if len(rows) < 3000:
        raise RuntimeError(
            f"Too few rows: {len(rows)}. Source may be broken or columns changed."
        )

    with OUTPUT_FILE.open("w", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    print(f"Wrote {len(rows)} rows to {OUTPUT_FILE}")
    print(f"First date: {rows[0][0]}")
    print(f"Last date: {rows[-1][0]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
