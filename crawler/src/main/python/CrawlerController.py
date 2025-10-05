from crawler.src.main.python.storage.BookStorageDate import BookStorageDate
from crawler.src.main.python.storage.BookStorageId import BookStorageId
from crawler.src.main.python.GutenbergRequest import GutenbergRequest

from pathlib import Path

class CrawlerController:
    def __init__(self, total_books = 1000, datalakeStructure="date"):
        self.requester = GutenbergRequest()
        self.storage = BookStorageId() if datalakeStructure == "id" else BookStorageDate()
        self.datalake = datalakeStructure
        self.total_books = total_books
        self.logs_path = Path("../../../../control/logs")
        self.control_path = self.logs_path
        self.downloaded_path = self.logs_path / "downloaded_books.txt"
        self.failed_to_download_path = self.logs_path / "failed_to_download_books.txt"
        self.not_downloaded = set(range(1, self.total_books + 1)) - self._downloaded()

    def _downloaded(self):
        return set((int(x) for x in set(self.downloaded_path.read_text().splitlines()))) if self.downloaded_path.exists() else set()

    def _failed_to_download(self):
        return set((int(x) for x in set(self.failed_to_download_path.read_text().splitlines()))) if self.failed_to_download_path.exists() else set()

    def download(self, books_to_download = 1):
        self.control_path.mkdir(parents=True, exist_ok=True)

        for _ in range(books_to_download):
            if not self._crawlBooks():
                break

        self.not_downloaded = set(range(1, self.total_books + 1)) - self._downloaded()

        if self._failed_to_download():
            print("[DOWNLOAD] The following books could not be downloaded:", sorted(list(self._failed_to_download())))

    def _crawlBooks(self):
        if self.not_downloaded:
            candidate_id = self.not_downloaded.pop()
            while candidate_id in self._failed_to_download():
                if self.not_downloaded:
                    candidate_id = self.not_downloaded.pop()
                else:
                    return True
        else:
            print("[DOWNLOAD] There are no more books to download")
            return False
        print(f"[DOWNLOAD] Downloading new book with ID {candidate_id}...")
        was_successful = self._crawlBook(candidate_id)
        if was_successful:
            with open(self.downloaded_path, "a", encoding="utf-8") as f:
                f.write(f"{candidate_id}\n")
        else:
            with open(self.failed_to_download_path, "a", encoding="utf-8") as f:
                f.write(f"{candidate_id}\n")
        return True

    def _crawlBook(self, bookId):
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
