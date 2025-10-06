import io
import sys
import timeit
import gc
import shutil
import unittest
from pathlib import Path
from indexer.src.main.python.invertedindex.MonoliticStructure.MonoliticIndexer import MonoliticIndexer


DATALAKE_PATH = "datalake"
INDEXING_SPEED_FILE = "indexer/src/test/resources/indexing_ids.txt"
NUM_ITERATIONS = 5
CLEANUP_AFTER_TEST = True

def generateSet():
    insertion_file = Path(INDEXING_SPEED_FILE)

    if not insertion_file.exists():
        print(f"ERROR: File {INDEXING_SPEED_FILE} does not exist")
        return set()

    try:
        book_ids = set(int(x.strip()) for x in insertion_file.read_text().splitlines() if x.strip())
        print(f"Using {len(book_ids)} books from {INDEXING_SPEED_FILE}")
        return book_ids
    except ValueError as e:
        print(f"ERROR: Invalid book ID in {INDEXING_SPEED_FILE}: {e}")
        return set()

def generateLanguageReferences(book_ids):
    return {str(book_id): 'english' for book_id in book_ids}

def cleanup_directory(path):
    gc.collect()
    if Path(path).exists():
        shutil.rmtree(path, ignore_errors=True)

def silent_run(func):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        func()
    finally:
        sys.stdout = old_stdout

class IndexingSpeedBenchmarkTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("=" * 70)
        print("INVERTED INDEX SPEED BENCHMARK")
        print("=" * 70)
        cls.synthetic_set = generateSet()
        cls.language_refs = generateLanguageReferences(cls.synthetic_set)
        cls.results = {}

    def test_monolitic_indexing_speed(self):
        print("[2/3] Testing MonoliticIndexer...")
        output_m = "MONOLITIC_INDEX"

        def run_m():
            cleanup_directory(output_m)
            gc.collect()
            indexer = MonoliticIndexer(output_json_path=output_m, downloaded_books_path=DATALAKE_PATH)
            silent_run(lambda: indexer.buildIndexForBooks(self.synthetic_set, self.language_refs))

        avg_time = timeit.timeit(run_m, number=NUM_ITERATIONS) / NUM_ITERATIONS
        IndexingSpeedBenchmarkTest.results["MonoliticIndexer"] = avg_time

        print(f"   Saving final output...")
        cleanup_directory(output_m)
        gc.collect()
        indexer_m = MonoliticIndexer(output_json_path=output_m, downloaded_books_path=DATALAKE_PATH)
        indexer_m.buildIndexForBooks(self.synthetic_set, self.language_refs)

        json_file = Path(output_m) / "inverted_index.json"
        if json_file.exists():
            size = json_file.stat().st_size / (1024 * 1024)
            print(f"   Created inverted_index.json ({size:.2f} MB)")
            self.assertTrue(json_file.exists(), "inverted_index.json should be created")

        if CLEANUP_AFTER_TEST:
            cleanup_directory(output_m)

    @classmethod
    def tearDownClass(cls):
        if cls.results:
            print(f"\n{'=' * 70}")
            print(f"INDEXING SPEED COMPARISON - {len(cls.synthetic_set)} books")
            print(f"{'=' * 70}")
            for name in sorted(cls.results.keys(), key=lambda x: cls.results[x]):
                print(f"{name:<35} {cls.results[name]:>10.4f}s")
            print(f"{'=' * 70}\n")

        if CLEANUP_AFTER_TEST:
            print("Cleaning up generated files...")
            cleanup_directory("MONOLITIC_INDEX")
            print("   Removed MONOLITIC_INDEX/")

if __name__ == '__main__':
    unittest.main(verbosity=2)