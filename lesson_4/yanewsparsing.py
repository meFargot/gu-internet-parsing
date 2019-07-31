# 1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
# 
# *Заголовок
# *Краткое описание
# *Ссылка на новость


REGION = 'Vladimir'


def parse_news(yanews_html):
    ''' Return list of tuples like: (Header, Description, Link)
    '''
    pass


def get_yanews_html(region):
    ''' Return string with html of news.yandex.ru/region
    '''
    pass


def print_news(parsed_news):
    ''' Print formatted news
    '''
    pass


if __name__ == "__main__":
    yanews_html = get_yanews_html(REGION)
    parsed_news = parse_news(yanews_html)
    print_news(parsed_news)
