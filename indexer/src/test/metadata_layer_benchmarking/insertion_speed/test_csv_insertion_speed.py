import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.parser.metadata_parser import MetadataParser
from indexer.src.main.python.metadata.storage.csv.metadata_csv_container import MetadataCSVContainer


downloads = "indexer/src/test/resources/test_downloaded_books_reference.txt"
DATALAKE_PATH = r""  #your datalake path

def generateSet():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_csv_insertion_speed_benchmark():
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

    def setup_csv():
        gc.collect()
        for _ in range(5):
            try:
                delete_csv()
                break
            except PermissionError:
                time.sleep(0.1)

    def recreate_csv_db():
        setup_csv()
        gc.collect()
        db = MetadataCSVContainer(MetadataParser(DATALAKE_PATH), "./METADATA")
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        db.save_metadata(synthetic_set)
        sys.stdout = old_stdout

    n = 5
    total_time = timeit.timeit(recreate_csv_db, number=n)
    print("\n--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (CSV) para {len(synthetic_set)} libros: {total_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    delete_csv()
    os.rmdir("./METADATA")