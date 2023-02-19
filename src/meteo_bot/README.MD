## Инструкция по запуску бота на роутере Keenetic (в процессе разработки)
Настройка среды:
```bash
opkg update
opkg upgrade
opkg install python3 python3-pip cron ext-ui
python get-pip.py
```


Пакеты для бота:
```
pip install pyTelegramBotAPI
opkg install python3-lxml
```

запуск вручную:
`python /opt/etc/meteo_bot/main.py`
или
`/opt/etc/init.d/S55metbot start`

Обновление бота
```bash
wget https://raw.githubusercontent.com/fox67rus/esp8266-MeteoBot/main/src/meteo_bot/main.py --no-check-certificate -O /opt/etc/meteo_bot/main.py
wget https://raw.githubusercontent.com/fox67rus/esp8266-MeteoBot/main/src/meteo_bot/extensions.py --no-check-certificate -O /opt/etc/meteo_bot/extensions.py
wget https://raw.githubusercontent.com/fox67rus/esp8266-MeteoBot/main/src/meteo_bot/configs.py --no-check-certificate -O /opt/etc/meteo_bot/configs.py
wget https://raw.githubusercontent.com/fox67rus/esp8266-MeteoBot/main/src/meteo_bot/exceptions.py --no-check-certificate -O /opt/etc/meteo_bot/exceptions.py
```
