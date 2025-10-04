from nltk.corpus import stopwords

from indexer.invertedindex.StopWords import StopWords

if __name__ == "__main__":
    stopwords = StopWords(r"C:\UNIVERSIDAD\TERCER_ANYO\BIG_DATA\SearchEngineV6\crawler\src\main\python\datalake", "indexer", "invertedIndex")
    stopwords.cleanStopWords()