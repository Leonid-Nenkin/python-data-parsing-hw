import re
import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyItem
from scrapy.loader import ItemLoader



class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.start_urls = ['https://leroymerlin.ru/search/?q=обои']

    def parse(self, response):
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", "//h1/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("photos", "//picture['@id=picture-box-idgenerated-0']/source[contains(@media, 'only screen and (min-width: 1024px)') and contains (@itemprop, 'image')]/@srcset")
        yield loader.load_item()