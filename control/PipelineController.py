from pathlib import Path
import random

from crawler.src.main.python.Crawler import Crawler


class PipelineController:
    def __init__(self, control_path = Path("control"), total_books = 1000):
        self.total_books = total_books
        self.control_path = control_path
        self.download_path = control_path / "downloaded_books.txt"
        self.index_path = control_path / "indexed_books.txt"
        self.crawler = Crawler(datalakeStructure="id")

    def downloaded(self):
        return set(self.download_path.read_text().splitlines()) if self.download_path.exists() else set()

    def indexed(self):
        return set(self.index_path.read_text().splitlines()) if self.index_path.exists() else set()

    def pipeline(self, books_to_download = 1):
        self.control_path.mkdir(parents=True, exist_ok=True)
        ready_to_index = self.downloaded() - self.indexed()
        # ready_to_index = False
        if ready_to_index:
            self.index(ready_to_index)
        for _ in range(books_to_download):
            self.download()

    def index(self, ready_to_index):
        for book_id in ready_to_index:
            print(f"[INDEX] indexing {book_id}")
                # Indexer here
            with open(self.index_path, "a", encoding="utf-8") as f:
                f.write(f"{book_id}\n")
            print(f"[INDEX] Book {book_id} successfully indexed.")

    def download(self):
        candidate_id = str(random.randint(1, self.total_books))
        if candidate_id not in self.downloaded():
            print(f"[DOWNLOAD] Downloading new book with ID {candidate_id}...")
            was_successful = self.crawler.crawlBook(candidate_id)
            if was_successful:
                with open(self.download_path, "a", encoding="utf-8") as f:
                    f.write(f"{candidate_id}\n")
