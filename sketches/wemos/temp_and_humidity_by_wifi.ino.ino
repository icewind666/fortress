#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h> // библиотека для управления устройствами по I2C 

/**
 * Читает температуру с датчика DallasTemperature
 * и данные с датчика DHT (тоже температура и влажность)
 * Показывает на LCD 16x2 экране и отправляет на сервер 
 * HTTP GET запросом.
 * 
 * Также снимает данные с PIR датчика движения.
 * 
 */ 

DHT dht(D5, DHT11);
LiquidCrystal_I2C lcd(0x27,16,2); // присваиваем имя lcd для дисплея 16х2
#define SENSOR_ID "T_DS18B20"
#define ONE_WIRE_BUS 4 // Пин на плате для датчика = 4
OneWire oneWire(ONE_WIRE_BUS);

// These wifi credentials we know
//char ssid[] = "DogsDeputat";
//char pass[] = "AF7J95rhxer";
//char ssid[] = "ASUS";
//char pass[] = "testpass";
char ssid[] = "TP-LINK_817096";
char pass[] = "87697094";

const char* api_host = "http://192.168.0.105:5000/t"; // Api host where to send data
const long interval = 200;

// создадим объект для работы с библиотекой DallasTemperature
DallasTemperature sensors(&oneWire);
int calibrationTime = 10; //Время калибровки датчика (10-60 сек. по даташиту)
long unsigned int lowIn; //Время, в которое был принят сигнал отсутствия движения(LOW)
long unsigned int pause = 5000; //Пауза, после которой движение считается оконченным
boolean lockLow = true; //Флаг. false = значит движение уже обнаружено, true - уже известно, что движения нет
boolean takeLowTime; //Флаг. Сигнализирует о необходимости запомнить время начала отсутствия движения
int pirPin = 7; //вывод подключения PIR датчика

void setup()
{
  sensors.begin();
  Serial.begin(115200);
  Serial.println("Calibrating");
  // Калибровка
  dht.begin();
  pinMode(pirPin, INPUT);
  digitalWrite(pirPin, LOW);
  delay(500);

  for(int i = 0; i < calibrationTime; i++) {
      delay(1000);
  }
  
  lcd.init(); // initialize the lcd
  lcd.backlight();
  lcd.setCursor(0,1);
  lcd.print("LOADING");
  lcd.setCursor(1,0);
  lcd.print("LOADING");

  // Подключаемся к wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  int i = 0;  
  
  while (WiFi.status() != WL_CONNECTED && i++ < 5) {
    Serial.println("Waiting for wifi...");
    delay(500);
  }
  
}

// Устанавливает строку в дисплее и пишет пробелы
// чтобы очистить ее
void clear_line(int line) {
  lcd.setCursor(0, line);
  lcd.print("                ");
}

void loop() {  
  sensors.requestTemperatures();
  delay(10);

  float h = dht.readHumidity();
  // Считываем температуру
  float t = dht.readTemperature();
  // Проверка удачно прошло ли считывание.
  if (isnan(h) || isnan(t)) {
    Serial.println("Не удается считать показания");
    clear_line(0);
    lcd.print("Error");
  }
  delay(10);

  HTTPClient http;
  http.begin(api_host);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  String postData = "value="+ String(sensors.getTempCByIndex(0),DEC) + "&sensor_id=" + SENSOR_ID;
  Serial.println("T1=" + String(t,DEC) + ";H=" + String(h,DEC));
  
  if (!isnan(h) && !isnan(t)) {
    clear_line(0);
    lcd.print("T1=" + String(t,DEC) + ";H=" + String(h,DEC));
  }
  clear_line(1);
  lcd.print("T2="+String(sensors.getTempCByIndex(0),DEC));
  Serial.println(String(sensors.getTempCByIndex(0),DEC));
  http.POST(postData);
  http.writeToStream(&Serial);
  http.end();      
  delay(1000); 
}
