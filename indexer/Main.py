from indexer.MetadataParser import MetadataParser

if __name__ == "__main__":
    metadataParser = MetadataParser("../indexer/datalake", "../indexer/bookCounter.txt")
    metadataParser.parseMetadaCsv("ejemplo.csv")
