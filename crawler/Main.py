from crawler.Crawler import Crawler

if __name__ == "__main__":
    # TODO: Make the file path a system argument
    crawler = Crawler("bookCounter.txt")
    crawler.request()