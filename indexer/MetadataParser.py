from pathlib import Path
import re
import sqlite3

from indexer.IndexedBooksCount import IndexedBooksCount


class MetadataParser:

    def __init__(self, booksMetadataContentPath, bookCounterPath):
        self.booksMetadataContentPath = booksMetadataContentPath
        self.bookCounterPath = bookCounterPath
        self.bookCount = IndexedBooksCount(bookCounterPath)

    def store(self, id=None, title=None, author=None, language=None):
        if id is None:
            return "error"
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            language TEXT
            );
            """)

            cursor.execute("""
            INSERT INTO metadata (id, title, author, language)
            VALUES (?, ?, ?, ?)
            """, (id, title, author, language))



    def parseMetadata(self):
        route = Path(self.booksMetadataContentPath)
        files = route.rglob(f'[0-9]*header.txt')
        pattern = re.compile(r"Title:\s*(.+)|Author:\s*(.+)|Language:\s*(.+)")
        for f in files:
            fileMatch = re.search(r"^(\d+)_", f.name)
            if int(fileMatch.group(1)) >= int(self.bookCount.getId()):
                self.bookCount.increaseBookId()
                with f.open('r') as file:
                    metadata = {}
                    for line in file:
                        match = pattern.search(line)
                        if match:
                            matchSplit = match.group(0).split(sep=":", maxsplit=1)
                            metadata[matchSplit[0]] = matchSplit[1]
                            print(f"found a match in {fileMatch.group(1)}")
                    self.store(
                        id=int(fileMatch.group(1)),
                        title=metadata["Title"] if "Title" in metadata.keys() else None,
                        author=metadata["Author"] if "Author" in metadata.keys() else None,
                        language=metadata["Language"] if "Language" in metadata.keys() else None)