from pymongo import MongoClient, UpdateOne


class MongoDB:
    def __init__(self, databaseName, colectionName):
        self.client = MongoClient('localhost')
        self.database = self.client[databaseName]
        self.collection = self.database[colectionName]


    # TODO: Improve performance, this is a simple schema
    def insertInformation(self, bookId, wordFrecuence):
        operaciones = []
        for palabra, freq in wordFrecuence.items():
            operaciones.append(
                UpdateOne(
                    {"word": palabra},
                    {"$push": {"documents": {"book_id": bookId, "frequency": freq}}},
                    upsert=True
                )
            )
        self.collection.bulk_write(operaciones)