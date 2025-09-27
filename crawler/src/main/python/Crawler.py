class Crawler:
    def __init__(self, counter, requester, storage, scheduler, booksNumber):
        self.counter = counter
        self.requester = requester
        self.storage = storage
        self.scheduler = scheduler
        self.booksNumber = booksNumber

    def crawlBook(self):
        bookId = self.counter.getId()
        content = self.requester.fetchBook(bookId)

        if content:
            path = self.storage.save(bookId, content)
            if path:
                print(f"Book {bookId} saved at {path}")
            else:
                print(f"Book {bookId} not saved")
        else:
            print(f"Book {bookId} not found")

        self.counter.increaseBookId()

    def schedulerCrawl(self):
        self.scheduler.scheduleTask(self.crawlBook, self.booksNumber)