import json
import os
from pathlib import Path
from indexer.src.main.python.metadata.storage.metadata_datamart_container import MetadataDatamartContainer

class MetadataJSONContainer(MetadataDatamartContainer):
    def __init__(self, metadata_parser, json_path):
        super().__init__(metadata_parser)
        self.json_path = Path(json_path)
        self.json_file_path = self.json_path / "metadata.json"

    def save_metadata(self, book_id_set):
        if not os.path.exists(self.json_path):
            self.json_path.mkdir(parents=True, exist_ok=True)
        all_metadata = self.metadata_parser.parse_metadata(book_id_set)
        print(all_metadata, "This is all the metadata")
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as file:
                try:
                    existing_metadata = json.load(file)
                except json.JSONDecodeError:
                    existing_metadata = {}
        else:
            existing_metadata = {}
        existing_metadata.update(all_metadata)
        with open(self.json_file_path, 'w') as file:
            if existing_metadata:
                json.dump(existing_metadata, file, indent=2)
                print(f"Metadata saved in {self.json_file_path}\n")
        return self.extract_language(all_metadata)
