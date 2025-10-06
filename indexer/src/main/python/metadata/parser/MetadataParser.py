import re
from pathlib import Path

class MetadataParser():
    def __init__(self, booksMetadataContentPath = "./control/datalake"):
        self.booksMetadataContentPath = booksMetadataContentPath
        self.pattern = re.compile(r"Title:\s*(.+)|Author:\s*(.+)|Language:\s*(.+)")

    def parseMetadata(self, idSet):
        route = Path(self.booksMetadataContentPath)
        all_metadata = {}
        for f in route.rglob(f'[0-9]*header.txt'):
            fileMatch = re.search(r"^(\d+)_", f.name)
            if int(fileMatch.group(1)) in idSet:
                print(f"[INDEX] Indexing book {fileMatch.group(1)}.")
                with f.open('r', encoding="utf-8") as file:
                    metadata = self._extract_metadata(file)
                    if metadata:
                        #print(f"found a match in {fileMatch.group(1)}: {metadata}")
                        all_metadata[fileMatch.group(1)] = metadata
                        print(f"[INDEX] Book {fileMatch.group(1)} successfully indexed.\n")
                    else:
                        print(f"[INDEX] No metadata found in book {fileMatch.group(1)}.")
        return all_metadata

    def _extract_metadata(self, file):
        metadata = {}
        for line in file:
            match = self.pattern.search(line)
            if match:
                key, value = match.group(0).split(":", maxsplit=1)
                metadata[key.strip()] = value.strip()
        return metadata
