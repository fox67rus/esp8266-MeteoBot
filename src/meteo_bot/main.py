import telebot
from telebot import types
from random import choice

from extensions import TOKEN, get_local_weather_data, get_weather_sensitivity, get_weather_from_yandex, \
    get_moon_forecast
from configs import WIND_DIRECTION, WEATHER_DESCRIPTION, weather_facts

bot = telebot.TeleBot(TOKEN)


# Обработка команд
@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    # print(f'{message.chat.username}'+message.text)

    text = f'Добрейшего времени суток вам, {message.chat.first_name}!\n\n'
    bot.send_message(message.chat.id, text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🌡️ Данные с датчика')
    btn2 = types.KeyboardButton('😵 Медицинский прогноз')
    btn3 = types.KeyboardButton('🌐 Данные из Интернета')
    btn4 = types.KeyboardButton('🌜 Фазы Луны')

    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, 'Выберете необходимое действие или отправьте команду /help',
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    # print(f'{message.chat.username}'+message.text)

    text = f'Нажмите на кнопку для получения интересующей информации.\n' \
           f'Список доступных команд:\n' \
           f'Введите команду /temp для вывода данных с датчика.\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['temp'])
def command_temp(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Получаем данные с датчика...')
    text = get_local_weather_data()
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['fact'])
def command_fact(message: telebot.types.Message):
    # print(f'{message.chat.username}' + message.text)

    bot.send_message(message.chat.id, 'А вы знали, что... \n')
    text = choice(weather_facts)
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def text_message(message: telebot.types.Message):
    # print(f'{message.chat.username}' + message.text)

    if message.text == '🌡️ Данные с датчика':
        bot.send_message(message.chat.id, 'Получаем данные с датчика...')
        text = get_local_weather_data()
        bot.send_message(message.chat.id, text)

    elif message.text == '😵 Медицинский прогноз':
        text = get_weather_sensitivity()
        bot.send_message(message.from_user.id, text, parse_mode='Markdown')
    elif message.text == '🌜 Фазы Луны':
        text = get_moon_forecast()
        bot.send_message(message.from_user.id, text, parse_mode='Markdown')
    elif message.text == '🌐 Данные из Интернета':
        weather_data = get_weather_from_yandex()
        fact = weather_data['fact']
        text = f'Температура: {fact["temp"]} °C.\n' \
               f'Но одеваться нужно на {fact["feels_like"]} °C.\n' \
               f'За окном {WEATHER_DESCRIPTION[fact["condition"]]}.\n\n' \
               f'Влажность: {fact["humidity"]} %.\n' \
               f'Давление: {fact["pressure_mm"]} мм рт. ст.\n' \
               f'Ветер дует {WIND_DIRECTION[fact["wind_dir"]]} со скоростью {fact["wind_speed"]} м/с. ' \
               f'Порывы до {fact["wind_gust"]} м/с.\n'

        bot.send_message(message.from_user.id, text, parse_mode='Markdown')

    else:
        bot.send_message(message.from_user.id, '\nВведите /help для вывода доступных команд')


try:
    bot.polling(none_stop=True)
except ConnectionError as e:
    print('Ошибка подключения к боту:', e)
