import csv
import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.parser.MetadataParser import MetadataParser
from indexer.src.main.python.metadata.storage.csv.MetadataCSVContainer import MetadataCSVContainer

DATALAKE_PATH = r"" #your datalake path
downloads = "indexer/src/test/resources/test_downloaded_books_reference.txt"

def generateSet():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_csv_query_performance_benchmark():
    synthetic_set = generateSet()

    def delete_csv():
        gc.collect()
        for _ in range(5):
            try:
                if os.path.exists("./METADATA/metadata.csv"):
                    os.remove("./METADATA/metadata.csv")
                break
            except PermissionError:
                time.sleep(0.1)

    def query_books_by_author_csv():
        author_name = "Thomas Jefferson"
        results = []
        with open("METADATA/metadata.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('Author', '').strip() == author_name:
                    results.append(row)
        return results

    def query_books_by_language_csv():
        language = "English"
        results = []
        with open("METADATA/metadata.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('Language', '').strip() == language:
                    results.append(row)
        return results

    db = MetadataCSVContainer(MetadataParser(DATALAKE_PATH), "./METADATA")
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    db.saveMetadata(synthetic_set)
    sys.stdout = old_stdout

    n = 5
    total_author_time = timeit.timeit(query_books_by_author_csv, number=n)
    total_language_time = timeit.timeit(query_books_by_language_csv, number=n)

    print("\n--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por autor ('Thomas Jefferson') en CSV para {len(synthetic_set)} libros: {total_author_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por idioma ('English') en CSV para {len(synthetic_set)} libros: {total_language_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")

    delete_csv()
    if os.path.exists("./METADATA") and not os.listdir("./METADATA"):
        os.rmdir("./METADATA")
