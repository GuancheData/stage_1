from pathlib import Path

from crawler.src.main.python.Crawler import Crawler
from indexer.src.main.python.metadata.storage.MetadataDatamartContainer import MetadataDatamartContainer


class PipelineController:
    def __init__(self, logs_path = Path("logs"), metadata_storage_mode = MetadataDatamartContainer, total_books = 1000):
        self.total_books = total_books
        self.control_path = Path(logs_path)
        self.downloaded_path = logs_path / "downloaded_books.txt"
        self.failed_to_download_path = logs_path / "failed_to_download_books.txt"
        self.index_path = logs_path / "indexed_books.txt"
        self.crawler = Crawler(datalakeStructure="id")
        self.indexer = metadata_storage_mode
        self.not_downloaded = set(range(1, self.total_books + 1)) - self.downloaded()

    def downloaded(self):
        return set((int(x) for x in set(self.downloaded_path.read_text().splitlines()))) if self.downloaded_path.exists() else set()

    def failed_to_download(self):
        return set((int(x) for x in set(self.failed_to_download_path.read_text().splitlines()))) if self.failed_to_download_path.exists() else set()

    def indexed(self):
        return set((int(x) for x in set(self.index_path.read_text().splitlines()))) if self.index_path.exists() else set()

    def pipeline(self, books_to_download = 1):
        self.control_path.mkdir(parents=True, exist_ok=True)
        ready_to_index = self.downloaded() - self.indexed()
        if ready_to_index:
            self.index(ready_to_index)
        for _ in range(books_to_download):
            if not self.download():
                break
        self.not_downloaded = set(range(1, self.total_books + 1)) - self.downloaded()
        if self.failed_to_download():
            print("[DOWNLOAD] These books could not be downloaded:", sorted(list(self.failed_to_download())))

    def index(self, ready_to_index):
        self.indexer.saveMetadata(ready_to_index)
        ####
        for book_id in ready_to_index:
            with open(self.index_path, "a", encoding="utf-8") as f:
                f.write(f"{book_id}\n")

    def download(self):
        if self.not_downloaded:
            candidate_id = self.not_downloaded.pop()
            while candidate_id in self.failed_to_download():
                if self.not_downloaded:
                    candidate_id = self.not_downloaded.pop()
                else:
                    return True
        else:
            print("[DOWNLOAD] There are no more books to download")
            return False
        print(f"[DOWNLOAD] Downloading new book with ID {candidate_id}...")
        was_successful = self.crawler.crawlBook(candidate_id)
        if was_successful:
            with open(self.downloaded_path, "a", encoding="utf-8") as f:
                f.write(f"{candidate_id}\n")
        else:
            with open(self.failed_to_download_path, "a", encoding="utf-8") as f:
                f.write(f"{candidate_id}\n")
        return True
