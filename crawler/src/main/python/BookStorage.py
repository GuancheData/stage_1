import os
from pathlib import Path
from abc import ABC, abstractmethod

BOOK_START = "*** START OF THE PROJECT GUTENBERG EBOOK"
BOOK_END = "*** END OF THE PROJECT GUTENBERG EBOOK"
class BookStorage(ABC):
    def __init__(self, outputDir = "datalake"):
        self.outputDir = Path(outputDir)
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

    def separateHeader(self, content):
        if BOOK_START not in content or BOOK_END not in content:
            return False

        header, bodyFooter = content.split(BOOK_START, 1)
        bodyFooter = bodyFooter.split("\n", 1) [1]
        body = bodyFooter.split(BOOK_END, 1)[0]

        return header, body

    @abstractmethod
    def save(self, bookId, content):
        pass
