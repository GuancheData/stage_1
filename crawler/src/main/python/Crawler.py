from crawler.src.main.python.BookStorageDate import BookStorageDate
from crawler.src.main.python.BookStorageId import BookStorageId
from crawler.src.main.python.GutenbergRequest import GutenbergRequest

class Crawler:
    def __init__(self, datalakeStructure="date"):
        self.requester = GutenbergRequest()
        self.storage = BookStorageId() if datalakeStructure == "id" else BookStorageDate()
        self.datalake = datalakeStructure

    def crawlBook(self, bookId):
        content = self.requester.fetchBook(bookId)

        if content:
            path = self.storage.save(bookId, content)
            if path:
                print(f"[DOWNLOAD] Book {bookId} successfully found and saved at {path}", "\n")
                return True
            else:
                print(f"[DOWNLOAD] Book {bookId} not saved", "\n")
                return False
        else:
            print(f"[DOWNLOAD] Book {bookId} not found", "\n")
            return False
