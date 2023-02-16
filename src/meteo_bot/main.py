import telebot
from telebot import types

from src.meteo_bot.access_config import TOKEN
from extensions import get_weather_data

bot = telebot.TeleBot(TOKEN)


# Обработка команд
@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    text = f'Добрейшего времени суток вам, {message.chat.first_name}!\n\n' \
           f'Введите команду /temp для вывода погоды.\n'
    bot.send_message(message.chat.id, text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🌡️ Данные с датчика')
    btn2 = types.KeyboardButton('🌐 Данные из Интернета')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "🌡️ Данные с датчика / 🌐 Данные из Интернета", reply_markup=markup)


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    text = f'Список доступных команд:\n' \
           f'Введите команду /temp для вывода данных с датчика.\n'
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
def text_message(message: telebot.types.Message):
    if message.text == '🌡️ Данные с датчика':
        pass
    elif message.text == '🌐 Данные из Интернета':
        bot.send_message(message.from_user.id, 'Подробная погода по ' +
                         '[ссылке](https://m.meteonova.ru/med/20429-pogoda-Karmanovo.htm)', parse_mode='Markdown')

    else:
        bot.send_message(message.from_user.id, '\nВведите /help для вывода доступных команд')


try:
    bot.polling(none_stop=True)
except ConnectionError as e:
    print('Ошибка подключения к боту:', e)
