import os

from indexer.src.main.python.invertedindex.InvertedIndexDatamartContainer import InvertedIndexDatamartContainer


class HierarchicalFolderStructure(InvertedIndexDatamartContainer):
    def __init__(self, downloadedBooksPath, route):
        super().__init__(downloadedBooksPath)
        self.route = route
        os.makedirs(self.route, exist_ok=True)
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            os.makedirs(os.path.join(self.route, letter), exist_ok=True)

    def saveIndexForBook(self, bookId, positionDict, language_references):
        files_data = {}
        for word, positions in positionDict.items():
            firstWord = word[0].upper()
            if not firstWord.isalpha() or firstWord not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                continue
            file_path = os.path.join(self.route, firstWord, f"{word}.txt")
            files_data.setdefault(file_path, []).append(f"{bookId},{len(positions)},{positions}\n")

        for file_path, lines in files_data.items():
            with open(file_path, 'a', encoding='utf-8') as f:
                f.writelines(lines)