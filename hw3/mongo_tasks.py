from pymongo import MongoClient
from  pprint import pprint
from collect_data import collect_data

base_url = 'https://hh.ru'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
pages=2

client = MongoClient('127.0.0.1', 27017)
db = client['hh']
vacancies = db.vacancies
vacancies_list = collect_data(base_url, headers, pages)
vacancies.insert_many(vacancies_list)

required_salary = 70000
result = vacancies.find({'min_salary': {'$gt': required_salary}})

for doc in result:
    pprint(doc)

