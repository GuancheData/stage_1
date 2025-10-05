from control.PipelineController import PipelineController
from indexer.src.main.python.invertedindex.MongoDb.MongoDb import MongoDB
from indexer.src.main.python.metadata.parser.MetadataParser import MetadataParser
from indexer.src.main.python.metadata.storage.json.MetadataJSONContainer import MetadataJSONContainer

'''if __name__ == '__main__':
    controller = PipelineController(total_books=50, metadata_storage_mode=MetadataSQLiteDB(MetadataParser("../control/datalake"), "METADATA.db"))
    controller.pipeline(books_to_download=43)'''

if __name__ == '__main__':
    pc = PipelineController(total_books=50000, metadata_storage_mode=MetadataJSONContainer(MetadataParser("../control/datalake"), "METADATA.json"),
                            inverted_index_storage_mode=MongoDB("../control/datalake", 'search-engine', 'invertedIndex'))
    pc.pipeline(books_to_download=50000)

'''if __name__ == '__main__':
    pc = PipelineController(total_books=50, metadata_storage_mode=MetadataCSVContainer(MetadataParser("../control/datalake"), "METADATA.csv"))
    pc.pipeline(books_to_download=43)'''

'''if __name__ == '__main__':
    pc = PipelineController(total_books=50, metadata_storage_mode=MetadataMySQLDB(MetadataParser("../control/datalake"), {'host': 'localhost', 'user': 'root', 'password': 'passwd', 'database': 'metadata'}))
    pc.pipeline(books_to_download=43)'''
