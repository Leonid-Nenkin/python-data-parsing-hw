import requests
from bs4 import BeautifulSoup
from pprint import pprint

base_url = 'https://hh.ru'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
params = {'page': 1}
url = f'{base_url}/vacancies/finansist'

response = requests.get(url, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')
# print(response.text)

vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
vacancies_list = []

for vacancy in vacancies:
    vacancy_data = {}

    info = vacancy.find('a', {'class': 'bloko-link'})
    title = info.getText()
    try:
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
    except AttributeError:
        salary = 'Не указано'
    vacancy_link = info['href']
    employer_link = base_url + vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})['href']
    
    vacancy_data['title'] = title
    vacancy_data['salary'] = salary
    vacancy_data['vacancy_link'] = vacancy_link
    vacancy_data['employer_link'] = employer_link

    vacancies_list.append(vacancy_data)


pprint(vacancies_list)
