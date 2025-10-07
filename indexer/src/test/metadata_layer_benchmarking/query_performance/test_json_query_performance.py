import json
import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path

from indexer.src.main.python.metadata.parser.metadata_parser import MetadataParser
from indexer.src.main.python.metadata.storage.json.metadata_json_container import MetadataJSONContainer

DATALAKE_PATH = r"indexer/src/test/resources/datalake"
downloads = "indexer/src/test/resources/test_downloaded_books_reference.txt"

def generate_set():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_json_query_performance_benchmark():
    synthetic_set = generate_set()

    def delete_json():
        gc.collect()
        for _ in range(5):
            try:
                if os.path.exists("./METADATA/metadata.json"):
                    os.remove("./METADATA/metadata.json")
                break
            except PermissionError:
                time.sleep(0.1)

    def query_books_by_author_json():
        author_name = "Thomas Jefferson"
        results = {}
        with open("METADATA/metadata.json", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)  # data es un diccionario con IDs como claves
            for book_id, book_info in data.items():
                if book_info.get('Author', '').strip() == author_name:
                    results[book_id] = book_info
        return results

    def query_books_by_language_json():
        language = "English"
        results = {}
        with open("METADATA/metadata.json", encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            for book_id, book_info in data.items():
                if book_info.get('Language', '').strip() == language:
                    results[book_id] = book_info
        return results

    db = MetadataJSONContainer(MetadataParser(DATALAKE_PATH), "./METADATA")
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    db.save_metadata(synthetic_set)
    sys.stdout = old_stdout

    n = 5
    total_author_time = timeit.timeit(query_books_by_author_json, number=n)
    total_language_time = timeit.timeit(query_books_by_language_json, number=n)

    print("\n--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por autor ('Thomas Jefferson') en JSON para {len(synthetic_set)} libros: {total_author_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por idioma ('English') en JSON para {len(synthetic_set)} libros: {total_language_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")

    delete_json()
    if os.path.exists("./METADATA") and not os.listdir("./METADATA"):
        os.rmdir("./METADATA")
