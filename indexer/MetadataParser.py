from pathlib import Path
import re

class MetadataParser:

    def __init__(self, booksMetadataContentPath, bookCounterPath):
        self.booksMetadataContentPath = booksMetadataContentPath
        self.bookCounterPath = bookCounterPath


    def parseMetadata(self):
        route = Path(self.booksMetadataContentPath)
        files = route.rglob('*header.txt')
        pattern = re.compile(r"Title:\s*(.+)|Author:\s*(.+)|Language: \s*(.+)")
        for f in files:
            with f.open('r') as file:
                for line in file:
                    match = pattern.search(line)
                    if match:
                        print(match)