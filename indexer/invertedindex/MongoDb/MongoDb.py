from pymongo import MongoClient, UpdateOne


class MongoDB:
    def __init__(self, databaseName, colectionName):
        self.client = MongoClient('localhost')
        self.database = self.client[databaseName]
        self.collection = self.database[colectionName]
        self.collection.create_index("word", unique=True)


    def insertInformation(self, bookId, wordFrecuence):
        operaciones = []
        for palabra, positions in wordFrecuence.items():
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