import os
import sqlite3
from pathlib import Path

from indexer.src.main.python.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer

class MetadataSQLiteDB(MetadataDatamartContainer):
    def __init__(self, dbPath = "../../../../Metadata"):
        super().__init__()
        self.dbPath = Path(dbPath)
        self.dbFilePath = self.dbPath / "metadata.db"

    def saveMetadata(self, idSet):
        metadataSet = self.parser.parseMetadata(idSet)
        for id, metadata in metadataSet.items():
            self.insertMetadata(id=int(id),
                title=metadata["Title"] if "Title" in metadata.keys() else None,
                author=metadata["Author"] if "Author" in metadata.keys() else None,
                language=metadata["Language"] if "Language" in metadata.keys() else None)
        if len(metadataSet.keys()) != 0:
            print(f"Metadata saved in {self.dbFilePath} (SQLite)\n")
            return self.extractLanguage(metadataSet)

    def insertMetadata(self, id, title, author, language):
        if not os.path.exists(self.dbPath):
            self.dbPath.mkdir(parents=True, exist_ok=True)

        if id is None:
            return "error"
        with sqlite3.connect(self.dbFilePath) as connection:
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