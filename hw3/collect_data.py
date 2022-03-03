from base64 import encode
from cmath import inf
import requests
from bs4 import BeautifulSoup
from pprint import pprint

def parse_salary(salary):
    min = 0
    max = 0

    if salary == "Не указано":
        return min, max
    elif salary.startswith("от", 0, 2):
        salary = salary.replace("руб.", "").replace("от", "").replace(" ", "").replace(" ", "")
        min = float(salary)
        max = 1000000000
    elif salary.startswith("до", 0, 2):
        salary = salary.replace("руб.", "").replace("до", "").replace(" ", "").replace(" ", "")
        min = 0
        max = float(salary)
    else:
        salary = salary.replace("руб.", "").replace(" ", "").replace(" ", "")
        sal_range = salary.split("–")
        min, max = float(sal_range[0]), float(sal_range[1])
    return min, max

def collect_data(base_url, headers, pages):
    for i in range(pages):
        if i == 0:
            url = f'{base_url}/vacancies/finansist'
        else:
            url = f'{base_url}/vacancies/finansist?page={i}'

        response = requests.get(url, headers=headers)
        dom = BeautifulSoup(response.text, 'html.parser')

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
            min_salary, max_salary = parse_salary(salary)
            vacancy_link = info['href']
            employer_link = base_url + vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})['href']
            
            vacancy_data['title'] = title
            vacancy_data['min_salary'] = min_salary
            vacancy_data['max_salary'] = max_salary
            vacancy_data['vacancy_link'] = vacancy_link
            vacancy_data['employer_link'] = employer_link

            vacancies_list.append(vacancy_data)
    return vacancies_list