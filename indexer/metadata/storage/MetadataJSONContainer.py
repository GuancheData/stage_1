import json

from indexer.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer

class MetadataJSONContainer(MetadataDatamartContainer):
    def __init__(self, parser, jsonPath):
        super().__init__(parser)
        self.jsonPath = jsonPath

    def saveMetadata(self, idSet):
        all_metadata = self.parser.parseMetadata(idSet)
        with open(self.jsonPath, 'a') as file:
            if all_metadata != {}:
                json.dump(all_metadata, file)
                print(f"Metadata saved in {self.jsonPath}\n")
