# import salary as salary
import scrapy
from scrapy.http import HtmlResponse
from jobscraper.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=python',
                  'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=python']

    def parse_salary(self, salary):
        min = None
        max = None

        if (salary[0] == "з/п не указана") | (salary[0] == "По договорённости"):
            return min, max
        elif (salary[0] == "от") and (not("до" in salary)):
            salary = salary[1].replace("руб.", "").replace(" ", "").replace(" ", "").replace("\xa0", "")
            min = float(salary)
        elif salary[0] == "до":
            salary = salary[1].replace("руб.", "").replace(" ", "").replace(" ", "").replace("\xa0", "")
            max = float(salary)
        else:
            min = float(salary[1].replace(" ", "").replace(" ", "").replace("\xa0", ""))
            max = float(salary[3].replace(" ", "").replace(" ", "").replace("\xa0", ""))
        return min, max

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name_value = response.css('h1::text').get()
        salary_value = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        salary_value = [s.strip() for s in salary_value]
        salary_min, salary_max = self.parse_salary(salary_value)
        url_value = response.url
        yield JobparserItem(name=name_value, salary_min=salary_min, salary_max=salary_max, url=url_value)
