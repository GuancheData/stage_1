from indexer.MetadataParser import MetadataParser

if __name__ == "__main__":
    metadataParser = MetadataParser("../crawler/src/main/python/datalake", "../crawler/src/main/python/bookCounter.txt")
    metadataParser.parseMetadata()
