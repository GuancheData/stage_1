from CrawlerController import CrawlerController
import sys
from crawler.src.main.python.storage.BookStorageId import BookStorageId

if __name__ == "__main__":
    #storage = BookStorageDate("datalake")

    crawler = CrawlerController(sys.argv[1],
                                sys.argv[2],
                                datalakeStructure="id")
    crawler.download(15)