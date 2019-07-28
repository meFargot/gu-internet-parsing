from time import sleep
from pprint import pprint

import requests
from lxml import html, etree
import csv


HH_SEARCH_URL = 'https://hh.ru/search/vacancy'
HH_BASE_URL = 'https://hh.ru'
VACANCY_FILENAME = 'vacancy.csv'
HH_HEADERS = {
    'accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,image/'
               'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'),
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://hh.ru/',
    'upgrade-insecure-requests': '1',
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                   '537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/'
                   '537.36')
}


def get_hh_search_html(search_string):
    ''' Возвращает html страницу со списком вакансий в результате поиска по
        search_string
    '''
    get_params = {
        'area': '1',
        'text': search_string,
        'from': 'suggest_post'
    }
    response = requests.get(HH_SEARCH_URL, params=get_params,
                            headers=HH_HEADERS)
    return response.text


def get_next_url(text_html):
    ''' Возвращает ссылку на следующую страницу с вакансиями
    '''
    root = html.fromstring(text_html)
    next_url = root.xpath("//a[contains(@class, 'bloko-button "
                          "HH-Pager-Controls-Next HH-Pager-Control')]/@href")
    return HH_BASE_URL + next_url[0]


def parse_vacancy(text_html):
    ''' Возвращает список кортежей вида: (наименование вакансии, зарплата,
        ссылка на вакансию)
    '''
    root = html.fromstring(text_html)
    vacancy_div_list = root.xpath("//div[contains(@class, "
                                  "'vacancy-serp-item__row "
                                  "vacancy-serp-item__row_header')]")

    vacancy_list = []

    for vacancy_div in vacancy_div_list:
        vacancy_div_string = etree.tostring(vacancy_div)
        current_div = html.fromstring(vacancy_div_string)

        vacancy_name = current_div.xpath("//a/text()")
        vacancy_salary = current_div.xpath(
                                       "//div[contains(@class, "
                                       "'vacancy-serp-item__compensation')]"
                                       "/text()")
        vacancy_link = current_div.xpath("//a/@href")

        if not vacancy_salary:
            vacancy_salary = ['не указана']

        vacancy_list.append((vacancy_name[0],
                             vacancy_salary[0],
                             vacancy_link[0]))

    return vacancy_list


def get_next_html(next_url):
    ''' Возвращает следующую страницу по ссылке "Дальше"
    '''
    response = requests.get(next_url, headers=HH_HEADERS)
    return response.text


SEARCH_STRING = 'программист'
PAGES = 5

print(f'Парсинг страницы: 1')
text_html = get_hh_search_html(SEARCH_STRING)
vacancy_list = parse_vacancy(text_html)
next_url = get_next_url(text_html)

for page in range(1, PAGES):
    print(f'Парсинг страницы: {page + 1}')
    sleep(3)
    text_html = get_next_html(next_url)
    vacancy_list += parse_vacancy(text_html)
    next_url = get_next_url(text_html)

with open(VACANCY_FILENAME, 'w', encoding='utf-8') as file_handler:
    writer = csv.writer(file_handler)
    writer.writerows(vacancy_list)

pprint(vacancy_list)
