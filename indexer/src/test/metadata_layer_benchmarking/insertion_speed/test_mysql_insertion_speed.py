import io
import sys
import time
import timeit
import os
import gc
from pathlib import Path
import mysql.connector

import indexer.src.test.resources.mysql_credentials as credentials
from indexer.src.main.python.metadata.storage.mysql.MetadataMySQLDB import MetadataMySQLDB

DATALAKE_PATH = "control/datalake"
downloads = "indexer/src/test/resources/insertion_speed.txt"

def generateSet():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_mysql_insertion_speed_benchmark():
    synthetic_set = generateSet()

    def delete_db():
        gc.collect()
        conn = mysql.connector.connect(host=credentials.MYSQL_HOST,user=credentials.MYSQL_USER,password=credentials.MYSQL_PASSWORD,database=credentials.MYSQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS metadata")
        conn.commit()
        cursor.close()
        conn.close()
        time.sleep(0.1)

    def setup_db():
        gc.collect()
        for _ in range(5):
            try:
                delete_db()
                break
            except Exception:
                time.sleep(0.1)

    def recreate_db():
        setup_db()
        gc.collect()
        db = MetadataMySQLDB({"host":credentials.MYSQL_HOST, "user":credentials.MYSQL_USER, "password":credentials.MYSQL_PASSWORD, "database":credentials.MYSQL_DATABASE})
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        db.saveMetadata(synthetic_set)
        sys.stdout = old_stdout

    n = 5
    total_time = timeit.timeit(recreate_db, number=n)
    print("\n--------------------------------------------------------------------------------")
    print(f"Tiempo promedio por inserción (MySQL) para {len(synthetic_set)} libros: {total_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------")
    delete_db()