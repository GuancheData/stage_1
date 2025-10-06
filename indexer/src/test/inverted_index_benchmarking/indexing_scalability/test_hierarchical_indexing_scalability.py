import io
import sys
import timeit
import gc
import shutil
import unittest
from pathlib import Path

from indexer.src.main.python.invertedindex.hierarchicalFolderStructure.HierarchicalFolderStructure import \
    HierarchicalFolderStructure

DATALAKE_PATH = "datalake"
BOOKS_IDS_FILE = "indexer/src/test/resources/books_ids.txt"
NUM_ITERATIONS = 3
CLEANUP_AFTER_TEST = True

BOOK_SET_SIZES = [10, 50, 100]


def generateSet(max_books=None):
    insertion_file = Path(BOOKS_IDS_FILE)

    if not insertion_file.exists():
        print(f"ERROR: File {BOOKS_IDS_FILE} does not exist")
        return set()

    try:
        book_ids = set(int(x.strip()) for x in insertion_file.read_text().splitlines() if x.strip())
        if max_books:
            book_ids = set(list(book_ids)[:max_books])
        print(f"Using {len(book_ids)} books from {BOOKS_IDS_FILE}")
        return book_ids
    except ValueError as e:
        print(f"ERROR: Invalid book ID in {BOOKS_IDS_FILE}: {e}")
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
        print("HIERARCHICAL FOLDER STRUCTURE - SCALABILITY BENCHMARK")
        print("=" * 70)
        cls.results = {}

    def test_hierarchical_indexing_scalability(self):
        print("\nTesting HierarchicalFolderStructure with different book set sizes...")
        output_h = "HIERARCHICAL_INDEX"

        for num_books in BOOK_SET_SIZES:
            print(f"\n[Testing with {num_books} books]")

            synthetic_set = generateSet(max_books=num_books)

            if len(synthetic_set) == 0:
                print(f"   Skipping - no books available")
                continue

            language_refs = generateLanguageReferences(synthetic_set)

            def run_h():
                cleanup_directory(output_h)
                gc.collect()
                indexer = HierarchicalFolderStructure(downloadedBooksPath=DATALAKE_PATH, hierarchicalOutputFolderPath=output_h)
                silent_run(lambda: indexer.buildIndexForBooks(synthetic_set, language_refs))

            print(f"   Running {NUM_ITERATIONS} iterations...")
            avg_time = timeit.timeit(run_h, number=NUM_ITERATIONS) / NUM_ITERATIONS
            self.results[f"HierarchicalFS_{num_books}_books"] = avg_time
            print(f"   Average time: {avg_time:.4f}s")

            print(f"   Saving final output...")
            cleanup_directory(output_h)
            gc.collect()
            indexer_h = HierarchicalFolderStructure(downloadedBooksPath=DATALAKE_PATH, hierarchicalOutputFolderPath=output_h)
            indexer_h.buildIndexForBooks(synthetic_set, language_refs)

            if Path(output_h).exists():
                file_count = len(list(Path(output_h).rglob("*.txt")))
                print(f"   Created {file_count} .txt files in {output_h}/")
                self.assertGreater(file_count, 0, "Should create at least one .txt file")

            if CLEANUP_AFTER_TEST:
                cleanup_directory(output_h)

    @classmethod
    def tearDownClass(cls):
        if cls.results:
            print(f"\n{'=' * 70}")
            print(f"HIERARCHICAL INDEXING - SCALABILITY RESULTS")
            print(f"{'=' * 70}")
            for name in sorted(cls.results.keys()):
                print(f"{name:<40} {cls.results[name]:>10.4f}s")
            print(f"{'=' * 70}\n")

        if CLEANUP_AFTER_TEST:
            print("Cleaning up generated files...")
            cleanup_directory("HIERARCHICAL_INDEX")
            print("   Removed HIERARCHICAL_INDEX/")


if __name__ == '__main__':
    unittest.main(verbosity=2)