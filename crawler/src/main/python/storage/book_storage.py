import os
from abc import ABC, abstractmethod

BOOK_START = "*** START OF THE PROJECT GUTENBERG EBOOK"
BOOK_END = "*** END OF THE PROJECT GUTENBERG EBOOK"
class BookStorage(ABC):
    def __init__(self, datalake_path):
        self.datalake_path = datalake_path
        if not os.path.exists(datalake_path):
            os.makedirs(datalake_path)

    def separate_header(self, content):
        if BOOK_START not in content or BOOK_END not in content:
            return False

        header, body_footer = content.split(BOOK_START, 1)
        body_footer = body_footer.split("\n", 1) [1]
        body = body_footer.split(BOOK_END, 1)[0]

        return header, body

    @abstractmethod
    def save(self, book_id, content):
        pass
