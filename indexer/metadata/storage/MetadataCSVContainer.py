import csv
import os

from indexer.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer

class MetadataCSVContainer(MetadataDatamartContainer):
    def __init__(self, parser, csvPath):
        super().__init__(parser)
        self.csvPath = csvPath

    def saveMetadata(self):
        all_metadata = self.parser.parseMetadata()
        file_exists = os.path.exists(self.csvPath)
        fieldnames = ["id", "Title", "Author", "Language"]
        with open(self.csvPath, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for id_key, metadata in all_metadata.items():
                row = {"id": id_key,"Title": metadata.get("Title", ""),"Author": metadata.get("Author", ""),"Language": metadata.get("Language", "")}
                writer.writerow(row)
        if len(all_metadata) != 0:
            print(f"Metadata saved in {self.csvPath}")