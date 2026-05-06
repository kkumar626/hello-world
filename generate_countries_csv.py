# Usage:
#   python3 generate_countries_csv.py                   -> countries.csv (default)
#   python3 generate_countries_csv.py --format json     -> countries.json
#   python3 generate_countries_csv.py --format markdown -> countries.md

import csv
import json
import argparse

COUNTRIES = [
    {"Country": "United States", "Capital": "Washington, D.C.", "Currency": "USD", "Language": "English"},
    {"Country": "France", "Capital": "Paris", "Currency": "EUR", "Language": "French"},
    {"Country": "Japan", "Capital": "Tokyo", "Currency": "JPY", "Language": "Japanese"},
    {"Country": "Germany", "Capital": "Berlin", "Currency": "EUR", "Language": "German"},
    {"Country": "United Kingdom", "Capital": "London", "Currency": "GBP", "Language": "English"},
    {"Country": "Canada", "Capital": "Ottawa", "Currency": "CAD", "Language": "English/French"},
    {"Country": "Australia", "Capital": "Canberra", "Currency": "AUD", "Language": "English"},
    {"Country": "India", "Capital": "New Delhi", "Currency": "INR", "Language": "Hindi/English"},
    {"Country": "Brazil", "Capital": "Brasília", "Currency": "BRL", "Language": "Portuguese"},
    {"Country": "China", "Capital": "Beijing", "Currency": "CNY", "Language": "Mandarin"},
    {"Country": "Thailand", "Capital": "Bangkok", "Currency": "THB", "Language": "Thai"},
]

FIELDS = ["Country", "Capital", "Currency", "Language"]


def write_csv(data, filename="countries.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV written to '{filename}'")


def write_json(data, filename="countries.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"JSON written to '{filename}'")


def write_markdown(data, filename="countries.md"):
    col_widths = {field: len(field) for field in FIELDS}
    for row in data:
        for field in FIELDS:
            col_widths[field] = max(col_widths[field], len(row[field]))

    def md_row(values):
        return "| " + " | ".join(v.ljust(col_widths[f]) for f, v in zip(FIELDS, values)) + " |"

    separator = "| " + " | ".join("-" * col_widths[f] for f in FIELDS) + " |"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_row(FIELDS) + "\n")
        f.write(separator + "\n")
        for row in data:
            f.write(md_row([row[f] for f in FIELDS]) + "\n")
    print(f"Markdown written to '{filename}'")


FORMATS = {
    "csv": write_csv,
    "json": write_json,
    "markdown": write_markdown,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export country data to a chosen format.")
    parser.add_argument(
        "--format",
        choices=FORMATS.keys(),
        default="csv",
        help="Output format: csv, json, or markdown (default: csv)",
    )
    args = parser.parse_args()
    FORMATS[args.format](COUNTRIES)
