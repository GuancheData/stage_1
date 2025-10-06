import time
import gc
import shutil
import unittest
import json
from pathlib import Path
from indexer.src.main.python.invertedindex.MonoliticStructure.MonoliticIndexer import MonoliticIndexer

DATALAKE_PATH = "datalake"
BOOKS_IDS_FILE = "indexer/src/test/resources/indexing_ids.txt"
OUTPUT_PATH = "MONOLITIC_INDEX"
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


def cleanup_directory(path):
    gc.collect()
    if Path(path).exists():
        shutil.rmtree(path, ignore_errors=True)


class MonoliticQueryPerformanceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("=" * 70)
        print("MONOLITIC INDEXER - QUERY PERFORMANCE BENCHMARK")
        print("=" * 70)
        cls.synthetic_set = generateSet()
        cls.language_refs = generateLanguageReferences(cls.synthetic_set)
        cls.results = {}
        cls.inverted_index = None

        print(f"Building index for {len(cls.synthetic_set)} books...")
        print("(This is one-time setup, not part of query performance measurement)")
        cleanup_directory(OUTPUT_PATH)
        gc.collect()

        cls.indexer = MonoliticIndexer(output_json_path=OUTPUT_PATH, downloaded_books_path=DATALAKE_PATH)
        cls.indexer.buildIndexForBooks(cls.synthetic_set, cls.language_refs)

        index_file = Path(OUTPUT_PATH) / "inverted_index.json"
        if index_file.exists():
            size = index_file.stat().st_size / (1024 * 1024)
            print(f"Index built successfully (inverted_index.json: {size:.2f} MB)")

            with open(index_file, 'r') as f:
                cls.inverted_index = json.load(f)
            print(f"Loaded {len(cls.inverted_index)} terms into memory\n")
        else:
            print("WARNING: Index file not created\n")

    def search_monolitic(self, query_term):
        query_term = query_term.lower().strip()

        if self.inverted_index is None:
            return []

        if query_term in self.inverted_index:
            return list(self.inverted_index[query_term].keys())
        else:
            return []

    def test_query_performance(self):
        print("Testing query performance...")
        print(f"Running {len(TEST_QUERIES)} different queries, {NUM_QUERY_RUNS} times each\n")

        query_times = []
        detailed_results = []

        for query in TEST_QUERIES:
            start = time.perf_counter()
            for _ in range(NUM_QUERY_RUNS):
                results = self.search_monolitic(query)
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

        MonoliticQueryPerformanceTest.results = {
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
            print(f"MONOLITIC INDEXER - SUMMARY")
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
            print("Cleaning up generated files...")
            cleanup_directory(OUTPUT_PATH)
            print(f"   Removed {OUTPUT_PATH}/")


if __name__ == '__main__':
    unittest.main(verbosity=2)