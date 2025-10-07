import sys

from indexer.src.main.python.indexer_controller import IndexerController
from indexer.src.main.python.inverted_index.mongo_db.mongo_db import MongoDB
from indexer.src.main.python.metadata.parser.metadata_parser import MetadataParser

from indexer.src.main.python.metadata.storage.json.metadata_json_container import MetadataJSONContainer
from indexer.src.main.python.metadata.storage.csv.metadata_csv_container import MetadataCSVContainer
from indexer.src.main.python.metadata.storage.mysql.metadata_mysqldb import MetadataMySQLDB
from indexer.src.main.python.metadata.storage.sqlite.metadata_sqlitedb import MetadataSQLiteDB


if __name__ == '__main__':
    indexer = IndexerController(MetadataCSVContainer(MetadataParser(sys.argv[1]), sys.argv[2]),
                                MongoDB(sys.argv[1]), sys.argv[3])
    indexer.index()
