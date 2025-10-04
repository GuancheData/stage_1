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


        for f in booksBody:
            init_time = time.perf_counter()
            with open(f, 'r', encoding='utf-8') as file:
                fileMatch = re.search(r"^(\d+)_", f.name).group(1)
                text = file.read()
                tokens = word_tokenize(text)
                filtered_tokens = [word.lower() for word in tokens if word.lower() not in stopWords and word.isalpha()]
                freq = dict(Counter(filtered_tokens))
                print(f"Procesando libro {fileMatch}: {len(freq)} palabras únicas")
                self.database.insertInformation(fileMatch, freq)

            final_time = time.perf_counter()
            print(f"Tiempo total: {final_time - init_time:.2f} segundos")