from BookCounter import BookCounter
from BookStorage import BookStorage
from Crawler import Crawler
from GutenbergRequest import GutenbergRequest
from BookRequestSchedule import BookRequestSchedule
import sys

if __name__ == "__main__":
    counter = BookCounter("bookCounter.txt")
    requester = GutenbergRequest()
    storage = BookStorage("datalake")
    scheduler = BookRequestSchedule()

    crawler = Crawler(counter, requester, storage, scheduler,  int(sys.argv[1]))
    crawler.schedulerCrawl()
