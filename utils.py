import json
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re

seen_flats_path = 'seen_flats.txt'


def load_seen_flats():
    with open(seen_flats_path, 'r') as f:
        return json.loads(f.read())


def update_seen_flats(seen):
    with open(seen_flats_path, 'w') as f:
        f.write(json.dumps(seen))


headers = {
    i.split(": ")[0]: i.split(": ")[1] for i in """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Host: www.myhome.ge
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15
Accept-Language: ru
Referer: https://www.myhome.ge/ru/
Connection: keep-alive""".split('\n')
}


def _get_views(link):
    """Получение просмотров, количества комнат и координат квартиры"""
    s = BeautifulSoup(requests.get(link, headers=headers).text)
    views = s.select('div.d-flex.align-items-center.views')[0].find_all('span')[0].text
    flats = s.select('a.see-all-statements')[0].text
    lat = s.select('div.map-container')[0].find_all('div')[0].get('data-lat')
    long = s.select('div.map-container')[0].find_all('div')[0].get('data-lng')

    time.sleep(2)
    return views, flats, lat, long


def sendLocation(token, chat_id, lat, long, proxies=None):
    '''Send message from Bot to Telegram user/channel/group
    data = {'chat_id': chat_id,
            'text': msg,
            'parse_mode': 'Markdown'}
    r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data=data)
    return r'''
    data = {'chat_id': chat_id,
            "latitude": lat,
            "longitude": long,
            'parse_mode': 'Markdown'}
    if proxies:
        r = requests.post(f'https://api.telegram.org/bot{token}/sendLocation', data=data, proxies=proxies)
    else:
        r = requests.post(f'https://api.telegram.org/bot{token}/sendLocation', data=data)
    return r


def sendMessage(token, chat_id, msg, proxies=None):
    '''Send message from Bot to Telegram user/channel/group
    data = {'chat_id': chat_id,
            'text': msg,
            'parse_mode': 'Markdown'}
    r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data=data)
    return r'''
    data = {'chat_id': chat_id,
            'text': msg,
            'parse_mode': 'Markdown'}
    if proxies:
        r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data=data, proxies=proxies)
    else:
        r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data=data)
    return r


def get_flats_by_map(links_list, seen_flats, minutes_horizon, tg_token, tg_chat):
    for link in links_list:
        s = BeautifulSoup(requests.get(link, headers=headers).text)
        flats = s.find_all('a', {"class": "card-container"})  # количество квартир на странице
        time.sleep(3)

        for i in flats:
            time_ = i.find_all('div', {"class": "statement-date"})[0].text
            dif = (datetime.now() - datetime.strptime("2022 " + time_.replace('Сен.', "Sep").replace('Окт.', "Oct").replace('Ноя.', "Nov"), '%Y %d %b %H:%M')).total_seconds()

            if dif < minutes_horizon * 60:
                href = i.get('href')
                price = i.find_all('b', {"class": "item-price-usd mr-2"})
                sq = i.find_all("div", {"class": "item-size"})[0].text
                id_ = re.findall("/([0-9]{8})/", href)[0]
                img_ = i.find_all('img')[0].get('data-src')
                params = ', '.join([j.text for j in i.find_all('div', {"class": "d-flex options"})[0].find_all('span')])

                if id_ not in seen_flats:
                    print(dif, time_, price, href)
                    views, items, lat, long = _get_views(href)
                    # отправка соообщений в чат (данные по квартире + локация квартиры)
                    sendMessage(tg_token, tg_chat, f"[${price[0].text}]({img_})\nПросмотры - {views}\n{items}\n{params}\n{sq}\n{time_}\n\n[ссылка на квартиру]({href})")
                    sendLocation(tg_token, tg_chat, lat, long)
                    seen_flats[id_] = href

    return seen_flats
