
# Open Library Books

A Python script that fetches book records from the Open Library
Search API, filters books first published after 2000, and saves
the results to a sorted CSV file.

## Features

- Fetches up to 50 book records from Open Library.
- Filters records by first publication year.
- Sorts results by publication year and title.
- Exports the data to CSV.

## Requirements

- Python 3.10+
- requests

## Installation

```bash
python -m venv .venv
```

Activate the virtual environment, then install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The script creates `books.csv` in the current directory.

## CSV columns

- title
- authors
- first_publish_year
- openlibrary_key