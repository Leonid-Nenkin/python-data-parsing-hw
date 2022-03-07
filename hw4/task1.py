import requests
from lxml import html
from pymongo import MongoClient


header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"}
response = requests.get('https://lenta.ru/', headers=header)
dom = html.fromstring(response.text)

client = MongoClient('127.0.0.1', 27017)
db = client['lenta']
news = db.news

items = dom.xpath(dom.xpath("/div[@class='card-mini__title']"))
items_list = []
for item in items:
    item_info = {}
    source = 'Lenta'
    link = item.xpath(".///div[@class='card-mini__title']/@href")
    news = item.xpath(".///div[@class='card-mini__title']/text()")
    date = item.xpath(".///div[@class='card-mini__date']/text()")

    # название источника;
    # наименование новости;
    # ссылку на новость;
    # дата публикации.

    item_info['link'] = link
    item_info['source'] = source
    item_info['news'] = news
    item_info['date'] = date

    items_list.append(item_info)

news.insert_many(items_list)
