from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobscraper import settings
from jobscraper.spiders.hhru import HhruSpider
from jobscraper.spiders.superjob import SjSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(HhruSpider)
    crawler_process.crawl(SjSpider)


    crawler_process.start()
