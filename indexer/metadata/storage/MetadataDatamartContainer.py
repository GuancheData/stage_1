from abc import ABC, abstractmethod

from indexer.metadata.MetadataParser import MetadataParser


class MetadataDatamartContainer(ABC):
    def __init__(self, parser):
        self.parser = parser

    @abstractmethod
    def saveMetadata(self):
        pass