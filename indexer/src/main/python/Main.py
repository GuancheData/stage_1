import sys

from indexer.src.main.python.IndexerController import IndexerController
from indexer.src.main.python.invertedindex.MongoDb.MongoDb import MongoDB
from indexer.src.main.python.metadata.parser.MetadataParser import MetadataParser

from indexer.src.main.python.metadata.storage.json.MetadataJSONContainer import MetadataJSONContainer
from indexer.src.main.python.metadata.storage.csv.MetadataCSVContainer import MetadataCSVContainer
from indexer.src.main.python.metadata.storage.mysql.MetadataMySQLDB import MetadataMySQLDB
from indexer.src.main.python.metadata.storage.sqlite.MetadataSQLiteDB import MetadataSQLiteDB


if __name__ == '__main__':
    indexer = IndexerController(MetadataCSVContainer(MetadataParser(sys.argv[0]), sys.argv[1]),
                                MongoDB(sys.argv[0]), sys.argv[2])
    indexer.index()
