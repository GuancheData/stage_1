import csv
import os
from pathlib import Path

from indexer.src.main.python.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer

class MetadataCSVContainer(MetadataDatamartContainer):
    def __init__(self, parser, csvPath):
        super().__init__(parser)
        self.csvPath = Path(csvPath)
        self.csvFilePath = self.csvPath / "metadata.csv"

    def saveMetadata(self, idSet):
        if not os.path.exists(self.csvPath):
            self.csvPath.mkdir(parents=True, exist_ok=True)
        all_metadata = self.parser.parseMetadata(idSet)
        file_exists = os.path.exists(self.csvFilePath)
        fieldnames = ["id", "Title", "Author", "Language"]
        with open(self.csvFilePath, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for id_key, metadata in all_metadata.items():
                row = {"id": id_key,"Title": metadata.get("Title", ""),"Author": metadata.get("Author", ""),"Language": metadata.get("Language", "")}
                writer.writerow(row)
        if len(all_metadata) != 0:
            print(f"Metadata saved in {self.csvFilePath}")
        return self.extractLanguage(all_metadata)