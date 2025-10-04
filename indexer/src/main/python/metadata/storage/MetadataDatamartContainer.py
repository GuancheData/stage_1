from abc import ABC, abstractmethod


class MetadataDatamartContainer(ABC):
    def __init__(self, parser):
        self.parser = parser

    @abstractmethod
    def saveMetadata(self):
        pass