import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path
import mysql.connector

import indexer.src.test.resources.mysql_credentials as credentials
from indexer.src.main.python.metadata.parser.metadata_parser import MetadataParser
from indexer.src.main.python.metadata.storage.mysql.metadata_mysqldb import MetadataMySQLDB
from indexer.src.main.python.metadata.storage.sqlite.metadata_sqlitedb import MetadataSQLiteDB

downloads_medium_size = "indexer/src/test/resources/test_downloaded_books_reference.txt"
downloads_big_size = "indexer/src/test/resources/test_downloaded_books_reference_big.txt"
downloads_small_size = "indexer/src/test/resources/test_downloaded_books_reference_small.txt"
DATALAKE_PATH = r"indexer/src/test/resources/datalake"

def generate_set(downloads):
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_mysql_insertion_speed_benchmark():

    def delete_mysql():
        gc.collect()
        conn = mysql.connector.connect(host=credentials.MYSQL_HOST, user=credentials.MYSQL_USER,
                                       password=credentials.MYSQL_PASSWORD, database=credentials.MYSQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS metadata")
        conn.commit()
        cursor.close()
        conn.close()
        time.sleep(0.1)

    def setup_mysql():
        gc.collect()
        for _ in range(5):
            try:
                delete_mysql()
                break
            except Exception:
                time.sleep(0.1)

    def recreate_mysql_db(synthetic_set):
        setup_mysql()
        gc.collect()
        db = MetadataMySQLDB(MetadataParser(DATALAKE_PATH),
                             {"host": credentials.MYSQL_HOST, "user": credentials.MYSQL_USER,
                              "password": credentials.MYSQL_PASSWORD, "database": credentials.MYSQL_DATABASE})
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        db.save_metadata(synthetic_set)
        sys.stdout = old_stdout

    n = 5
    synthetic_set_medium_size = generate_set(downloads_medium_size)
    synthetic_set_big_size = generate_set(downloads_big_size)
    synthetic_set_small_size = generate_set(downloads_small_size)
    total_small_time = timeit.timeit(lambda: recreate_mysql_db(synthetic_set_small_size), number=n)
    total_medium_time = timeit.timeit(lambda: recreate_mysql_db(synthetic_set_medium_size), number=n)
    total_big_time = timeit.timeit(lambda: recreate_mysql_db(synthetic_set_big_size), number=n)
    print("\n--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (MYSQL) para {len(synthetic_set_small_size)} libros: {total_small_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (MYSQL) para {len(synthetic_set_medium_size)} libros: {total_medium_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (MYSQL) para {len(synthetic_set_big_size)} libros: {total_big_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    delete_mysql()
