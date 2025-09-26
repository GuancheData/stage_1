from BookCounter import BookCounter
from BookStorage import BookStorage
from Crawler import Crawler
from GutenbergRequest import GutenbergRequest

if __name__ == "__main__":
    counter = BookCounter("bookCounter.txt")
    requester = GutenbergRequest()
    storage = BookStorage("books")

    crawler = Crawler(counter, requester, storage)
    crawler.crawlBook()