from pymongo import MongoClient, UpdateOne

from indexer.src.main.python.inverted_index.inverted_index_datamart_container import InvertedIndexDatamartContainer


class MongoDB(InvertedIndexDatamartContainer):
    def __init__(self, datalake_path, database_name ="SearchEngineInvertedIndex", collection_name ="InvertedIndex"):
        super().__init__(datalake_path)
        self.client = MongoClient('localhost')
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]
        self.collection.create_index("word", unique=True)


    def save_index_for_book(self, book_id, position_dict, language_references):
        operaciones = []
        for palabra, positions in position_dict.items():
            operaciones.append(
                UpdateOne(
                    {"word": palabra},
                    {"$set": {f"documents.{book_id}": {
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
