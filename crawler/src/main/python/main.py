from crawler_controller import CrawlerController
import sys

if __name__ == "__main__":
    crawler = CrawlerController(sys.argv[1], sys.argv[2], datalake_structure="id")
    crawler.download(15)
