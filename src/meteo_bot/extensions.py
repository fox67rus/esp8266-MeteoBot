import requests
# import lxml.html
import json
from bs4 import BeautifulSoup

from access_config import *
from exceptions import ConnectionException


def get_local_weather_data(ip=esp_ip):
    try:
        html = requests.get(ip).content
    except Exception:
        raise ConnectionException('Ошибка подключения к датчику.')
    else:
        soup = BeautifulSoup(html, 'lxml')
        temperature = soup.select_one('#temp').text
        humidity = soup.find(id='humi').contents[0]
        pressure = soup.find(id='press').contents[0]

        text = f'Температура: {temperature} °C.\n' \
               f'Влажность: {humidity} %.\n' \
               f'Давление: {pressure} мм рт. ст.\n'
        return text


def get_weather_from_yandex(latitude=coordinates[0], longitude=coordinates[1], API_key=yandex_API_Key):
    url = f'https://api.weather.yandex.ru/v2/informers?lat=' \
          f'{latitude}&lon={longitude}'
    headers = {'X-Yandex-API-Key': API_key}

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        weather_data = json.loads(r.text)
    else:
        weather_data = None

    return weather_data


def get_weather_sensitivity():
    url = 'https://www.meteonova.ru/med/20429.htm'
    try:
        page = requests.get(url).content
    except Exception:
        raise ConnectionException('Ошибка получения данных с сайта')
    else:
        health_status = []
        soup = BeautifulSoup(page, 'lxml')
        img_css = soup.select('tr.display > td.temper > img', limit=4)
        for img in img_css:
            health_status.append(img.get('title'))
        return health_status


if __name__ == '__main__':
    for data in get_local_weather_data():
        print(data)

    get_weather_sensitivity()

    weather_yandex = get_weather_from_yandex()

    fact = weather_yandex['fact']
    print(fact)
    forecast = weather_yandex['forecast']
    print(forecast)
