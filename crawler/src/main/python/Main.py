from CrawlerController import CrawlerController
from crawler.src.main.python.storage.BookStorageId import BookStorageId

if __name__ == "__main__":
    #storage = BookStorageDate("datalake")

    crawler = CrawlerController(50, datalakeStructure="id")
    crawler.download(15)