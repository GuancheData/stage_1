from indexer.invertedindex.hierarchicalFolderStructure.StopWords import StopWords

if __name__ == "__main__":
    stopwords = StopWords(r"C:\Users\enriq\PycharmProjects\SearchEngine\crawler\src\main\python\datalake", "../control/HierarchicalFolderStructure/datamart/",)
    stopwords.cleanStopWords()
    print("Cleaned stop words")