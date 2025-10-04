import json
import os

from indexer.src.main.python.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer

class MetadataJSONContainer(MetadataDatamartContainer):
    def __init__(self, parser, jsonPath):
        super().__init__(parser)
        self.jsonPath = jsonPath


    def saveMetadata(self, idSet):
        all_metadata = self.parser.parseMetadata(idSet)
        if os.path.exists(self.jsonPath):
            with open(self.jsonPath, 'r') as file:
                try:
                    existing_metadata = json.load(file)
                except json.JSONDecodeError:
                    existing_metadata = {}
        else:
            existing_metadata = {}
        existing_metadata.update(all_metadata)
        with open(self.jsonPath, 'w') as file:
            if existing_metadata:
                json.dump(existing_metadata, file, indent=2)
                print(f"Metadata saved in {self.jsonPath}\n")
        return self.extractLanguage(all_metadata)