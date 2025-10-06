import csv
import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.storage.csv.metadata_csv_container import MetadataCSVContainer

DATALAKE_PATH = "control/datalake"
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
        print(results)
        return results

    db = MetadataCSVContainer(Path("METADATA"))
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    db.save_metadata(synthetic_set)
    sys.stdout = old_stdout

    n = 5
    total_time = timeit.timeit(query_books_by_author_csv, number=n)

    print("\n--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por autor ('Thomas Jefferson') en CSV para {len(synthetic_set)} libros: {total_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")

    delete_csv()
    if os.path.exists("./METADATA") and not os.listdir("./METADATA"):
        os.rmdir("./METADATA")