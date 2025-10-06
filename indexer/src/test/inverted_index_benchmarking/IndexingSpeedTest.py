import io
import sys
import timeit
import gc
import shutil
import unittest
from pathlib import Path
from pymongo import MongoClient

from indexer.src.main.python.invertedindex.hierarchicalFolderStructure.HierarchicalFolderStructure import \
    HierarchicalFolderStructure
from indexer.src.main.python.invertedindex.MongoDb.MongoDb import MongoDB
from indexer.src.main.python.invertedindex.MonoliticStructure.MonoliticIndexer import MonoliticIndexer

DATALAKE_PATH = r"C:\Users\fabio\PycharmProjects\stage_1_V3\datalake"
INDEXING_SPEED_FILE = "indexer/src/test/resources/indexing_speed.txt"
NUM_ITERATIONS = 5
CLEANUP_AFTER_TEST = True


def generateSet():
    insertion_file = Path(INDEXING_SPEED_FILE)

    if not insertion_file.exists():
        print(f"ERROR: File {INDEXING_SPEED_FILE} does not exist!")
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


def cleanup_mongodb(db_name):
    try:
        client = MongoClient('localhost', serverSelectionTimeoutMS=5000)
        client.drop_database(db_name)
        client.close()
    except:
        pass


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

    def test_1_hierarchical_indexing_speed(self):
        print("\n[1/3] Testing HierarchicalFolderStructure...")
        output_h = "HIERARCHICAL_INDEX"

        def run_h():
            cleanup_directory(output_h)
            gc.collect()
            indexer = HierarchicalFolderStructure(downloadedBooksPath=DATALAKE_PATH,
                                                  hierarchicalOutputFolderPath=output_h)
            silent_run(lambda: indexer.buildIndexForBooks(self.synthetic_set, self.language_refs))

        avg_time = timeit.timeit(run_h, number=NUM_ITERATIONS) / NUM_ITERATIONS
        IndexingSpeedBenchmarkTest.results["HierarchicalFolderStructure"] = avg_time

        print(f"   Saving final output...")
        cleanup_directory(output_h)
        gc.collect()
        indexer_h = HierarchicalFolderStructure(downloadedBooksPath=DATALAKE_PATH,
                                                hierarchicalOutputFolderPath=output_h)
        indexer_h.buildIndexForBooks(self.synthetic_set, self.language_refs)

        if Path(output_h).exists():
            file_count = len(list(Path(output_h).rglob("*.txt")))
            print(f"   Created {file_count} .txt files in {output_h}/")
            self.assertGreater(file_count, 0, "Should create at least one .txt file")

        if CLEANUP_AFTER_TEST:
            cleanup_directory(output_h)

    def test_2_monolitic_indexing_speed(self):
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

    def test_3_mongodb_indexing_speed(self):
        print("[3/3] Testing MongoDB...")
        db_name = "BENCHMARK_INVERTED_INDEX"

        try:
            def run_mongo():
                cleanup_mongodb(db_name)
                gc.collect()
                indexer = MongoDB(databaseName=db_name, collectionName="benchmark", downloadedBooksPath=DATALAKE_PATH)
                silent_run(lambda: indexer.buildIndexForBooks(self.synthetic_set, self.language_refs))

            avg_time = timeit.timeit(run_mongo, number=NUM_ITERATIONS) / NUM_ITERATIONS
            IndexingSpeedBenchmarkTest.results["MongoDB"] = avg_time

            print(f"   Saving final output...")
            cleanup_mongodb(db_name)
            gc.collect()
            indexer_mongo = MongoDB(databaseName=db_name, collectionName="benchmark", downloadedBooksPath=DATALAKE_PATH)
            indexer_mongo.buildIndexForBooks(self.synthetic_set, self.language_refs)
            print(f"   Data stored in MongoDB database '{db_name}'")

            if CLEANUP_AFTER_TEST:
                cleanup_mongodb(db_name)

        except Exception as e:
            print(f"   MongoDB skipped: {e}")
            self.skipTest(f"MongoDB not available: {e}")

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
            cleanup_directory("MONOLITIC_INDEX")
            print("   Removed MONOLITIC_INDEX/")
            cleanup_mongodb("BENCHMARK_INVERTED_INDEX")
            print("   Removed MongoDB database 'BENCHMARK_INVERTED_INDEX'")
            print("Cleanup complete!\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)