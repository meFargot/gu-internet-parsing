# Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по
# названию города, а не по IATA коду. Пункт отправления и пункт назначения
# должны передаваться в качестве параметров. Сделать форматированный вывод,
# который содержит в себе пункт отправления, пункт назначения, дату вылета,
# цену билета (можно добавить еще другие параметры по желанию)


from argparse import ArgumentParser
import requests

from pprint import pprint


CITY_DATA_URL = 'http://api.travelpayouts.com/data/en/cities.json'
TICKETS_DATA_URL = 'http://min-prices.aviasales.ru/calendar_preload'

# получить параметры: пункт отправления, пункт назначения
parser = ArgumentParser()
parser.add_argument(
    '-f', '--from_city', type=str, required=True,
    metavar='[point of departure]',
    help='Пункт отправления'
)
parser.add_argument(
    '-t', '--to_city', type=str, required=True,
    metavar='[destination]',
    help='Пункт назначения'
)
args = parser.parse_args()

# определить IATA коды
city_data_response = requests.get(CITY_DATA_URL)
city_data_json = city_data_response.json()

from_city_iata, to_city_iata = None, None
for city in city_data_json:
    if city['name'] == args.from_city:
        from_city_iata = city['code']
    if city['name'] == args.to_city:
        to_city_iata = city['code']
    if (from_city_iata is not None) and (to_city_iata is not None):
        break

if from_city_iata is None:
    print(f'Города {args.from_city} не найдено')
    exit()
if to_city_iata is None:
    print(f'Города {args.to_city} не найдено')
    exit()

# получить дату вылета и цену билета
api_params = {
    'origin_iata': from_city_iata,
    'destination': to_city_iata,
}
tickets_data_response = requests.get(TICKETS_DATA_URL, params=api_params)
tickets_data_json = tickets_data_response.json()

# вывод данных
print(f'Origin\tDestination\tDepart date\tPrice')
for ticket in tickets_data_json['best_prices']:
    print(f'{args.from_city}\t{args.to_city}\t\t'
          f'{ticket["depart_date"]}\t{ticket["value"]}')
