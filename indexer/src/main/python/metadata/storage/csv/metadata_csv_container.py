import csv
import os
from pathlib import Path

from indexer.src.main.python.metadata.storage.metadata_datamart_container import MetadataDatamartContainer

class MetadataCSVContainer(MetadataDatamartContainer):
    def __init__(self, metadata_parser, csv_path):
        super().__init__(metadata_parser)
        self.csv_path = Path(csv_path)
        self.csv_file_path = self.csv_path / "metadata.csv"

    def save_metadata(self, book_id_set):
        if not os.path.exists(self.csv_path):
            self.csv_path.mkdir(parents=True, exist_ok=True)
        all_metadata = self.metadata_parser.parse_metadata(book_id_set)
        file_exists = os.path.exists(self.csv_file_path)
        field_names = ["id", "Title", "Author", "Language"]
        with open(self.csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            if not file_exists:
                writer.writeheader()
            for id_key, metadata in all_metadata.items():
                row = {"id": id_key,"Title": metadata.get("Title", ""),"Author": metadata.get("Author", ""),"Language": metadata.get("Language", "")}
                writer.writerow(row)
        if len(all_metadata) != 0:
            print(f"Metadata saved in {self.csv_file_path}")
        return self.extract_language(all_metadata)
