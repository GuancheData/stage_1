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

        bookIdStr = f"{bookId:04d}"

        if len(bookIdStr) > 4 and len(bookIdStr) % 2 != 0:
            bookIdStr = f"0{bookIdStr}"

        parts = [bookIdStr[i:i+2] for i in range(0, len(bookIdStr), 2)]
        path = self.outputDir
        for part in parts:
            path = path / part

        path.mkdir(parents=True, exist_ok=True)

        headerPath = path / f"{bookId}_header.txt"
        bodyPath = path / f"{bookId}_body.txt"

        with open(headerPath, "w", encoding="utf-8") as file:
            file.write(headerContent.strip())
        with open (bodyPath, "w", encoding="utf-8") as file:
            file.write(bodyContent.strip())
        return str(headerPath), str(bodyPath)
