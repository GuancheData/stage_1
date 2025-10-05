import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.parser.MetadataParser import MetadataParser
from indexer.src.main.python.metadata.storage.csv.MetadataCSVContainer import MetadataCSVContainer
from indexer.src.main.python.metadata.storage.json.MetadataJSONContainer import MetadataJSONContainer
from indexer.src.main.python.metadata.storage.sqlite.MetadataSQLiteDB import MetadataSQLiteDB

DATALAKE_PATH = "control/datalake"
downloads = "indexer/src/test/resources/insertion_speed.txt"

def generateSet():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_sqlite_insertion_speed_benchmark():
    synthetic_set = generateSet()

    def delete_db():
        gc.collect()
        for _ in range(5):
            try:
                if os.path.exists("METADATA.db"):
                    os.remove("METADATA.db")
                break
            except PermissionError:
                time.sleep(0.1)

    def setup_db():
        gc.collect()
        for _ in range(5):
            try:
                delete_db()
                break
            except PermissionError:
                time.sleep(0.1)

    def recreate_db():
        setup_db()
        gc.collect()
        db = MetadataSQLiteDB(MetadataParser(DATALAKE_PATH), "METADATA.db")
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        db.saveMetadata(synthetic_set)
        sys.stdout = old_stdout

    n = 5
    total_time = timeit.timeit(recreate_db, number=n)
    print("\n-----------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (SQLite) para {len(synthetic_set)} libros: {total_time / n:.4f} segundos")
    print("-----------------------------------------------------------------")
    delete_db()

def test_json_insertion_speed_benchmark():
    synthetic_set = generateSet()

    def delete_json():
        gc.collect()
        for _ in range(5):
            try:
                if os.path.exists("METADATA.json"):
                    os.remove("METADATA.json")
                break
            except PermissionError:
                time.sleep(0.1)

    def setup_json():
        gc.collect()
        for _ in range(5):
            try:
                delete_json()
                break
            except PermissionError:
                time.sleep(0.1)

    def recreate_json_db():
        setup_json()
        gc.collect()
        db = MetadataJSONContainer(MetadataParser(DATALAKE_PATH), "METADATA.json")
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        db.saveMetadata(synthetic_set)
        sys.stdout = old_stdout

    n = 5
    total_time_json = timeit.timeit(recreate_json_db, number=n)
    print("\n-----------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (JSON) para {len(synthetic_set)} libros: {total_time_json / n:.4f} segundos")
    print("-----------------------------------------------------------------")
    delete_json()


'''def test_csv_save_metadata(benchmark):
    container = MetadataCSVContainer(MetadataParser(DATALAKE_PATH), "METADATA.csv")
    benchmark(container.saveMetadata)'''
