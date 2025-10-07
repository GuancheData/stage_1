import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.parser.metadata_parser import MetadataParser
from indexer.src.main.python.metadata.storage.csv.metadata_csv_container import MetadataCSVContainer


downloads_medium_size = "indexer/src/test/resources/test_downloaded_books_reference.txt"
downloads_big_size = "indexer/src/test/resources/test_downloaded_books_reference_big.txt"
downloads_small_size = "indexer/src/test/resources/test_downloaded_books_reference_small.txt"
DATALAKE_PATH = r""  #your datalake path

def generate_set(downloads):
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_csv_insertion_speed_benchmark():

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

    def recreate_csv_db(synthetic_set):
        setup_csv()
        gc.collect()
        db = MetadataCSVContainer(MetadataParser(DATALAKE_PATH), "./METADATA")
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        db.save_metadata(synthetic_set)
        sys.stdout = old_stdout

    n = 5
    synthetic_set_medium_size = generate_set(downloads_medium_size)
    synthetic_set_big_size = generate_set(downloads_big_size)
    synthetic_set_small_size = generate_set(downloads_small_size)
    total_small_time = timeit.timeit(lambda: recreate_csv_db(synthetic_set_small_size), number=n)
    total_medium_time = timeit.timeit(lambda: recreate_csv_db(synthetic_set_medium_size), number=n)
    total_big_time = timeit.timeit(lambda: recreate_csv_db(synthetic_set_big_size), number=n)
    print("\n--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (CSV) para {len(synthetic_set_small_size)} libros: {total_small_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (CSV) para {len(synthetic_set_medium_size)} libros: {total_medium_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (CSV) para {len(synthetic_set_big_size)} libros: {total_big_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    delete_csv()
    os.rmdir("./METADATA")