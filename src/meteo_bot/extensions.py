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

        text = f'Температура: {temperature}.\n' \
               f'Влажность: {humidity} %.\n' \
               f'Давление: {pressure} мм рт. ст.\n'
        return text


def get_weather_from_yandex(latitude=coordinates[0], longitude=coordinates[1], API_key=yandex_API_Key):
    url = f'https://api.weather.yandex.ru/v2/informers?lat=' \
          f'{latitude}&lon={longitude}'
    headers = {'X-Yandex-API-Key': API_key}

    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        raise ConnectionException('Ошибка получения данных с Яндекс')
    else:
        weather_data = json.loads(r.text)

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

        text = f'Сейчас:\n{health_status[0]}.\n' \
               f'{health_status[1]}\n\n' \
               f'Ожидается в ближайшие 6 часов:\n{health_status[2]}\n' \
               f'{health_status[3]}'

    return text


def get_agro_forecast():
    """
    Прогноз для садоводов
    """
    url = 'https://my-calend.ru/moon-phase'
    try:
        page = requests.get(url).content
    except Exception:
        raise ConnectionException('Ошибка получения данных с сайта')
    else:
        soup = BeautifulSoup(page, 'lxml')
        moon_status = []
        table_moon_data = soup.findAll('td')

        for td in table_moon_data:
            div = td.findAll(['a', 'div', 'span'])
            for moon_data in div:
                if moon_data.text:
                    moon_status.append(moon_data.text)

        # print(f'{moon_status=}')

        soon_moon_phase = []
        soon_moon_date = []

        for soon_phase in soup.select('.moon-phase-phases-title', limit=4):
            soon_moon_phase.append(soon_phase.get_text())

        for soon_date in soup.select('.moon-phase-phases-title ~ div', limit=4):
            soon_moon_date.append(soon_date.get_text())

        soon_moon_dict = dict(zip(soon_moon_phase, soon_moon_date))
        # print(f'{soon_moon_dict=}')

        text = f'Фаза луны - {moon_status[5]} {moon_status[7]}. \n{moon_status[3]} {moon_status[4]}. ' \
               f'Освещенность - {moon_status[2]}\n\n' \
               f'Ближайшие фазы Луны:\n'

        for key, value in soon_moon_dict.items():
            text += '{1} ({0})'.format(value, key) + '\n'

        return text


if __name__ == '__main__':
    # print(f'{get_local_weather_data()}')
    # print(f'{get_weather_sensitivity()=}')
    # print(f'{get_weather_from_yandex()=}')
    get_agro_forecast()
    print(get_agro_forecast())
