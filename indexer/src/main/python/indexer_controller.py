from pathlib import Path

class IndexerController():
    def __init__(self, metadata_storage_mode, inverted_index_storage_mode, logs_output_path):
        self.logs_output_path = Path(logs_output_path)
        self.control_path = self.logs_output_path
        self.downloaded_path = self.logs_output_path / "downloaded_books.txt"
        self.failed_to_download_path = self.logs_output_path / "failed_to_download_books.txt"
        self.index_path = self.logs_output_path / "indexed_books.txt"
        self.indexer = metadata_storage_mode
        self.inverted_index = inverted_index_storage_mode

    def _downloaded(self):
        return set((int(x) for x in set(self.downloaded_path.read_text().splitlines()))) if self.downloaded_path.exists() else set()

    def _indexed(self):
        return set((int(x) for x in set(self.index_path.read_text().splitlines()))) if self.index_path.exists() else set()

    def index(self):
        self.control_path.mkdir(parents=True, exist_ok=True)
        ready_to_index = self._downloaded() - self._indexed()
        print(ready_to_index)
        if not ready_to_index:
            return False
        language_references = self.indexer.save_metadata(book_id_set=ready_to_index)
        print(language_references)
        if not language_references:
            return False
        self.inverted_index.build_index_for_books(ready_to_index, language_references)
        for book_id in ready_to_index:
            with open(self.index_path, "a", encoding="utf-8") as f:
                f.write(f"{book_id}\n")
