import os

from pathlib import Path

from indexer.src.main.python.inverted_index.inverted_index_datamart_container import InvertedIndexDatamartContainer

class HierarchicalFolderStructure(InvertedIndexDatamartContainer):
    def __init__(self, datalake_path, inverted_index_output_folder_path):
        super().__init__(datalake_path)
        self.route = Path(inverted_index_output_folder_path)
        self.route.mkdir(parents=True, exist_ok=True)
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            (self.route / letter).mkdir(exist_ok=True)

    def save_index_for_book(self, book_id, position_dict, language_references):
        reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
        files_data = {}
        for word, positions in position_dict.items():
            first_word = word[0].upper()
            if word.upper() in reserved_names:
                continue
            if not first_word.isalpha() or first_word not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                continue
            file_path = os.path.join(self.route, first_word, f"{word}.txt")
            files_data.setdefault(file_path, []).append(f"{book_id},{len(positions)},{positions}\n")

        for file_path, lines in files_data.items():
            with open(file_path, 'a', encoding='utf-8') as f:
                f.writelines(lines)
