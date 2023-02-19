import telebot
from telebot import types

from access_config import TOKEN
from extensions import prepare_message, get_weather_sensitivity, get_weather_from_yandex
from configs import WIND_DIRECTION, WEATHER_DESCRIPTION

bot = telebot.TeleBot(TOKEN)


# Обработка команд
@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    text = f'Добрейшего времени суток вам, {message.chat.first_name}!\n\n'
    bot.send_message(message.chat.id, text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🌡️ Данные с датчика')
    btn2 = types.KeyboardButton('😵 Медицинский прогноз')
    btn3 = types.KeyboardButton('🌐 Данные из Интернета')

    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, 'Выберете необходимое действие или отправьте команду /help',
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    text = f'Нажмите на кнопку для получения интересующей информации.\n' \
           f'Список доступных команд:\n' \
           f'Введите команду /temp для вывода данных с датчика.\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['temp'])
def command_temp(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Получаем данные с датчика...')
    text = prepare_message()
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def text_message(message: telebot.types.Message):
    if message.text == '🌡️ Данные с датчика':
        bot.send_message(message.chat.id, 'Получаем данные с датчика...')
        text = prepare_message()
        bot.send_message(message.chat.id, text)

    elif message.text == '😵 Медицинский прогноз':
        weather_health_data = get_weather_sensitivity()
        if weather_health_data:
            weather_heart_now = weather_health_data[0]
            weather_magnet_now = weather_health_data[1]
            weather_heart_soon = weather_health_data[2]
            weather_magnet_soon = weather_health_data[3]

            text = f'Сейчас:\n{weather_heart_now}. \n' \
                   f'{weather_magnet_now}\n\n' \
                   f'Ожидается в ближайшие 6 часов:\n{weather_heart_soon} \n' \
                   f'{weather_magnet_soon}'
        else:
            text = 'Не удалось получить данные'

        bot.send_message(message.from_user.id, text, parse_mode='Markdown')

    elif message.text == '🌐 Данные из Интернета':
        weather_data = get_weather_from_yandex()
        # url = weather_data['info']['url']

        fact = weather_data['fact']
        print(fact)
        forecast = weather_data['forecast']
        print(forecast)

        text = f'Температура: {fact["temp"]} °C.\n' \
               f'Но одеваться нужно на {fact["feels_like"]} °C.\n' \
               f'За окном {WEATHER_DESCRIPTION[fact["condition"]]}.\n\n' \
               f'Влажность: {fact["humidity"]} %.\n' \
               f'Давление: {fact["pressure_mm"]} мм рт. ст.\n' \
               f'Ветер дует {WIND_DIRECTION[fact["wind_dir"]]} со скоростью {fact["wind_speed"]} м/с. ' \
               f'Порывы до {fact["wind_gust"]} м/с.\n'

        bot.send_message(message.from_user.id, text, parse_mode='Markdown')

        # bot.send_message(message.from_user.id, 'Подробная погода по ' +
        #                  f'[ссылке]({url})', parse_mode='Markdown')

    else:
        bot.send_message(message.from_user.id, '\nВведите /help для вывода доступных команд')


try:
    bot.polling(none_stop=True)
except ConnectionError as e:
    print('Ошибка подключения к боту:', e)
