import io
import sys
import timeit
import gc
import shutil
import unittest
from pathlib import Path
from indexer.src.main.python.inverted_index.hierarchical_folder_structure.hierarchical_folder_structure import \
    HierarchicalFolderStructure


DATALAKE_PATH = "indexer/src/test/resources/datalake"
BOOKS_IDS_FILE = "indexer/src/test/resources/books_ids.txt"
NUM_ITERATIONS = 5
CLEANUP_AFTER_TEST = True
OUTPUT_H = "indexer/src/test/inverted_index_benchmarking/indexing_speed/HIERARCHICAL_INDEX"
def generate_set():
    insertion_file = Path(BOOKS_IDS_FILE)

    if not insertion_file.exists():
        print(f"ERROR: File {BOOKS_IDS_FILE} does not exist")
        return set()

    try:
        book_ids = set(int(x.strip()) for x in insertion_file.read_text().splitlines() if x.strip())
        print(f"Using {len(book_ids)} books from {BOOKS_IDS_FILE}")
        return book_ids
    except ValueError as e:
        print(f"ERROR: Invalid book ID in {BOOKS_IDS_FILE}: {e}")
        return set()

def generate_language_references(book_ids):
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
        cls.synthetic_set = generate_set()
        cls.language_refs = generate_language_references(cls.synthetic_set)
        cls.results = {}

    def test_hierarchical_indexing_speed(self):
        print("\n[1/3] Testing HierarchicalFolderStructure...")

        def run_h():
            cleanup_directory(OUTPUT_H)
            gc.collect()
            indexer = HierarchicalFolderStructure(datalake_path=DATALAKE_PATH, inverted_index_output_folder_path=OUTPUT_H)
            silent_run(lambda: indexer.build_index_for_books(self.synthetic_set, self.language_refs))

        avg_time = timeit.timeit(run_h, number=NUM_ITERATIONS) / NUM_ITERATIONS
        IndexingSpeedBenchmarkTest.results["HierarchicalFolderStructure"] = avg_time

        print(f"   Saving final output...")
        cleanup_directory(OUTPUT_H)
        gc.collect()
        indexer_h = HierarchicalFolderStructure(datalake_path=DATALAKE_PATH, inverted_index_output_folder_path=OUTPUT_H)
        indexer_h.build_index_for_books(self.synthetic_set, self.language_refs)

        if Path(OUTPUT_H).exists():
            file_count = len(list(Path(OUTPUT_H).rglob("*.txt")))
            print(f"   Created {file_count} .txt files in {OUTPUT_H}/")
            self.assertGreater(file_count, 0, "Should create at least one .txt file")

        if CLEANUP_AFTER_TEST:
            cleanup_directory(OUTPUT_H)

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
            cleanup_directory("HIERARCHICAL_INDEX")
            print("   Removed HIERARCHICAL_INDEX/")

if __name__ == '__main__':
    unittest.main(verbosity=2)