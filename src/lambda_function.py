from __future__ import annotations
from bs4 import BeautifulSoup
from datetime import date
import requests
import os
import psycopg2


def lambda_handler(event, context):
    persist_stats(parse_html())


def get_stats():
    pass


def persist_stats(loses: dict):

    connection = psycopg2.connect(
               host=os.environ.get('DB_HOST'),
               database=os.environ.get('PG_DATABASE'),
               user=os.getenv('DB_USER'),
               password=os.environ.get('PG_PASSWORD'))

    connection.cursor().execute('''INSERT INTO stats(date,
    personnel_total,
    personnel_delta,
    personnel_killed,
    personnel_wounded,
    personnel_captured,
    acv,
    acv_delta,
    tanks,
    tanks_delta,
    artillery,
    artillery_delta,
    aircrafts,
    aircrafts_delta,
    helicopters,
    helicopters_delta,
    naval,
    naval_delta) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                (loses["date"],
                                 loses["total_loses"],
                                    loses["incremental_loses"],
                                    loses["killed"],
                                    loses["wounded"],
                                    loses["captured"],
                                    loses["acv"],
                                    loses["acv_delta"],
                                    loses["tanks"],
                                    loses["tanks_delta"],
                                    loses["artillery"],
                                    loses["artillery_delta"],
                                    loses["aircrafts"],
                                    loses["aircrafts_delta"],
                                    loses["helicopters"],
                                    loses["helicopters_delta"],
                                    loses["naval"],
                                    loses["naval_delta"]))
    connection.commit()
    connection.cursor().close()


def parse_html():
    URL = "https://www.minusrus.com/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    loses_dict = dict()

    loses_dict['date'] = date.today()

    large_cards = soup.find_all('div', 'card_large')

    for card in large_cards:
        text = card.find_next('div', 'card__amount').text
        parse_loses_overall(text, loses_dict)

        loses_details = card.find_next('div', 'amount-details') \
            .find_all('div', 'amount-details__item')

        parse_loses_details(loses_details, loses_dict)

    card_containers = soup.find_all('div', 'card__container')[
        0].find_all_next('div', 'card')
    parse_card_container('acv', card_containers[0], loses_dict)
    parse_card_container('tanks', card_containers[1], loses_dict)
    parse_card_container('artillery', card_containers[2], loses_dict)
    parse_card_container('aircrafts', card_containers[3], loses_dict)
    parse_card_container('helicopters', card_containers[4], loses_dict)
    parse_card_container('naval', card_containers[5], loses_dict)

    return loses_dict


def parse_loses_overall(loses_str: str, loses_dict: dict[str, int]):
    cleaned_str = loses_str.replace('\n', '').replace(
        ' ', '').replace('~', '').replace('.', '')
    cleaned_arr = cleaned_str.split('+')

    loses_dict['total_loses'] = int(cleaned_arr[0])
    loses_dict['incremental_loses'] = int(cleaned_arr[1])
    return loses_dict


def parse_loses_details(details_items: list, loses_dict: dict[str, int]):
    loses_dict['killed'] = int(
        details_items[0].text.split('~')[1].replace('.', ''))
    loses_dict['wounded'] = int(
        details_items[1].text.split('~')[1].replace('.', ''))
    loses_dict['captured'] = int(
        details_items[2].text.split('~')[1].replace('.', ''))


def parse_card_container(prefix: str, container, loses_dict: dict[str, int]):
    loses_dict[prefix] = int(container.find_next(
        'span', 'card__amount-total').text)

    delta = container.find_next('span', 'card__amount-progress')
    if delta is not None:
        loses_dict[f'{prefix}_delta'] = int(container.find_next(
            'span', 'card__amount-progress').text.replace('+', ''))
    else:
        loses_dict[f'{prefix}_delta'] = 0


if __name__ == "__main__":
    lambda_handler(None, None)
