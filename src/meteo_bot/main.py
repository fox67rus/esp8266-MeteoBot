import telebot
from telebot import types

from src.meteo_bot.access_config import TOKEN
from extensions import prepare_message, get_weather_sensitivity

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
    text = f'Список доступных команд:\n' \
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
        bot.send_message(message.from_user.id, 'Подробная погода по ' +
                         '[ссылке](https://m.meteonova.ru/med/20429-pogoda-Karmanovo.htm)', parse_mode='Markdown')

    else:
        bot.send_message(message.from_user.id, '\nВведите /help для вывода доступных команд')


try:
    bot.polling(none_stop=True)
except ConnectionError as e:
    print('Ошибка подключения к боту:', e)
