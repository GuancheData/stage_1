from crawler_controller import CrawlerController
import sys

if __name__ == "__main__":
    datalake_path = sys.argv[1]
    logs_output_path = sys.argv[2]
    crawler = CrawlerController(datalake_path, logs_output_path, datalake_structure="id")
    crawler.download(15)
