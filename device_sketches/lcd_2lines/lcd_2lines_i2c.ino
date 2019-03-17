#include <LiquidCrystal_I2C.h>

#include <Wire.h> // библиотека для управления устройствами по I2C 


LiquidCrystal_I2C lcd(0x27,16,2); // присваиваем имя lcd для дисплея 20х2


//Время калибровки датчика (10-60 сек. по даташиту)
int calibrationTime = 10;      
//Время, в которое был принят сигнал отсутствия движения(LOW)
long unsigned int lowIn;       
//Пауза, после которой движение считается оконченным
long unsigned int pause = 5000;
//Флаг. false = значит движение уже обнаружено, true - уже известно, что движения нет
boolean lockLow = true;
//Флаг. Сигнализирует о необходимости запомнить время начала отсутствия движения
boolean takeLowTime;
int pirPin = 2;    //вывод подключения PIR датчика

void setup() // процедура setup
{
  lcd.init(); // инициализация LCD дисплея
  lcd.backlight(); // включение подсветки дисплея
   
  lcd.setCursor(0,0);  // ставим курсор на 1 символ второй строки
  lcd.print("WELCOME"); // печатаем сообщение на второй строке


  Serial.begin(9600);
  pinMode(pirPin, INPUT);

  digitalWrite(pirPin, LOW);
  //дадим датчику время на калибровку

  clear_line(0);
  lcd.setCursor(0,0);
  lcd.print("Calibrating");

for(int i = 0; i < calibrationTime; i++)
  {
    Serial.print(".");
    delay(1000);
  }
  Serial.println(" done");
  clear_line(0);
  lcd.setCursor(0,1);
  lcd.print("Done");

  Serial.println("SENSOR ACTIVE");
  delay(50);  
}

void loop() // процедура loop
{

//Если обнаружено движение
  if(digitalRead(pirPin) == HIGH)
  {
    Serial.println("HIGH");
    //Если еще не вывели информацию об обнаружении
    if(lockLow)
    {
      lockLow = false;
      clear_line(0);
      lcd.print("detected");     
      delay(50);
    }        
    takeLowTime = true;
  }

  //Ели движения нет
  if(digitalRead(pirPin) == LOW)
  {      
    Serial.println("LOW");
    //Если время окончания движения еще не записано
    if(takeLowTime)
    {
      lowIn = millis();          //Сохраним время окончания движения
      takeLowTime = false;       //Изменим значения флага, чтобы больше не брать время, пока не будет нового движения
    }
    //Если время без движение превышает паузу => движение окончено
    if(!lockLow && millis() - lowIn > pause)
    { 
      //Изменяем значение флага, чтобы эта часть кода исполнилась лишь раз, до нового движения
      lockLow = true;          
      clear_line(1);
           
      lcd.print("FINISHED");
      delay(50);
    }
  }
  
}

void clear_line(int line) {
  lcd.setCursor(0, line);
  lcd.print("                ");
}

