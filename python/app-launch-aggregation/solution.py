from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"user_id", "session_id", "platform", "source", "region"}


def build_reports(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns: {missing_list}")

    source_platform = (
        data.groupby(["platform", "source"], dropna=False)
        .agg(
            unique_users=("user_id", "nunique"),
            sessions=("session_id", "nunique"),
        )
        .reset_index()
        .sort_values(
            by=["platform", "unique_users", "sessions", "source"],
            ascending=[True, False, False, True],
        )
    )

    city_users = (
        data.groupby("region", dropna=False)
        .agg(unique_users=("user_id", "nunique"))
        .reset_index()
        .rename(columns={"region": "city"})
        .sort_values(by=["unique_users", "city"], ascending=[False, True])
    )

    return source_platform, city_users


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build app-launch aggregation reports.")
    parser.add_argument("input_csv", type=Path, help="Input CSV file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/generated"),
        help="Directory for generated CSV reports",
    )
    parser.add_argument("--separator", default=",", help="Input CSV separator")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input_csv.exists():
        raise FileNotFoundError(f"Input file not found: {args.input_csv}")

    data = pd.read_csv(args.input_csv, sep=args.separator)
    source_platform, city_users = build_reports(data)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_platform.to_csv(
        args.output_dir / "source_platform_stats.csv",
        index=False,
        encoding="utf-8-sig",
    )
    city_users.to_csv(
        args.output_dir / "city_users_stats.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print(f"Saved reports to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
