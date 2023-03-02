from bs4 import BeautifulSoup
import requests
import json
import resolution
import re

headers = {'Content-Type': 'application/json'}

pattern = re.compile('\(\+(.*?)\)')


def parse_html() -> dict:
    latest_page = get_latest_loses_page()
    results = get_loses(latest_page)


def get_latest_loses_page() -> str:

    page_upd = requests.post('http://localhost:8191/v1', json={
        "cmd": "request.get",
        "url": parse_site,
        "maxTimeout": 60000
    }, headers=headers)

    flare_solver_response = json.loads(page_upd.content)

    soup = BeautifulSoup(flare_solver_response['solution']['response'], 'html.parser')

    news_list: list = soup.find_all('div', 'content')[-1].find_all('li')
    links_list = []

    for news_elem in news_list:
        if stop_word in news_elem.text:
            link = f'{parse_site}{news_elem.find_next("a")["href"]}'
            links_list.append(link)

    return links_list[0]


def get_loses(page: str) -> dict:
    page_upd = requests.post('http://localhost:8191/v1', json={
        "cmd": "request.get",
        "url": page,
        "maxTimeout": 60000
    }, headers=headers)

    flare_solver_response = json.loads(page_upd.content)

    soup = BeautifulSoup(flare_solver_response['solution']['response'], 'html.parser')

    loses_raw = soup.find_next('div', {'id': 'aticle-content'}).find_all('p', 'justifyfull')
    content_raw = []
    for loses_raw_entry in loses_raw:
        if '-' in loses_raw_entry.text:
            content_raw.append(loses_raw_entry.text)


def parse_content(content_raw) -> dict:
    loses_dict = {}
    for content_raw_entry in content_raw:
        parse_row(loses_dict, content_raw_entry)


def parse_row(loses_dict: dict, content_raw_entry: str):
    split_list = content_raw_entry.split('-')
    loss_name_raw = split_list[0]
    loss_amount_raw = split_list[1]

    loss_name_resolved = resolve_loses_name(loss_name_raw)

    if not loss_name_resolved:
        return


def resolve_loses_name(loss_name_raw: str):
    return resolution.resolution_dict.get(loss_name_raw.strip())


def resolve_loses_amount(loss_amount_raw: str):
    amount_closing_index = loss_amount_raw.rfind(')')
    amount_to_parse = loss_amount_raw[: amount_closing_index]

    amount_split = amount_to_parse.split(' ')

    if len(amount_split) > 2:
        amount_split = amount_split[-2:]  217 (+2)
    
    daily_amount = amount_split[0]
    matched = pattern.match(amount_split[1])
    if matched: 
        delta_amount = matched.groups # finish this shit


    return resolution.resolution_dict.get(loss_name_raw.strip())

    
