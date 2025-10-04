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
            languages[idx] = (all_metadata[idx]["Language"]).lower()
        print(languages)
        return languages