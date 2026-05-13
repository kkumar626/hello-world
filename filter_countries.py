# Usage:
#   python3 filter_countries.py --continent Asia
#   python3 filter_countries.py --continent "North America" --input countries.json
#   python3 filter_countries.py --continent Africa --input countries.csv
#   python3 filter_countries.py --list-continents

import csv
import json
import argparse
import os

VALID_CONTINENTS = ["Asia", "Europe", "Africa", "North America", "South America", "Oceania"]


def load_csv(filepath):
    with open(filepath, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_json(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def load_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".csv":
        return load_csv(filepath)
    elif ext == ".json":
        return load_json(filepath)
    else:
        raise ValueError(f"Unsupported file type '{ext}'. Use a .csv or .json file.")


def print_table(rows):
    if not rows:
        print("No countries found.")
        return

    fields = list(rows[0].keys())
    col_widths = {f: len(f) for f in fields}
    for row in rows:
        for f in fields:
            col_widths[f] = max(col_widths[f], len(row.get(f, "")))

    def fmt_row(values):
        return "| " + " | ".join(v.ljust(col_widths[f]) for f, v in zip(fields, values)) + " |"

    separator = "| " + " | ".join("-" * col_widths[f] for f in fields) + " |"

    print(fmt_row(fields))
    print(separator)
    for row in rows:
        print(fmt_row([row.get(f, "") for f in fields]))


def find_input_file():
    for candidate in ["countries.csv", "countries.json"]:
        if os.path.exists(candidate):
            return candidate
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter countries by continent.")
    parser.add_argument("--continent", help="Continent to filter by (e.g. Asia, Europe, Africa)")
    parser.add_argument("--input", help="Input file (countries.csv or countries.json). Auto-detected if omitted.")
    parser.add_argument("--list-continents", action="store_true", help="List all available continents and exit")
    args = parser.parse_args()

    if args.list_continents:
        print("Available continents:")
        for c in VALID_CONTINENTS:
            print(f"  - {c}")
        exit(0)

    if not args.continent:
        parser.error("--continent is required. Use --list-continents to see options.")

    input_file = args.input or find_input_file()
    if not input_file:
        print("No input file found. Run generate_countries_csv.py first, or specify --input.")
        exit(1)

    continent = args.continent.strip()
    matches = [c for c in VALID_CONTINENTS if c.lower() == continent.lower()]
    if not matches:
        print(f"Unknown continent '{continent}'. Use --list-continents to see valid options.")
        exit(1)
    continent = matches[0]

    data = load_file(input_file)

    if "Continent" not in data[0]:
        print(f"'{input_file}' does not have a Continent column. Regenerate it with the updated generate_countries_csv.py.")
        exit(1)

    results = [row for row in data if row.get("Continent", "").lower() == continent.lower()]

    print(f"\nCountries in {continent} ({len(results)} found) — source: {input_file}\n")
    print_table(results)
