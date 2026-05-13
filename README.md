# hello-world

My personal sandbox — where scripts are born, ideas get tested, and nothing is too serious.

## What's in here

- **`generate_countries_csv.py`** — generates country data (capital, currency, language) across 6 continents in CSV, JSON, or Markdown format
- **`filter_countries.py`** — filters that data by continent straight from the terminal
- **`index.html`** — a simple webpage, just vibes

## Quick start

```bash
# Generate country data
python3 generate_countries_csv.py                   # CSV (default)
python3 generate_countries_csv.py --format json
python3 generate_countries_csv.py --format markdown

# Filter by continent
python3 filter_countries.py --list-continents
python3 filter_countries.py --continent Africa
python3 filter_countries.py --continent "South America" --input countries.json
```

## Notes to self

- This is a playground. Break things, fix things, repeat.
- Don't overthink it.
