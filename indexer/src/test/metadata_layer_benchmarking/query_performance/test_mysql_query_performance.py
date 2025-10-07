import csv
import io
import mysql.connector
import sys
import time
import timeit
import os
import gc
from pathlib import Path

import indexer.src.test.resources.mysql_credentials as credentials
from indexer.src.main.python.metadata.parser.MetadataParser import MetadataParser
from indexer.src.main.python.metadata.storage.mysql.MetadataMySQLDB import MetadataMySQLDB

DATALAKE_PATH = r"" #your datalake path
downloads = "indexer/src/test/resources/test_downloaded_books_reference.txt"

def generateSet():
    return set((int(x) for x in set(Path(downloads).read_text().splitlines()))) if Path(downloads).exists() else set()

def test_mysql_query_performance_benchmark():
    synthetic_set = generateSet()

    def delete_mysql_database():
        gc.collect()
        config = {
            "host": credentials.MYSQL_HOST,
            "user": credentials.MYSQL_USER,
            "password": credentials.MYSQL_PASSWORD,
            "database": credentials.MYSQL_DATABASE
        }
        db_name = config["database"]
        try:
            conn = mysql.connector.connect(host=config["host"], user=config["user"], password=config["password"])
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
            conn.close()
            print(f"Base de datos '{db_name}' eliminada.")
        except mysql.connector.Error as e:
            print(f"Error al eliminar la base de datos: {e}")
            time.sleep(0.2)

    def query_books_by_author_mysql():
        author_name = "Thomas Jefferson"
        results = {}

        conn = mysql.connector.connect(
            host=credentials.MYSQL_HOST,
            user=credentials.MYSQL_USER,
            password=credentials.MYSQL_PASSWORD,
            database=credentials.MYSQL_DATABASE
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, language FROM metadata WHERE author = %s;", (author_name,))
        rows = cursor.fetchall()

        for book_id, title, author, language in rows:
            results[str(book_id)] = {
                "Title": title,
                "Author": author,
                "Language": language
            }

        conn.close()
        return results

    def query_books_by_language_mysql():
        language = "English"
        results = {}

        conn = mysql.connector.connect(
            host=credentials.MYSQL_HOST,
            user=credentials.MYSQL_USER,
            password=credentials.MYSQL_PASSWORD,
            database=credentials.MYSQL_DATABASE
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, language FROM metadata WHERE language = %s;", (language,))
        rows = cursor.fetchall()

        for book_id, title, author, language in rows:
            results[str(book_id)] = {
                "Title": title,
                "Author": author,
                "Language": language
            }

        conn.close()
        return results

    delete_mysql_database()
    db = MetadataMySQLDB(MetadataParser(DATALAKE_PATH), {
        "host": credentials.MYSQL_HOST,
        "user": credentials.MYSQL_USER,
        "password": credentials.MYSQL_PASSWORD,
        "database": credentials.MYSQL_DATABASE
    })
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    db.saveMetadata(synthetic_set)
    sys.stdout = old_stdout

    n = 5
    total_author_time = timeit.timeit(query_books_by_author_mysql, number=n)
    total_language_time = timeit.timeit(query_books_by_language_mysql, number=n)

    print("\n--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por autor ('Thomas Jefferson') en MySQL para {len(synthetic_set)} libros: {total_author_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")
    print(f"Tiempo promedio de query por idioma ('English') en MySQL para {len(synthetic_set)} libros: {total_language_time / n:.4f} segundos")
    print("--------------------------------------------------------------------------------------------------")

    delete_mysql_database()
