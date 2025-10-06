import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.storage.json.MetadataJSONContainer import MetadataJSONContainer

DATALAKE_PATH = "control/datalake"
downloads = "indexer/src/test/resources/insertion_speed.txt"

def generateSet():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_json_insertion_speed_benchmark():
    synthetic_set = generateSet()

    def delete_json():
        gc.collect()
        for _ in range(5):
            try:
                if os.path.exists("./METADATA/metadata.json"):
                    os.remove("./METADATA/metadata.json")
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
        db = MetadataJSONContainer(Path("METADATA"))
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        db.saveMetadata(synthetic_set)
        sys.stdout = old_stdout

    n = 5
    total_time_json = timeit.timeit(recreate_json_db, number=n)
    print("\n--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (JSON) para {len(synthetic_set)} libros: {total_time_json / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    delete_json()
    os.rmdir("./METADATA")
