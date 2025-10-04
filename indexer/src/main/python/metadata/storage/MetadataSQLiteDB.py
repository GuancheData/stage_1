import sqlite3

from indexer.src.main.python.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer

class MetadataSQLiteDB(MetadataDatamartContainer):
    def __init__(self, parser, dbPath):
        super().__init__(parser)
        self.dbPath = dbPath

    def saveMetadata(self, idSet):
        metadataSet = self.parser.parseMetadata(idSet)
        for id, metadata in metadataSet.items():
            self.insertMetadata(id=int(id),
                title=metadata["Title"] if "Title" in metadata.keys() else None,
                author=metadata["Author"] if "Author" in metadata.keys() else None,
                language=metadata["Language"] if "Language" in metadata.keys() else None)
        if len(metadataSet.keys()) != 0:
            print(f"Metadata saved in {self.dbPath}\n")

    def insertMetadata(self, id, title, author, language):
        if id is None:
            return "error"
        with sqlite3.connect(self.dbPath) as connection:
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