# import salary as salary
import scrapy
from scrapy.http import HtmlResponse
from jobscraper.items import JobparserItem

class SjSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vacancy/search/?keywords=python']


    def parse_salary(self, salary):
        min = None
        max = None

        if (salary[0] == "Не указано") | (salary[0] == "По договорённости"):
            return min, max
        elif salary[0] == "от":
            salary = salary[-1].replace("руб.", "").replace(" ", "").replace(" ", "").replace("\xa0", "")
            min = float(salary)
        elif salary[0] == "до":
            salary = salary[-1].replace("руб.", "").replace(" ", "").replace(" ", "").replace("\xa0", "")
            max = float(salary)
        else:
            min = float(salary[0].replace(" ", "").replace(" ", "").replace("\xa0", ""))
            max = float(salary[4].replace(" ", "").replace(" ", "").replace("\xa0", ""))
        return min, max

    def parse(self, response: HtmlResponse):
        pos = response.url.find('vacancy')
        base_url = response.url[:pos-1]
        
        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe') and contains(@class, 'f-test-link-Dalshe')]/@href").get()
        
        try:
            next_page = base_url + next_page
        except TypeError:
            next_page = False
                
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//span['@class=_1BiPY']/a[contains(@class,'icMQ_') and contains(@class, '_6AfZ9')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name_value = response.css('h1::text').get()
        salary_value = response.xpath("//span[contains(@class, '_1OuF') and contains(@class, '_ ZON4b')]/span[contains(@class,'_2Wp8I') and contains(@class, '_1BiPY') and contains(@class, '_26ig7')]//text()").getall()
        salary_min, salary_max = self.parse_salary(salary_value)
        url_value = response.url
        yield JobparserItem(name=name_value, salary_min=salary_min, salary_max=salary_max, url=url_value)

