from config import channels
from crawler.data_crawler import crawl_channel


for i in channels:
    print(crawl_channel(i))
