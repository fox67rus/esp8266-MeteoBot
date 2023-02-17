import requests
import lxml.html
from bs4 import BeautifulSoup

from src.meteo_bot.access_config import ip
from exceptions import ConnectionException


def prepare_text_to_print(incoming_list):
    new_text = incoming_list[0]

    new_text = new_text.replace("\r", "")
    new_text = new_text.replace("\n", "")
    new_text = new_text.replace("%", "")
    new_text = new_text.replace("°", "")
    new_text = new_text.replace("мм рт. ст.", "")
    new_text = new_text.strip()

    return new_text


def get_weather_data():
    try:
        html = requests.get(ip).content
    except Exception:
        raise ConnectionException('Ошибка подключения к датчику.')
    else:
        tree = lxml.html.document_fromstring(html)
        temp = prepare_text_to_print(tree.xpath('//*[@id="temp"]/text()'))
        humi = prepare_text_to_print(tree.xpath('//*[@id="humi"]/text()'))
        press = prepare_text_to_print(tree.xpath('//*[@id="press"]/text()'))

        data_list = [temp, humi, press]

        return data_list


def prepare_message():
    weather_data = get_weather_data()
    if weather_data:
        temperature = weather_data[0]
        humidity = weather_data[1]
        pressure = weather_data[2]
        text = f'Температура: {temperature} °C.\n' \
               f'Влажность: {humidity} %.\n' \
               f'Давление: {pressure} мм рт. ст.\n'
        return text


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
        print(len(img_css))
        for img in img_css:
            health_status.append(img.get('title'))
        print(health_status)
        return health_status


if __name__ == '__main__':
    for data in get_weather_data():
        print(data)

    get_weather_sensitivity()
