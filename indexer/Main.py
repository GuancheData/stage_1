from indexer.MetadataParser import MetadataParser

if __name__ == "__main__":
    metadataParser = MetadataParser("datalake", "bookCounter.txt")
    metadataParser.parseMetadata()
