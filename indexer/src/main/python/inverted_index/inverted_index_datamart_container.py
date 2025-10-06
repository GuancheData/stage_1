import re
import time
from abc import ABC, abstractmethod
from pathlib import Path

from nltk import word_tokenize
from nltk.corpus import stopwords


class InvertedIndexDatamartContainer(ABC):
    def __init__(self, datalake_path):
        self.datalake_path = datalake_path

    @abstractmethod
    def save_index_for_book(self, book_id, position_dict, language_references):
        pass

    def build_index_for_books(self, book_id_set, language_references):
        route = Path(self.datalake_path)
        init_time = time.perf_counter()

        for f in route.rglob("[0-9]*body.txt"):
            file_match_obj = re.search(r"^(\d+)_", f.name)
            if not file_match_obj:
                continue
            file_match = file_match_obj.group(1)
            if file_match not in language_references:
                continue
            if int(file_match) not in book_id_set:
                continue
            print(f"[INVERTED INDEX] Indexing book {file_match} ({language_references[file_match]})...")
            book_language = language_references[file_match].lower()
            try:
                stop_words = frozenset(stopwords.words(book_language))
            except Exception as e:
                continue
            word_position = 0
            position_dict = {}
            with f.open('r', encoding='utf-8') as file:
                for line in file:
                    tokens = word_tokenize(line)
                    for token in tokens:
                        if token.isalpha() and token.lower() not in stop_words:
                            word = token.lower()
                            position_dict.setdefault(word, []).append(word_position)
                        word_position += 1
            self.save_index_for_book(file_match, position_dict, language_references)
        final_time = time.perf_counter()
        print(f"[INVERTED INDEX] Total indexing time: {final_time - init_time:.2f} segundos")
