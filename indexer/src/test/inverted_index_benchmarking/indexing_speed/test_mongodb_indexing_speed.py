import io
import sys
import timeit
import gc
import shutil
import unittest
from pathlib import Path
from pymongo import MongoClient
from indexer.src.main.python.invertedindex.MongoDb.MongoDb import MongoDB

DATALAKE_PATH = "datalake"
BOOKS_IDS_FILE = "indexer/src/test/resources/books_ids.txt"
NUM_ITERATIONS = 5
CLEANUP_AFTER_TEST = True


def generateSet():
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


def generateLanguageReferences(book_ids):
    return {str(book_id): 'english' for book_id in book_ids}


def cleanup_directory(path):
    gc.collect()
    if Path(path).exists():
        shutil.rmtree(path, ignore_errors=True)


def cleanup_mongodb(db_name):
    client = None
    try:
        client = MongoClient('localhost', serverSelectionTimeoutMS=5000)
        client.drop_database(db_name)
    except Exception:
        pass
    finally:
        if client is not None:
            client.close()


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

    def test_3_mongodb_indexing_speed(self):
        print("[3/3] Testing MongoDB...")
        db_name = "BENCHMARK_INVERTED_INDEX"

        try:
            def run_mongo():
                cleanup_mongodb(db_name)
                gc.collect()
                indexer = MongoDB(databaseName=db_name, collectionName="benchmark", downloadedBooksPath=DATALAKE_PATH)
                try:
                    silent_run(lambda: indexer.buildIndexForBooks(self.synthetic_set, self.language_refs))
                finally:
                    if hasattr(indexer, 'client') and indexer.client is not None:
                        indexer.client.close()

            avg_time = timeit.timeit(run_mongo, number=NUM_ITERATIONS) / NUM_ITERATIONS
            IndexingSpeedBenchmarkTest.results["MongoDB"] = avg_time

            print(f"   Saving final output...")
            cleanup_mongodb(db_name)
            gc.collect()

            indexer_mongo = MongoDB(databaseName=db_name, collectionName="benchmark", downloadedBooksPath=DATALAKE_PATH)
            try:
                indexer_mongo.buildIndexForBooks(self.synthetic_set, self.language_refs)
                print(f"   Data stored in MongoDB database '{db_name}'")
            finally:
                if hasattr(indexer_mongo, 'client') and indexer_mongo.client is not None:
                    indexer_mongo.client.close()

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
            cleanup_mongodb("BENCHMARK_INVERTED_INDEX")
            print("   Removed MongoDB database 'BENCHMARK_INVERTED_INDEX'")


if __name__ == '__main__':
    unittest.main(verbosity=2)