# 1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
# 
# *Заголовок
# *Краткое описание
# *Ссылка на новость

import requests
from bs4 import BeautifulSoup


YANEWS_BASE_URL = 'https://news.yandex.ru'
REGION = 'Vladimir'


def parse_news(yanews_html):
    ''' Return list of tuples like: (Header, Description, Link)
    '''
    soup = BeautifulSoup(yanews_html, 'html.parser')

    def is_story(class_):
        return True if 'story_view_normal' in class_ else False
    
    news_divs_list = soup.findAll('div', attrs={'class': is_story})
    not_filtered_parsed_news_list = []
    for news in news_divs_list:
        try:
            news_header = news.find('h2', attrs={'class': 'story__title'}).find('a').string
        except AttributeError:
            news_header = 'no header'
        
        try:
            news_descr = news.find('div', attrs={'class': 'story__text'}).string
        except AttributeError:
            news_descr = 'no description'

        try:
            news_url = YANEWS_BASE_URL + news.find('h2', attrs={'class': 'story__title'}).find('a')['href']
        except AttributeError:
            news_url = 'no url'

        not_filtered_parsed_news_list.append((news_header, news_descr, news_url))
    
    parsed_news_list = []
    for header, descr, url in not_filtered_parsed_news_list:
        if header == 'no header' and descr == 'no description' and url == 'no url':
            continue
        parsed_news_list.append((header, descr, url))

    return parsed_news_list


def get_yanews_html(region):
    ''' Return string with html of news.yandex.ru/region
    '''
    yanews_url = '/'.join([YANEWS_BASE_URL, region])

    # headers copy-past from browser (FireFox)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Host': 'news.yandex.ru',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }

    try:
        yanews_response = requests.get(yanews_url, headers=headers)
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)
    
    yanews_html = yanews_response.text

    return yanews_html


def print_news(parsed_news):
    ''' Print formatted news
    '''
    for news in parsed_news:
        print(f'{news[0]}\n\n{news[1]}\n\nLink: {news[2]}')
        print('='*30)


if __name__ == "__main__":
    yanews_html = get_yanews_html(REGION)
    parsed_news = parse_news(yanews_html)
    print_news(parsed_news)
