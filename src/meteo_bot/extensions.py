import requests
import lxml.html
from src.meteo_bot.access_config import ip


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
    except Exception as error:
        print('Ошибка подключения к датчику.', error)
    else:
        tree = lxml.html.document_fromstring(html)
        temp = prepare_text_to_print(tree.xpath('//*[@id="temp"]/text()'))
        humi = prepare_text_to_print(tree.xpath('//*[@id="humi"]/text()'))
        press = prepare_text_to_print(tree.xpath('//*[@id="press"]/text()'))

        data_list = [temp, humi, press]

        return data_list


if __name__ == '__main__':
    for data in get_weather_data():
        print(data)
