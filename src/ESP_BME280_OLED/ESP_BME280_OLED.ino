#include <ESP8266WiFi.h>                                // Подключаем библиотеку ESP8266WiFi
#include <Wire.h>                                       // Подключаем библиотеку Wire
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_BME280.h>                            // Подключаем библиотеку Adafruit_BME280
#include <Adafruit_Sensor.h>                            // Подключаем библиотеку Adafruit_Sensor
#include "config.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define SEALEVELPRESSURE_HPA (1013.25)                  // Задаем высоту
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire);
 
Adafruit_BME280 bme;                                    // Установка связи по интерфейсу I2C
 
const char* ssid = WIFI_SSID;                           // Название WiFi сети
const char* password = WIFI_PASSWORD;                   // Пароль от WiFi сети
 
WiFiServer server(80);                                  // Указываем порт Web-сервера
String header;
String sTemp = "";
String sHumi = "";
String sPress = "";

String floatToString(float x, byte precision = 2) {
  char tmp[50];
  dtostrf(x, 0, precision, tmp);
  return String(tmp);
}
 
void setup() {
  Serial.begin(115200);                                 // Скорость передачи 115200
  bool status;
                                                       
  if (!bme.begin(0x76)) {                               // Проверка инициализации датчика
    Serial.println("Could not find a valid BME280 sensor, check wiring!"); // Печать ошибки инициализации.
    while (1);                                          // Зацикливаем
  }

   if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  display.clearDisplay();
  
  Serial.print("Connecting to ");                       // Отправка в Serial port 
  Serial.println(ssid);                                 // Отправка в Serial port 
  WiFi.begin(ssid, password);                           // Подключение к WiFi Сети
  while (WiFi.status() != WL_CONNECTED) {               // Проверка подключения к WiFi сети
    delay(500);                                         // Пауза
    Serial.print(".");                                  // Отправка в Serial port 
  }
 
  Serial.println("");                                   // Отправка в Serial port 
  Serial.println("WiFi connected.");                    // Отправка в Serial port 
  Serial.println("IP address: ");                       // Отправка в Serial port 
  Serial.println(WiFi.localIP());                       // Отправка в Serial port 
  server.begin();
  
  display.setTextSize(1);                               // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);                  // Draw white text                                 
}
 
void loop(){
 display.clearDisplay();
 display.setCursor(0,0); 
   
  float temp = bme.readTemperature();
  sTemp = "Temp: "+ floatToString(temp, 0) + " *";
  float humi = bme.readHumidity();
  sHumi = "Humi: "+ floatToString(humi, 0) + " %";
  float press = bme.readPressure() / 100.0F * 0.7501;
  sPress = "Press: "+ floatToString(press, 0) + " mm";

  display.println(sTemp);
  display.println(sHumi);
  display.println(sPress);
  display.println(WiFi.localIP());  
  display.display();  
   
  WiFiClient client = server.available();               // Получаем данные, посылаемые клиентом 
 
  if (client) {                                         
    Serial.println("New Client.");                      // Отправка "Новый клиент"
    String currentLine = "";                            // Создаем строку для хранения входящих данных от клиента
    while (client.connected()) {                        // Пока есть соединение с клиентом 
      if (client.available()) {                         // Если клиент активен 
        char c = client.read();                         // Считываем посылаемую информацию в переменную "с"
        Serial.write(c);                                // Отправка в Serial port 
        header += c;
        if (c == '\n') {                                // Вывод HTML страницы 
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");          // Стандартный заголовок HT
            client.println("Content-type:text/html ");
            client.println("Connection: close");        // Соединение будет закрыто после завершения ответа
            client.println("Refresh: 60");              // Автоматическое обновление каждые 60 сек 
            client.println();
            
            client.println("<!DOCTYPE html><html>");    // Веб-страница создается с использованием HTML
            client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            client.println("<meta charset='UTF-8'>"); 
            client.println("<link rel=\"icon\" href=\"data:,\">");
                     
            client.println("<style>body { text-align: center; font-family: \"Trebuchet MS\", Arial;}");
            client.println("table { border-collapse: collapse; width:40%; margin-left:auto; margin-right:auto; }");
            client.println("th { padding: 12px; background-color: #35d4c7; color: white; }");
            client.println("tr { border: 1px solid #ddd; padding: 12px; }");
            client.println("tr:hover { background-color: #8ad9d2; }");
            client.println("td { border: none; padding: 12px; }");
            client.println(".sensor { font-weight: bold; /* color:white; background-color: #bcbcbc;*/ padding: 1px; }");
            
            client.println("</style></head><body><h1>Метеостанция на BME280 и ESP8266</h1>");
            client.println("<table><tr><th>Параметр</th><th>Показания</th></tr>");
            client.println("<tr><td>Температура</td><td><span id=\"temp\" class=\"sensor\">");
            client.println(floatToString(temp, 1));
            client.println(" °</span></td></tr>");
            client.println("<tr><td>Давление</td><td><span id=\"press\" class=\"sensor\">");
            client.println(floatToString(press, 0));
            client.println(" мм рт. ст.</span></td></tr>");
            client.println("<tr><td>Влажность</td><td><span id=\"humi\" class=\"sensor\">");
            client.println(floatToString(humi, 0));
            client.println(" %</span></td></tr></table>"); 
            client.println("</body></html>");
            
            client.println();
            break;
          } else { 
            currentLine = "";
          }
        } else if (c != '\r') {  
          currentLine += c;      
        }
      }
    }
    header = "";
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
delay(1000); 
}
