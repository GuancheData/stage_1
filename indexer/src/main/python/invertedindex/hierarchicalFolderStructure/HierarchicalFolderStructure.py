import os

from pathlib import Path

from indexer.src.main.python.invertedindex.InvertedIndexDatamartContainer import InvertedIndexDatamartContainer


class HierarchicalFolderStructure(InvertedIndexDatamartContainer):
    def __init__(self, downloadedBooksPath = "../../../../datalake", route = "../../../../Inverted_index"):
        super().__init__(downloadedBooksPath)
        self.route = Path(route)
        self.route.mkdir(parents=True, exist_ok=True)
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            (self.route / letter).mkdir(exist_ok=True)

    def saveIndexForBook(self, bookId, positionDict, language_references):
        reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
        files_data = {}
        for word, positions in positionDict.items():
            if not word in reserved_names:
                continue
            firstWord = word[0].upper()
            if not firstWord.isalpha() or firstWord not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                continue
            file_path = os.path.join(self.route, firstWord, f"{word}.txt")
            files_data.setdefault(file_path, []).append(f"{bookId},{len(positions)},{positions}\n")

        for file_path, lines in files_data.items():
            with open(file_path, 'a', encoding='utf-8') as f:
                f.writelines(lines)