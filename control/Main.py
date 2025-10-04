from control.PipelineController import PipelineController
from indexer.src.main.python.metadata.MetadataParser import MetadataParser
from indexer.src.main.python.metadata.storage.MetadataJSONContainer import MetadataJSONContainer

'''if __name__ == '__main__':
    controller = PipelineController(total_books=50, metadata_storage_mode=MetadataSQLiteDB(MetadataParser("../control/datalake"), "METADATA.db"))
    controller.pipeline(books_to_download=43)'''

if __name__ == '__main__':
    pc = PipelineController(total_books=50, metadata_storage_mode=MetadataJSONContainer(MetadataParser("../control/datalake"), "METADATA.json"))
    pc.pipeline(books_to_download=43)

'''if __name__ == '__main__':
    pc = PipelineController(total_books=50, metadata_storage_mode=MetadataCSVContainer(MetadataParser("../control/datalake"), "METADATA.csv"))
    pc.pipeline(books_to_download=43)'''