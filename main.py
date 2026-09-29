
import csv
import time
import requests

API_URL = "https://openlibrary.org/search.json"
OUTPUT_FILE = "books.csv"
BOOK_LIMIT = 50
MIN_YEAR = 2000
BATCH_SIZE = 100
MAX_PAGES = 20



def fetch_page(page):
    headers = {
        "User-Agent": "OpenLibraryBooksProject/1.0 (student project)"
    }

    for limit in (20, 10, 5):
        params = {
            "q": "book",
            "page": page,
            "limit": limit,
            "fields": "key,title,author_name,first_publish_year",
        }

        for attempt in range(3):
            try:
                response = requests.get(
                    API_URL,
                    params=params,
                    headers=headers,
                    timeout=30,
                )
                response.raise_for_status()
                return response.json().get("docs", [])

            except requests.RequestException as error:
                print(
                    f"Page {page}, limit {limit}, "
                    f"attempt {attempt + 1}: {error}"
                )

                if attempt < 2:
                    time.sleep(2 ** (attempt + 1))

        print(f"Retrying page {page} with a smaller batch...")

    raise RuntimeError(
        f"Could not fetch page {page} after retries."
    )


def fetch_books():
    books_by_key = {}

    for page in range(1, MAX_PAGES + 1):
        print(f"Fetching page {page}...")

        books = fetch_page(page)

        if not books:
            print("No more records available.")
            break

        for book in books:
            year = book.get("first_publish_year")
            key = book.get("key")

            if (
                isinstance(year, int)
                and year > MIN_YEAR
                and key
                and key not in books_by_key
            ):
                books_by_key[key] = {
                    "title": book.get("title", ""),
                    "authors": "; ".join(
                        book.get("author_name", [])
                    ),
                    "first_publish_year": year,
                    "openlibrary_key": key,
                }

            if len(books_by_key) == BOOK_LIMIT:
                break

        print(f"Qualifying books found: {len(books_by_key)}")

        if len(books_by_key) >= BOOK_LIMIT:
            break

        time.sleep(0.5)

    return list(books_by_key.values())


def save_books(books, filename=OUTPUT_FILE):
    
    fieldnames = [
        "title",
        "authors",
        "first_publish_year",
        "openlibrary_key",
    ]

    books.sort(
        key=lambda book: (
            book["first_publish_year"],
            book["title"].casefold(),
        )
    )

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)


def main():
    try:
        books = fetch_books()
        save_books(books)

        print("\nDownload completed!")
        print(f"Books saved: {len(books)}")
        print(f"Output file: {OUTPUT_FILE}")

        if len(books) < BOOK_LIMIT:
            print(
                f"Warning: Only {len(books)} qualifying books "
                "were found within the page limit."
            )

    except requests.RequestException as error:
        print(f"API request failed: {error}")


if __name__ == "__main__":
    main()