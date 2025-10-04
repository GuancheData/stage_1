import time
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from pathlib import Path
import re
from indexer.invertedindex.MongoDb.MongoDb import MongoDB


class StopWords:
    def __init__(self,booksMetadataContentPath, databaseName, colectionName):
        self.booksMetadataContentPath = booksMetadataContentPath
        self.database = MongoDB(databaseName, colectionName)

    def cleanStopWords(self):
        route = Path(self.booksMetadataContentPath)
        booksBody = route.rglob("[0-9]*body.txt")
        stopWords = frozenset(stopwords.words("english"))

        init_time = time.perf_counter()
        for f in booksBody:
            with open(f, 'r', encoding='utf-8') as file:
                fileMatch = re.search(r"^(\d+)_", f.name).group(1)
                wordPosition = 0
                positionDict = {}
                for line in file:
                    tokens = word_tokenize(line)
                    for token in tokens:
                        if token.lower() not in stopWords and token.isalpha():
                            word = token.lower()
                            positionDict.setdefault(word, []).append(wordPosition)
                        wordPosition += 1
                self.database.insertInformation(fileMatch,positionDict)
        final_time = time.perf_counter()
        print(f"Tiempo total: {final_time - init_time:.2f} segundos")