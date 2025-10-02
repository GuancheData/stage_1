from datetime import datetime, timezone

from crawler.src.main.python.BookStorage import BookStorage

BOOK_START = "*** START OF THE PROJECT GUTENBERG EBOOK"
BOOK_END = "*** END OF THE PROJECT GUTENBERG EBOOK"
class BookStorageId(BookStorage):
    def __init__(self, outputDir = "datalake"):
        super().__init__(outputDir)

    def save(self, bookId, content):
        bookId = int(bookId)
        contentSeparated = super().separateHeader(content)

        if not contentSeparated:
            return False

        headerContent, bodyContent = contentSeparated

        bookIdFormattedFirstHalfPath = self.outputDir / f"{bookId:04d}"[:2]
        bookIdFormattedSecondHalfPath = bookIdFormattedFirstHalfPath / f"{bookId:04d}"[2:]

        bookIdFormattedSecondHalfPath.mkdir(parents=True, exist_ok=True)

        headerPath = bookIdFormattedSecondHalfPath / f"{bookId}_header.txt"
        bodyPath = bookIdFormattedSecondHalfPath / f"{bookId}_body.txt"

        with open(headerPath, "w", encoding="utf-8") as file:
            file.write(headerContent.strip())
        with open (bodyPath, "w", encoding="utf-8") as file:
            file.write(bodyContent.strip())
        return str(headerPath), str(bodyPath)
