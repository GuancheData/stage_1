import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.parser.MetadataParser import MetadataParser
from indexer.src.main.python.metadata.storage.sqlite.MetadataSQLiteDB import MetadataSQLiteDB


DATALAKE_PATH = ""  #your datalake path
downloads = "indexer/src/test/resources/test_downloaded_books_reference.txt"

def generateSet():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_sqlite_insertion_speed_benchmark():
    synthetic_set = generateSet()

    def delete_db():
        gc.collect()
        for _ in range(5):
            try:
                if os.path.exists("./METADATA/metadata.db"):
                    os.remove("./METADATA/metadata.db")
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
        db = MetadataSQLiteDB(MetadataParser(DATALAKE_PATH), "./METADATA")
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        db.saveMetadata(synthetic_set)
        sys.stdout = old_stdout

    n = 5
    total_time = timeit.timeit(recreate_db, number=n)
    print("\n--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (SQLite) para {len(synthetic_set)} libros: {total_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    delete_db()
    os.rmdir("./METADATA")


