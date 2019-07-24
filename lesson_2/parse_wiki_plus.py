import collections
import requests
import re

from pprint import pprint

try:
    from proxies import proxyDict
except ImportError:
    proxyDict = None


TEST_TOPIC = 'велосипед'  # название темы менять только здесь
REGEX_STATEMENT_WIKI_URL = '(?<=href=")/wiki/.+?(?=")'
BASE_WIKI_URL = 'https://ru.wikipedia.org'
RESULT_FILE_NAME = 'result.txt'
ENCODING = 'utf-8'


def return_wiki_html_by_topic(topic):
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/'
                                f'{topic.capitalize()}',
                                proxies=proxyDict)
    return wiki_request.text


def return_words(wiki_html, count=10, verbose=True):
    words = re.findall('[а-яА-Я]{3,}', wiki_html)
    words_counter = collections.Counter(words)

    if verbose:
        for word in words_counter.most_common(count):
            print(f'Слово {word[0]} встречается {word[1]} раз')

    return words_counter.most_common(count)


def return_first_wiki_url(wiki_html):
    search_result = re.search(REGEX_STATEMENT_WIKI_URL, wiki_html)
    first_wiki_url = BASE_WIKI_URL + search_result.group(0)
    return first_wiki_url


def return_wiki_html_by_url(wiki_url):
    wiki_request = requests.get(wiki_url,
                                proxies=proxyDict)
    return wiki_request.text


html_text = return_wiki_html_by_topic(TEST_TOPIC)
first_wiki_url = return_first_wiki_url(html_text)
html_text_by_first_url = return_wiki_html_by_url(first_wiki_url)
words_in_html_by_first_url = return_words(html_text_by_first_url,
                                          count=None,
                                          verbose=False)

# pprint(words_in_html_by_first_url)

with open(RESULT_FILE_NAME, 'w', encoding=ENCODING) as file_handler:
    for word, count in words_in_html_by_first_url:
        file_handler.write(f'Слово "{word}" встречается {count} раз\n')
