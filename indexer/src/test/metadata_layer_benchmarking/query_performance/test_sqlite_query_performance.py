import csv
import io
import sqlite3
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.parser.metadata_parser import MetadataParser
from indexer.src.main.python.metadata.storage.sqlite.metadata_sqlitedb import MetadataSQLiteDB

DATALAKE_PATH = r"indexer/src/test/resources/datalake"
downloads = "indexer/src/test/resources/test_downloaded_books_reference.txt"

def generate_set():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_sqlite_query_performance_benchmark():
    synthetic_set = generate_set()

    def delete_sqlite():
        gc.collect()
        for _ in range(5):
            try:
                if os.path.exists("./METADATA/metadata.db"):
                    os.remove("./METADATA/metadata.db")
                break
            except PermissionError:
                time.sleep(0.1)

    def query_books_by_author_sqlite():
        author_name = "Thomas Jefferson"
        results = {}

        conn = sqlite3.connect("./METADATA/metadata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, Title, Author, Language FROM metadata WHERE Author = ?", (author_name,))
        rows = cursor.fetchall()

        for book_id, title, author, language in rows:
            results[str(book_id)] = {
                "Title": title,
                "Author": author,
                "Language": language
            }
        conn.close()

        print(results)
        return results

    def query_books_by_language_sqlite():
        language = "English"
        results = {}

        conn = sqlite3.connect("./METADATA/metadata.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, Title, Author, Language FROM metadata WHERE Language = ?", (language,))
        rows = cursor.fetchall()

        for book_id, title, author, language in rows:
            results[str(book_id)] = {
                "Title": title,
                "Author": author,
                "Language": language
            }

        conn.close()
        return results

    delete_sqlite()
    db = MetadataSQLiteDB(MetadataParser(DATALAKE_PATH), "./METADATA")
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    db.save_metadata(synthetic_set)
    sys.stdout = old_stdout

    n = 5
    total_author_time = timeit.timeit(query_books_by_author_sqlite, number=n)
    total_language_time = timeit.timeit(query_books_by_language_sqlite, number=n)

    print("\n--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por autor ('Thomas Jefferson') en SQLITE para {len(synthetic_set)} libros: {total_author_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por idioma ('English') en SQLITE para {len(synthetic_set)} libros: {total_language_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")

    delete_sqlite()
    if os.path.exists("./METADATA") and not os.listdir("./METADATA"):
        os.rmdir("./METADATA")