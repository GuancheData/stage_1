import os
import sqlite3
from pathlib import Path

from indexer.src.main.python.metadata.storage.metadata_datamart_container import MetadataDatamartContainer

class MetadataSQLiteDB(MetadataDatamartContainer):
    def __init__(self, metadata_parser, db_path):
        super().__init__(metadata_parser)
        self.db_path = Path(db_path)
        self.db_file_path = self.db_path / "metadata.db"

    def save_metadata(self, book_id_set):
        metadata_set = self.metadata_parser.parse_metadata(book_id_set)
        for id, metadata in metadata_set.items():
            self.insert_metadata(id=int(id),
                                 title=metadata["Title"] if "Title" in metadata.keys() else None,
                                 author=metadata["Author"] if "Author" in metadata.keys() else None,
                                 language=metadata["Language"] if "Language" in metadata.keys() else None)
        if len(metadata_set.keys()) != 0:
            print(f"Metadata saved in {self.db_file_path} (SQLite)\n")
            return self.extract_language(metadata_set)

    def insert_metadata(self, id, title, author, language):
        if not os.path.exists(self.db_path):
            self.db_path.mkdir(parents=True, exist_ok=True)

        if id is None:
            return "error"
        with sqlite3.connect(self.db_file_path) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata
            (id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            language TEXT);
                           """)

            cursor.execute("""
                           INSERT INTO metadata (id, title, author, language)
                           VALUES (?, ?, ?, ?)
                           """, (id, title, author, language))
