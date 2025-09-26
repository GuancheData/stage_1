class Crawler:
    def __init__(self, counter, requester, storage):
        self.counter = counter
        self.requester = requester
        self.storage = storage

    def crawlBook(self):
        i = 1
        while i <= 1000:
            bookId = self.counter.getId()
            content = self.requester.fetchBook(bookId)

            if content:
                path = self.storage.save(bookId, content)
                print(f"Book {bookId} saved at {path}")
            else:
                print(f"Book {bookId} not found")

            self.counter.increaseBookId()