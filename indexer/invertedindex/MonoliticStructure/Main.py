from indexer.invertedindex.MonoliticStructure.StopWords import StopWords


if __name__ == "__main__":
    stopWords = StopWords('../../../crawler/src/main/python/datalake', './inverted_index.json')
    stopWords.cleanStopWords()
