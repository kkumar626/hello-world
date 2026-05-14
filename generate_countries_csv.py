# Usage:
#   python3 generate_countries_csv.py                   -> countries.csv (default)
#   python3 generate_countries_csv.py --format json     -> countries.json
#   python3 generate_countries_csv.py --format markdown -> countries.md

import csv
import json
import argparse

COUNTRIES = [
    # Asia
    {"Continent": "Asia", "Country": "Japan", "Capital": "Tokyo", "Currency": "JPY", "Language": "Japanese"},
    {"Continent": "Asia", "Country": "China", "Capital": "Beijing", "Currency": "CNY", "Language": "Mandarin"},
    {"Continent": "Asia", "Country": "India", "Capital": "New Delhi", "Currency": "INR", "Language": "Hindi/English"},
    {"Continent": "Asia", "Country": "Thailand", "Capital": "Bangkok", "Currency": "THB", "Language": "Thai"},
    {"Continent": "Asia", "Country": "South Korea", "Capital": "Seoul", "Currency": "KRW", "Language": "Korean"},
    {"Continent": "Asia", "Country": "Indonesia", "Capital": "Jakarta", "Currency": "IDR", "Language": "Indonesian"},
    {"Continent": "Asia", "Country": "Vietnam", "Capital": "Hanoi", "Currency": "VND", "Language": "Vietnamese"},
    {"Continent": "Asia", "Country": "Malaysia", "Capital": "Kuala Lumpur", "Currency": "MYR", "Language": "Malay"},
    {"Continent": "Asia", "Country": "Philippines", "Capital": "Manila", "Currency": "PHP", "Language": "Filipino/English"},
    {"Continent": "Asia", "Country": "Saudi Arabia", "Capital": "Riyadh", "Currency": "SAR", "Language": "Arabic"},
    {"Continent": "Asia", "Country": "United Arab Emirates", "Capital": "Abu Dhabi", "Currency": "AED", "Language": "Arabic"},
    {"Continent": "Asia", "Country": "Singapore", "Capital": "Singapore", "Currency": "SGD", "Language": "English/Malay/Chinese/Tamil"},
    # Europe
    {"Continent": "Europe", "Country": "France", "Capital": "Paris", "Currency": "EUR", "Language": "French"},
    {"Continent": "Europe", "Country": "Germany", "Capital": "Berlin", "Currency": "EUR", "Language": "German"},
    {"Continent": "Europe", "Country": "United Kingdom", "Capital": "London", "Currency": "GBP", "Language": "English"},
    {"Continent": "Europe", "Country": "Italy", "Capital": "Rome", "Currency": "EUR", "Language": "Italian"},
    {"Continent": "Europe", "Country": "Spain", "Capital": "Madrid", "Currency": "EUR", "Language": "Spanish"},
    {"Continent": "Europe", "Country": "Netherlands", "Capital": "Amsterdam", "Currency": "EUR", "Language": "Dutch"},
    {"Continent": "Europe", "Country": "Sweden", "Capital": "Stockholm", "Currency": "SEK", "Language": "Swedish"},
    {"Continent": "Europe", "Country": "Switzerland", "Capital": "Bern", "Currency": "CHF", "Language": "German/French/Italian"},
    {"Continent": "Europe", "Country": "Poland", "Capital": "Warsaw", "Currency": "PLN", "Language": "Polish"},
    {"Continent": "Europe", "Country": "Portugal", "Capital": "Lisbon", "Currency": "EUR", "Language": "Portuguese"},
    {"Continent": "Europe", "Country": "Greece", "Capital": "Athens", "Currency": "EUR", "Language": "Greek"},
    {"Continent": "Europe", "Country": "Russia", "Capital": "Moscow", "Currency": "RUB", "Language": "Russian"},
    # Africa
    {"Continent": "Africa", "Country": "Nigeria", "Capital": "Abuja", "Currency": "NGN", "Language": "English"},
    {"Continent": "Africa", "Country": "South Africa", "Capital": "Pretoria", "Currency": "ZAR", "Language": "Zulu/Xhosa/Afrikaans/English"},
    {"Continent": "Africa", "Country": "Egypt", "Capital": "Cairo", "Currency": "EGP", "Language": "Arabic"},
    {"Continent": "Africa", "Country": "Kenya", "Capital": "Nairobi", "Currency": "KES", "Language": "Swahili/English"},
    {"Continent": "Africa", "Country": "Ethiopia", "Capital": "Addis Ababa", "Currency": "ETB", "Language": "Amharic"},
    {"Continent": "Africa", "Country": "Ghana", "Capital": "Accra", "Currency": "GHS", "Language": "English"},
    {"Continent": "Africa", "Country": "Tanzania", "Capital": "Dodoma", "Currency": "TZS", "Language": "Swahili/English"},
    {"Continent": "Africa", "Country": "Morocco", "Capital": "Rabat", "Currency": "MAD", "Language": "Arabic/Berber"},
    {"Continent": "Africa", "Country": "Senegal", "Capital": "Dakar", "Currency": "XOF", "Language": "French"},
    {"Continent": "Africa", "Country": "Uganda", "Capital": "Kampala", "Currency": "UGX", "Language": "English/Swahili"},
    # North America
    {"Continent": "North America", "Country": "United States", "Capital": "Washington, D.C.", "Currency": "USD", "Language": "English"},
    {"Continent": "North America", "Country": "Canada", "Capital": "Ottawa", "Currency": "CAD", "Language": "English/French"},
    {"Continent": "North America", "Country": "Mexico", "Capital": "Mexico City", "Currency": "MXN", "Language": "Spanish"},
    {"Continent": "North America", "Country": "Cuba", "Capital": "Havana", "Currency": "CUP", "Language": "Spanish"},
    {"Continent": "North America", "Country": "Jamaica", "Capital": "Kingston", "Currency": "JMD", "Language": "English"},
    {"Continent": "North America", "Country": "Guatemala", "Capital": "Guatemala City", "Currency": "GTQ", "Language": "Spanish"},
    {"Continent": "North America", "Country": "Costa Rica", "Capital": "San José", "Currency": "CRC", "Language": "Spanish"},
    {"Continent": "North America", "Country": "Panama", "Capital": "Panama City", "Currency": "PAB", "Language": "Spanish"},
    # South America
    {"Continent": "South America", "Country": "Brazil", "Capital": "Brasília", "Currency": "BRL", "Language": "Portuguese"},
    {"Continent": "South America", "Country": "Argentina", "Capital": "Buenos Aires", "Currency": "ARS", "Language": "Spanish"},
    {"Continent": "South America", "Country": "Colombia", "Capital": "Bogotá", "Currency": "COP", "Language": "Spanish"},
    {"Continent": "South America", "Country": "Chile", "Capital": "Santiago", "Currency": "CLP", "Language": "Spanish"},
    {"Continent": "South America", "Country": "Peru", "Capital": "Lima", "Currency": "PEN", "Language": "Spanish/Quechua"},
    {"Continent": "South America", "Country": "Venezuela", "Capital": "Caracas", "Currency": "VES", "Language": "Spanish"},
    {"Continent": "South America", "Country": "Ecuador", "Capital": "Quito", "Currency": "USD", "Language": "Spanish"},
    {"Continent": "South America", "Country": "Bolivia", "Capital": "Sucre", "Currency": "BOB", "Language": "Spanish/Quechua/Aymara"},
    {"Continent": "South America", "Country": "Uruguay", "Capital": "Montevideo", "Currency": "UYU", "Language": "Spanish"},
    # Oceania
    {"Continent": "Oceania", "Country": "Australia", "Capital": "Canberra", "Currency": "AUD", "Language": "English"},
    {"Continent": "Oceania", "Country": "New Zealand", "Capital": "Wellington", "Currency": "NZD", "Language": "English/Māori"},
]

FIELDS = ["Continent", "Country", "Capital", "Currency", "Language"]


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
