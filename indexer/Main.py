from indexer.Indexer import Indexer

booksDir = "../crawler/src/main/python/books"
index_file = "invertedIndex.json"

indexer = Indexer(booksDir)
indexer.buildIndex()
indexer.saveIndex(index_file)

