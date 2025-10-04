import requests

class GutenbergRequest:
    baseUrl = "https://www.gutenberg.org/cache/epub"

    def getUrl(self, bookId):
        return f"{self.baseUrl}/{bookId}/pg{bookId}.txt"

    def fetchBook(self, bookId):
        response = requests.get(self.getUrl(bookId))
        if response.status_code == 200:
            return response.text
        return None
