from abc import ABC, abstractmethod

class MetadataDatamartContainer(ABC):
    def __init__(self, parser):
        self.parser = parser

    @abstractmethod
    def saveMetadata(self):
        pass

    def extractLanguage(self, all_metadata):
        languages = {}
        for idx, metadata in all_metadata.items():
            languages[idx] = None if all_metadata[idx].get("Language") is None else all_metadata[idx].get("Language").lower()
        return languages