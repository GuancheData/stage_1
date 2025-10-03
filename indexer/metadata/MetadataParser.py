import re
from pathlib import Path
from indexer.IndexedBooksCount import IndexedBooksCount

class MetadataParser():
    def __init__(self, booksMetadataContentPath, bookCounterPath):
        self.booksMetadataContentPath = booksMetadataContentPath
        self.bookCounterPath = bookCounterPath
        self.bookCount = IndexedBooksCount(bookCounterPath)
        self.pattern = re.compile(r"Title:\s*(.+)|Author:\s*(.+)|Language:\s*(.+)")

    def parseMetadata(self):
        route = Path(self.booksMetadataContentPath)
        files = sorted(list(route.rglob(f'[0-9]*header.txt')), key=lambda x: int(x.name.split('_')[0]))
        all_metadata = {}
        for f in files:
            fileMatch = re.search(r"^(\d+)_", f.name)
            if int(fileMatch.group(1)) >= int(self.bookCount.getId()):
                with f.open('r') as file:
                    metadata = self._extract_metadata(file)
                    if metadata:
                        print(f"found a match in {fileMatch.group(1)}: {metadata}")
                        all_metadata[fileMatch.group(1)] = metadata
                self.bookCount.increaseBookId()
            print(f.name)
        print("Todos los metadatos encontrados:", all_metadata)
        return all_metadata

    def _extract_metadata(self, file):
        metadata = {}
        for line in file:
            match = self.pattern.search(line)
            if match:
                key, value = match.group(0).split(":", maxsplit=1)
                metadata[key.strip()] = value.strip()
        return metadata

