import json
import os

from indexer.src.main.python.invertedindex.InvertedIndexDatamartContainer import InvertedIndexDatamartContainer


class MonoliticIndexer(InvertedIndexDatamartContainer):
    def __init__(self, downloadedBooksPath, output_json_path):
        self.output_json_path = output_json_path
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

        self._save()

    def _save(self):
        if os.path.exists(self.output_json_path):
            with open(self.output_json_path, 'r') as file:
                try:
                    existing_index = json.load(file)
                except json.JSONDecodeError:
                    existing_index = {}
        else:
            existing_index = {}
        existing_index.update(self.inverted_index)
        with open(self.output_json_path, 'w') as file:
            if existing_index:
                json.dump(existing_index, file, indent=2)
