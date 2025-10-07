import sys

from indexer.src.main.python.metadata.parser.metadata_parser import MetadataParser
from indexer.src.main.python.indexer_controller import IndexerController

# from indexer.src.main.python.inverted_index.monolitic_structure.monolitic_indexer import MonoliticIndexer
from indexer.src.main.python.inverted_index.hierarchical_folder_structure.hierarchical_folder_structure import HierarchicalFolderStructure
# from indexer.src.main.python.inverted_index.mongo_db.mongo_db import MongoDB

from indexer.src.main.python.metadata.storage.csv.metadata_csv_container import MetadataCSVContainer
# from indexer.src.main.python.metadata.storage.json.metadata_json_container import MetadataJSONContainer
# from indexer.src.main.python.metadata.storage.mysql.metadata_mysqldb import MetadataMySQLDB
# from indexer.src.main.python.metadata.storage.sqlite.metadata_sqlitedb import MetadataSQLiteDB

if __name__ == '__main__':
    datalake_path = sys.argv[1]
    logs_output_path = sys.argv[2]
    inverted_index_output_path = sys.argv[3]

    indexer = IndexerController(
        MetadataCSVContainer(
            MetadataParser(datalake_path),
            inverted_index_output_path),
            HierarchicalFolderStructure(
                datalake_path,
                inverted_index_output_path),
        logs_output_path)

    indexer.index()
