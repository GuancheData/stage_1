from indexer.src.main.python.IndexerController import IndexerController

from indexer.src.main.python.metadata.storage.MetadataJSONContainer import MetadataJSONContainer
from indexer.src.main.python.metadata.storage.MetadataCSVContainer import MetadataCSVContainer
from indexer.src.main.python.metadata.storage.MetadataMySQLDB import MetadataMySQLDB
from indexer.src.main.python.metadata.storage.MetadataSQLiteDB import MetadataSQLiteDB


if __name__ == '__main__':
    indexer = IndexerController(MetadataMySQLDB({"host": "localhost", "user": "root", "password":"root", "database": "metadata"}))
    indexer.index()
