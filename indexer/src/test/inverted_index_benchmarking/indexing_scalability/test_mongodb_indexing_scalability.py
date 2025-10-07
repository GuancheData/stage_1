import io
import sys
import timeit
import gc
import unittest
from pathlib import Path
from pymongo import MongoClient

from indexer.src.main.python.inverted_index.mongo_db.mongo_db import MongoDB

DATALAKE_PATH = "indexer/src/test/resources/datalake"
BOOKS_IDS_FILE = "indexer/src/test/resources/books_ids.txt"
NUM_ITERATIONS = 3
CLEANUP_AFTER_TEST = True

BOOK_SET_SIZES = [10, 50, 100]


def generate_set(max_books=None):
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


def generate_language_references(book_ids):
    return {str(book_id): 'english' for book_id in book_ids}


def cleanup_mongodb(db_name):
    client = None
    try:
        client = MongoClient('localhost', serverSelectionTimeoutMS=5000)
        client.drop_database(db_name)
    except Exception:
        pass
    finally:
        if client is not None:
            try:
                client.close()
            except Exception:
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
        print("MONGODB - SCALABILITY BENCHMARK")
        print("=" * 70)
        cls.results = {}

    def test_mongodb_indexing_scalability(self):
        print("\nTesting MongoDB with different book set sizes...")
        db_name = "BENCHMARK_INVERTED_INDEX"

        for num_books in BOOK_SET_SIZES:
            print(f"\n[Testing with {num_books} books]")

            synthetic_set = generate_set(max_books=num_books)

            if len(synthetic_set) == 0:
                print(f"   Skipping - no books available")
                continue

            language_refs = generate_language_references(synthetic_set)

            try:
                def run_mongo():
                    cleanup_mongodb(db_name)
                    gc.collect()
                    indexer = MongoDB(database_name=db_name, collection_name="benchmark",
                                      datalake_path=DATALAKE_PATH)
                    try:
                        silent_run(lambda: indexer.build_index_for_books(synthetic_set, language_refs))
                    finally:
                        if hasattr(indexer, 'client') and indexer.client is not None:
                            try:
                                indexer.client.close()
                            except Exception:
                                pass

                print(f"   Running {NUM_ITERATIONS} iterations...")
                avg_time = timeit.timeit(run_mongo, number=NUM_ITERATIONS) / NUM_ITERATIONS
                self.results[f"MongoDB_{num_books}_books"] = avg_time
                print(f"   Average time: {avg_time:.4f}s")

                print(f"   Saving final output...")
                cleanup_mongodb(db_name)
                gc.collect()
                indexer_mongo = MongoDB(database_name=db_name, collection_name="benchmark",
                                        datalake_path=DATALAKE_PATH)
                try:
                    indexer_mongo.build_index_for_books(synthetic_set, language_refs)
                    print(f"   Data stored in MongoDB database '{db_name}'")
                finally:
                    if hasattr(indexer_mongo, 'client') and indexer_mongo.client is not None:
                        try:
                            indexer_mongo.client.close()
                        except Exception:
                            pass

                if CLEANUP_AFTER_TEST:
                    cleanup_mongodb(db_name)

            except Exception as e:
                print(f"   MongoDB skipped for {num_books} books: {e}")
                continue

    @classmethod
    def tearDownClass(cls):
        if cls.results:
            print(f"\n{'=' * 70}")
            print(f"MONGODB INDEXING - SCALABILITY RESULTS")
            print(f"{'=' * 70}")
            for name in sorted(cls.results.keys()):
                print(f"{name:<40} {cls.results[name]:>10.4f}s")
            print(f"{'=' * 70}\n")

        if CLEANUP_AFTER_TEST:
            print("Cleaning up generated files...")
            cleanup_mongodb("BENCHMARK_INVERTED_INDEX")
            print("   Removed MongoDB database 'BENCHMARK_INVERTED_INDEX'")


if __name__ == '__main__':
    unittest.main(verbosity=2)