from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

PRICE_PATTERN = re.compile(r"^\s*([+-]?[\d.,]+)\s*([$€])\s*$")


def parse_price(value: object) -> tuple[float | None, str | None]:
    if pd.isna(value):
        return None, None

    match = PRICE_PATTERN.match(str(value))
    if not match:
        return None, None

    number, symbol = match.groups()
    currency = "USD" if symbol == "$" else "EUR"

    if currency == "USD":
        normalized = number.replace(",", "")
    elif "," in number:
        normalized = number.replace(".", "").replace(",", ".")
    else:
        normalized = number

    try:
        return float(normalized), currency
    except ValueError:
        return None, currency


def clean_transactions(data: pd.DataFrame, usd_to_eur: float) -> pd.DataFrame:
    if usd_to_eur <= 0:
        raise ValueError("usd_to_eur must be positive")
    if not {"id", "price"}.issubset(data.columns):
        raise ValueError("Input must contain id and price columns")

    parsed = data["price"].apply(parse_price)
    result = data.copy()
    result[["price_value", "currency"]] = pd.DataFrame(parsed.tolist(), index=data.index)

    eur_to_usd = 1 / usd_to_eur
    result["price_usd"] = result.apply(
        lambda row: (
            row["price_value"]
            if row["currency"] == "USD"
            else row["price_value"] * eur_to_usd
            if row["currency"] == "EUR" and pd.notna(row["price_value"])
            else None
        ),
        axis=1,
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean USD/EUR transaction prices.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/generated"))
    parser.add_argument("--usd-to-eur", type=float, default=0.87)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = pd.read_csv(args.input_csv, keep_default_na=False)
    cleaned = clean_transactions(data, args.usd_to_eur)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(args.output_dir / "cleaned_transactions.csv", index=False)

    revenue = (
        cleaned.dropna(subset=["currency", "price_value"])
        .groupby("currency", as_index=False)["price_value"]
        .sum()
        .rename(columns={"price_value": "revenue"})
    )
    revenue.to_csv(args.output_dir / "revenue_by_currency.csv", index=False)

    summary = {
        "usd_to_eur": args.usd_to_eur,
        "total_revenue_usd": round(float(cleaned["price_usd"].sum()), 2),
        "invalid_or_missing_rows": int(cleaned["price_value"].isna().sum()),
        "total_rows": int(len(cleaned)),
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
