import json
import os
from pathlib import Path
from indexer.src.main.python.inverted_index.inverted_index_datamart_container import InvertedIndexDatamartContainer


class MonoliticIndexer(InvertedIndexDatamartContainer):
    def __init__(self, datalake_path, inverted_index_output_path):
        super().__init__(datalake_path)
        self.inverted_index_output_path = inverted_index_output_path
        self.inverted_index_file_output_path = Path(self.inverted_index_output_path) / "inverted_index.json"
        self.inverted_index = {}

    def save_index_for_book(self, book_id, position_dict, language_references):
        self.bookId = book_id
        self.positionDict = position_dict

        for word, positions in self.positionDict.items():
            if word not in self.inverted_index:
                self.inverted_index[word] = {}
            self.inverted_index[word][book_id] = {
                'positions': positions,
                'frequency': len(positions)
            }

    def build_index_for_books(self, book_id_set, language_references):
        super().build_index_for_books(book_id_set, language_references)
        self._save()

    def _save(self):
        if not os.path.exists(self.inverted_index_output_path):
            Path(self.inverted_index_output_path).mkdir(parents=True, exist_ok=True)
        if os.path.exists(self.inverted_index_file_output_path):
            with open(self.inverted_index_file_output_path, 'r') as file:
                try:
                    existing_index = json.load(file)
                except json.JSONDecodeError:
                    existing_index = {}
        else:
            existing_index = {}
        existing_index.update(self.inverted_index)
        with open(self.inverted_index_file_output_path, 'w') as file:
            if existing_index:
                json.dump(existing_index, file, indent=2)
