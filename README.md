# esp8266-MeteoBot
Telegram-бот для вывода погоды с метеостанции на ESP8266

**Возможности:**
- получение данных (температура, влажность, давление) с датчика BME280, работающего на платформе ESP8266 и установленного на улице;
- получение дополнительных данных из сети Интернет (скорость ветра, прогноз на ближайшие дни).

**Скоро будут добавлены:**
- медицинский прогноз погоды (магнитные бури, колебания атмосферного давления и скорость изменения)
- прогноз для садоводов (фазы луны)


**Список доступных команд**
| Команда | Описание команды |
| --- | --- |
| `/start`| Инструкции по применению|
| `/help` | Список команд |
| `/temp` | Вывод данных с датчика |
| `/fact` | Интересный факт о погоде |

Для написания бота использовалась библиотека **pyTelegramBotAPI==4.10.0**

Описание работы датчика [здесь](src/ESP_BME280_OLED/README.md)
