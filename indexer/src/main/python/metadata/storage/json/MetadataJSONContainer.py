import json
import os
from pathlib import Path
from indexer.src.main.python.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer
from indexer.src.main.python.metadata.parser.MetadataParser import MetadataParser

class MetadataJSONContainer(MetadataDatamartContainer):
    def __init__(self, json_path = Path("../../../../Metadata")):
        super().__init__()
        self.jsonPath = json_path
        self.jsonFilePath = self.jsonPath / "metadata.json"

    def saveMetadata(self, idSet):
        if not os.path.exists(self.jsonPath):
            self.jsonPath.mkdir(parents=True, exist_ok=True)
        all_metadata = self.parser.parseMetadata(idSet)
        print(all_metadata, "This is all the metadata")
        if os.path.exists(self.jsonFilePath):
            with open(self.jsonFilePath, 'r') as file:
                try:
                    existing_metadata = json.load(file)
                except json.JSONDecodeError:
                    existing_metadata = {}
        else:
            existing_metadata = {}
        existing_metadata.update(all_metadata)
        with open(self.jsonFilePath, 'w') as file:
            if existing_metadata:
                json.dump(existing_metadata, file, indent=2)
                print(f"Metadata saved in {self.jsonFilePath}\n")
        return self.extractLanguage(all_metadata)
