import re
from pathlib import Path

class MetadataParser():
    def __init__(self, datalake_path):
        self.datalake_path = datalake_path
        self.pattern = re.compile(r"Title:\s*(.+)|Author:\s*(.+)|Language:\s*(.+)")

    def parse_metadata(self, book_id_set):
        route = Path(self.datalake_path)
        all_metadata = {}
        for f in route.rglob(f'[0-9]*header.txt'):
            file_match = re.search(r"^(\d+)_", f.name)
            if int(file_match.group(1)) in book_id_set:
                print(f"[INDEX] Indexing book {file_match.group(1)}.")
                with f.open('r', encoding="utf-8") as file:
                    metadata = self._extract_metadata(file)
                    if metadata:
                        all_metadata[file_match.group(1)] = metadata
                        print(f"[INDEX] Book {file_match.group(1)} successfully indexed.\n")
                    else:
                        print(f"[INDEX] No metadata found in book {file_match.group(1)}.")
        return all_metadata

    def _extract_metadata(self, file):
        metadata = {}
        for line in file:
            match = self.pattern.search(line)
            if match:
                key, value = match.group(0).split(":", maxsplit=1)
                metadata[key.strip()] = value.strip()
        return metadata
