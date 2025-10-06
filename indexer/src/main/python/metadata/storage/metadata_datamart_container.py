from abc import ABC, abstractmethod
from indexer.src.main.python.metadata.parser.metadata_parser import MetadataParser

class MetadataDatamartContainer(ABC):
    def __init__(self, metadata_parser):
        self.metadata_parser = metadata_parser

    @abstractmethod
    def save_metadata(self):
        pass

    def extract_language(self, all_metadata):
        languages = {}
        for idx, metadata in all_metadata.items():
            languages[idx] = None if all_metadata[idx].get("Language") is None else all_metadata[idx].get("Language").lower()
        return languages
