import os
from datetime import datetime, timezone
from pathlib import Path

from crawler.src.main.python.BookStorage import BookStorage

BOOK_START = "*** START OF THE PROJECT GUTENBERG EBOOK"
BOOK_END = "*** END OF THE PROJECT GUTENBERG EBOOK"
class BookStorageDate(BookStorage):
    def __init__(self, outputDir = "datalake"):
        super().__init__(outputDir)

    def save(self, bookId, content):
        contentSeparated = super().separateHeader(content)

        if not contentSeparated:
            return False

        headerContent, bodyContent = contentSeparated

        currentDate = datetime.now(timezone.utc).strftime('%Y%m%d')
        currentTime = datetime.now(timezone.utc).strftime('%H')

        date_dir = self.outputDir / currentDate
        time_dir = date_dir / currentTime

        time_dir.mkdir(parents=True, exist_ok=True)

        headerPath = time_dir / f"{bookId}_header.txt"
        bodyPath = time_dir / f"{bookId}_body.txt"

        with open(headerPath, "w", encoding="utf-8") as file:
            file.write(headerContent.strip())
        with open (bodyPath, "w", encoding="utf-8") as file:
            file.write(bodyContent.strip())
        return str(headerPath), str(bodyPath)
