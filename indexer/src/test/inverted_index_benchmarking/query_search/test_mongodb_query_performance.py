import time
import gc
import unittest
from pathlib import Path
from pymongo import MongoClient
from indexer.src.main.python.invertedindex.MongoDb.MongoDb import MongoDB

DATALAKE_PATH = "datalake"
BOOKS_IDS_FILE = "indexer/src/test/resources/books_ids.txt"
DB_NAME = "BENCHMARK_INVERTED_INDEX"
COLLECTION_NAME = "benchmark"
CLEANUP_AFTER_TEST = True

TEST_QUERIES = [
    "love",
    "war",
    "peace",
    "journey",
    "time",
    "heart",
    "death",
    "life",
    "freedom",
    "power"
]

NUM_QUERY_RUNS = 100


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


def cleanup_mongodb(db_name):
    try:
        client = MongoClient('localhost', serverSelectionTimeoutMS=5000)
        client.drop_database(db_name)
        client.close()
    except:
        pass


class MongoDBQueryPerformanceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("=" * 70)
        print("MONGODB - QUERY PERFORMANCE BENCHMARK")
        print("=" * 70)
        cls.synthetic_set = generateSet()
        cls.language_refs = generateLanguageReferences(cls.synthetic_set)
        cls.results = {}
        cls.collection = None

        print(f"Building index for {len(cls.synthetic_set)} books...")
        print("(This is one-time setup, not part of query performance measurement)")

        try:
            cleanup_mongodb(DB_NAME)
            gc.collect()

            cls.indexer = MongoDB(databaseName=DB_NAME, collectionName=COLLECTION_NAME,
                                  downloadedBooksPath=DATALAKE_PATH)
            cls.indexer.buildIndexForBooks(cls.synthetic_set, cls.language_refs)

            client = MongoClient('localhost', serverSelectionTimeoutMS=5000)
            db = client[DB_NAME]
            cls.collection = db[COLLECTION_NAME]

            doc_count = cls.collection.count_documents({})
            print(f"Index built successfully in MongoDB database '{DB_NAME}'")
            print(f"Collection contains {doc_count} documents\n")
        except Exception as e:
            print(f"ERROR: MongoDB setup failed: {e}")
            raise unittest.SkipTest(f"MongoDB not available: {e}")

    def search_mongodb(self, query_term):
        query_term = query_term.lower().strip()

        if self.collection is None:
            return []

        try:
            result = self.collection.find_one({"word": query_term})

            if result and "books" in result:
                return list(result["books"].keys())
            else:
                return []

        except Exception as e:
            return []

    def test_query_performance(self):
        print("Testing query performance...")
        print(f"Running {len(TEST_QUERIES)} different queries, {NUM_QUERY_RUNS} times each\n")

        query_times = []
        detailed_results = []

        for query in TEST_QUERIES:
            start = time.perf_counter()
            for _ in range(NUM_QUERY_RUNS):
                results = self.search_mongodb(query)
            end = time.perf_counter()

            avg_time = (end - start) / NUM_QUERY_RUNS
            qps = 1 / avg_time if avg_time > 0 else 0
            query_times.append(avg_time)
            detailed_results.append({
                'query': query,
                'avg_time_ms': avg_time * 1000,
                'qps': qps
            })

            print(f"   '{query:<15}' {avg_time * 1000:>8.2f} ms/query  |  {qps:>8.2f} queries/sec")

        avg_query_time = sum(query_times) / len(query_times)
        min_query_time = min(query_times)
        max_query_time = max(query_times)
        queries_per_second = 1 / avg_query_time if avg_query_time > 0 else 0

        MongoDBQueryPerformanceTest.results = {
            "avg_time_ms": avg_query_time * 1000,
            "min_time_ms": min_query_time * 1000,
            "max_time_ms": max_query_time * 1000,
            "qps": queries_per_second,
            "detailed": detailed_results
        }

        self.assertGreater(queries_per_second, 0, "Should be able to execute queries")
        self.assertLess(avg_query_time, 5.0, "Average query time should be under 5 seconds")

    @classmethod
    def tearDownClass(cls):
        if cls.results:
            print(f"\n{'=' * 70}")
            print(f"MONGODB - SUMMARY")
            print(f"{'=' * 70}")
            print(f"Books indexed:           {len(cls.synthetic_set)}")
            print(f"Queries tested:          {len(TEST_QUERIES)}")
            print(f"Runs per query:          {NUM_QUERY_RUNS}")
            print(f"{'-' * 70}")
            print(f"Average query time:      {cls.results['avg_time_ms']:.2f} ms")
            print(f"Minimum query time:      {cls.results['min_time_ms']:.2f} ms")
            print(f"Maximum query time:      {cls.results['max_time_ms']:.2f} ms")
            print(f"Queries per second:      {cls.results['qps']:.2f} QPS")
            print(f"{'=' * 70}\n")

        if CLEANUP_AFTER_TEST:
            print("Cleaning up MongoDB database...")
            cleanup_mongodb(DB_NAME)
            print(f"   Removed MongoDB database '{DB_NAME}'")


if __name__ == '__main__':
    unittest.main(verbosity=2)