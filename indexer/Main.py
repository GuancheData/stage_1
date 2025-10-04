from indexer.metadata.MetadataParser import MetadataParser
from indexer.metadata.storage.MetadataCSVContainer import MetadataCSVContainer
from indexer.metadata.storage.MetadataJSONContainer import MetadataJSONContainer
from indexer.metadata.storage.MetadataSQLiteDB import MetadataSQLiteDB

'''if __name__ == "__main__":
    metadataParser = MetadataParser("../indexer/datalake", "../indexer/bookCounter.txt")
    metadataParser.parseMetadaCsv("ejemplo.csv")'''

if __name__ == '__main__':
    metadataParser = MetadataParser("../crawler/src/main/python/datalake", "../control/indexed_books.txt")
    metadataParser.parseMetadata()


'''if __name__ == '__main__':
    MetadataSQLiteDB(MetadataParser("../crawler/src/main/python/datalake", "../control/indexed_books.txt"), "METADATA.db").saveMetadata()
'''

'''if __name__ == '__main__':
    MetadataJSONContainer(MetadataParser("../crawler/src/main/python/datalake", "../control/indexed_books.txt"), "METADATA.json").saveMetadata()
'''

'''if __name__ == '__main__':
    MetadataCSVContainer(MetadataParser("../crawler/src/main/python/datalake", "../control/indexed_books.txt"), "METADATA.csv").saveMetadata()
'''


