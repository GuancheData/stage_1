from BookCounter import BookCounter
from BookStorageDate import BookStorage
from Crawler import Crawler
from GutenbergRequest import GutenbergRequest
from BookRequestSchedule import BookRequestSchedule
from BookStorageId import BookStorageId
import sys

if __name__ == "__main__":
    counter = BookCounter("bookCounter.txt")
    requester = GutenbergRequest()
    storage = BookStorageId("datalake")
    scheduler = BookRequestSchedule()

    crawler = Crawler(counter, requester, storage, scheduler,  int(5))
    crawler.schedulerCrawl()
