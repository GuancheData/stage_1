from pymongo import MongoClient, UpdateOne

from indexer.src.main.python.invertedindex.InvertedIndexDatamartContainer import InvertedIndexDatamartContainer


class MongoDB(InvertedIndexDatamartContainer):
    def __init__(self, downloadedBooksPath, databaseName = "SearchEngineInvertedIndex", collectionName = "InvertedIndex"):
        super().__init__(downloadedBooksPath)
        self.client = MongoClient('localhost')
        self.database = self.client[databaseName]
        self.collection = self.database[collectionName]
        self.collection.create_index("word", unique=True)


    def saveIndexForBook(self, bookId, positionDict, language_references):
        operaciones = []
        for palabra, positions in positionDict.items():
            operaciones.append(
                UpdateOne(
                    {"word": palabra},
                    {"$set": {f"documents.{bookId}": {
                        "frecuency": len(positions),
                        "position": positions
                    }}},
                    upsert=True
                )
            )
            if len(operaciones) >= 5000:
                self.collection.bulk_write(operaciones, ordered=False)
                operaciones.clear()
        if operaciones:
            self.collection.bulk_write(operaciones, ordered=False)