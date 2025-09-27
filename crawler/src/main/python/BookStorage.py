import os
from datetime import datetime
from pathlib import Path

BOOK_START = "*** START OF THE PROJECT GUTENBERG EBOOK"
BOOK_END = "*** END OF THE PROJECT GUTENBERG EBOOK"
class BookStorage:
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

    def save(self, bookId, content):
        contentSeparated = self.separateHeader(content)

        if not contentSeparated:
            return False

        headerContent, bodyContent = contentSeparated


        currentDate = datetime.today().strftime('%Y%m%d')
        currentTime = datetime.today().strftime('%H')

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
