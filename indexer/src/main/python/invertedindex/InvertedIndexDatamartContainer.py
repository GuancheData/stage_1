import re
import time
from abc import ABC, abstractmethod
from pathlib import Path

from nltk import word_tokenize
from nltk.corpus import stopwords


class InvertedIndexDatamartContainer(ABC):
    def __init__(self, downloadedBooksPath):
        self.downloadedBooksPath = downloadedBooksPath

    @abstractmethod
    def saveIndexForBook(self, bookId, positionDict, language_references):
        pass

    def buildIndexForBooks(self, idSet, language_references):
        route = Path(self.downloadedBooksPath)
        init_time = time.perf_counter()

        for f in route.rglob("[0-9]*body.txt"):
            fileMatchObj = re.search(r"^(\d+)_", f.name)
            if not fileMatchObj:
                continue
            fileMatch = fileMatchObj.group(1)
            if fileMatch not in language_references:
                continue
            if int(fileMatch) not in idSet:
                continue
            print(f"[INVERTED INDEX] Indexing book {fileMatch} ({language_references[fileMatch]})...")
            book_language = language_references[fileMatch].lower()
            try:
                stopWords = frozenset(stopwords.words(book_language))
            except Exception as e:
                continue
            wordPosition = 0
            positionDict = {}
            with f.open('r', encoding='utf-8') as file:
                for line in file:
                    tokens = word_tokenize(line)
                    for token in tokens:
                        if token.isalpha() and token.lower() not in stopWords:
                            word = token.lower()
                            positionDict.setdefault(word, []).append(wordPosition)
                        wordPosition += 1
            self.saveIndexForBook(fileMatch, positionDict, language_references)
        final_time = time.perf_counter()
        print(f"[INVERTED INDEX] Total indexing time: {final_time - init_time:.2f} segundos")


"""
FUNCION INICIAL

    def buildIndexForBooks(self, language_references):
        route = Path(self.downloadedBooksPath)
        booksBody = route.rglob("[0-9]*body.txt")
        init_time = time.perf_counter()
        for f in booksBody:
            fileMatch = re.search(r"^(\d+)_", f.name).group(1)
            if fileMatch in language_references:
                book_language = language_references[fileMatch]
                stopWords = frozenset(stopwords.words(book_language))
                with open(f, 'r', encoding='utf-8') as file:
                    wordPosition = 0
                    positionDict = {}
                    for line in file:
                        tokens = word_tokenize(line)
                        for token in tokens:
                            if token.isalpha() and token.lower() not in stopWords:
                                word = token.lower()
                                positionDict.setdefault(word, []).append(wordPosition)
                            wordPosition += 1
                    self.saveIndexForBook(fileMatch, positionDict, language_references)
        final_time = time.perf_counter()
        print(f"Tiempo total: {final_time - init_time:.2f} segundos")
"""
