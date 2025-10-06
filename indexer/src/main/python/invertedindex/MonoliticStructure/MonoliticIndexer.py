import json
import os
from pathlib import Path
from indexer.src.main.python.invertedindex.InvertedIndexDatamartContainer import InvertedIndexDatamartContainer


class MonoliticIndexer(InvertedIndexDatamartContainer):
    def __init__(self, output_json_path = "../../../../Inverted_index", downloaded_books_path = "../../../../datalake"):
        super().__init__(downloaded_books_path)
        self.output_json_path = output_json_path
        self.output_json_file_path = Path(self.output_json_path) / "inverted_index.json"
        self.inverted_index = {}

    def saveIndexForBook(self, bookId, positionDict, language_references):

        self.bookId = bookId
        self.positionDict = positionDict

        for word, positions in self.positionDict.items():
            if word not in self.inverted_index:
                self.inverted_index[word] = {}
            self.inverted_index[word][bookId] = {
                'positions': positions,
                'frequency': len(positions)
            }

    def buildIndexForBooks(self, idSet, language_references):
        super().buildIndexForBooks(idSet, language_references)
        self._save()

    def _save(self):
        if not os.path.exists(self.output_json_path):
            Path(self.output_json_path).mkdir(parents=True, exist_ok=True)
        if os.path.exists(self.output_json_file_path):
            with open(self.output_json_file_path, 'r') as file:
                try:
                    existing_index = json.load(file)
                except json.JSONDecodeError:
                    existing_index = {}
        else:
            existing_index = {}
        existing_index.update(self.inverted_index)
        with open(self.output_json_file_path, 'w') as file:
            if existing_index:
                json.dump(existing_index, file, indent=2)
