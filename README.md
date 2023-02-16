# Мини метеостанция
## Оборудование
- Плата ESP8266 (NodeMCU V3, CH340G)
- Метеодатчик BME280
- OLED дисплей

## Схема подключения
...

## Подключение к ПК
1. Установить драйвер для CH340G.
2. Подключить плату USB-кабелем для передачи данных.
3. [Скачать и установить Arduino IDE](https://support.arduino.cc/hc/en-us/articles/360019833020-Download-and-install-Arduino-IDE)
4. Запустить Arduino IDE
5. Настроить поддержку ESP8266:
- перейти в меню File - Preferences - Additional Boards Manager URLs 
- добавить строки:
<code>
https://arduino.esp8266.com/stable/package_esp8266com_index.json 
https://dl.espressif.com/dl/package_esp32_index.json</code> 
</code>
- установить esp8266
6. Выбрать порт (если не определяется, то проверить драйвера и кабель).
7. Выбрать плату: Tools - Board - esp8266 - NodeMCU 1.0 (ESP-12E)