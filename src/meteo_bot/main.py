import telebot

from src.meteo_bot.access_config import TOKEN
from extensions import get_weather_data

bot = telebot.TeleBot(TOKEN)


# Обработка команд
@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    text = f'Добрейшего времени суток вам, {message.chat.first_name}!\n' \
           f'Введите команду /temp для вывода погоды.\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    text = f'Список доступных команд:\n' \
           f'Введите команду /temp для вывода погоды.\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['temp'])
def command_temp(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Получаем данные с датчика...')
    weather_data = get_weather_data()
    if weather_data:
        temperature = weather_data[0]
        humidity = weather_data[1]
        pressure = weather_data[2]
        text = f'Температура: {temperature} °C.\n' \
               f'Влажность: {humidity} %.\n' \
               f'Давление: {pressure} мм рт. ст.\n'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def repeat_text(message: telebot.types.Message):
    text = 'Введите /help для вывода доступных команд'
    bot.reply_to(message, text)


try:
    bot.polling(none_stop=True)
except ConnectionError as e:
    print('Ошибка подключения к боту:', e)
