#include <Wire.h>

//Время калибровки датчика (10-60 сек. по даташиту)
int calibrationTime = 20;      

//Время, в которое был принят сигнал отсутствия движения(LOW)
long unsigned int lowIn;       

//Пауза, после которой движение считается оконченным
long unsigned int pause = 1000;

//Флаг. false = значит движение уже обнаружено, true - уже известно, что движения нет
boolean lockLow = true;

//Флаг. Сигнализирует о необходимости запомнить время начала отсутствия движения
boolean takeLowTime;

//вывод подключения PIR датчика
int pirPin = D2;    

void setup() {
  Serial.begin(115200);
  pinMode(pirPin, INPUT);
  pinMode(pirPin, OUTPUT);
  digitalWrite(pirPin, LOW);
    
  for(int i = 0; i < calibrationTime; i++) {//дадим датчику время на калибровку
    Serial.print(".");
    delay(1000);
  }
  Serial.println(" done");
  Serial.println("SENSOR ACTIVE");
  delay(50);  
}

void loop() {  
  if(digitalRead(pirPin) == HIGH) { //Если обнаружено движение
    Serial.println("HIGH");    
    if(lockLow) {//Если еще не вывели информацию об обнаружении
      lockLow = false;
      delay(50);
    }        
    takeLowTime = true;
  }  
  if(digitalRead(pirPin) == LOW) {//Если движения нет      
    Serial.println("LOW");    
    if(takeLowTime) { //Если время окончания движения еще не записано
      lowIn = millis();          //Сохраним время окончания движения
      takeLowTime = false;       //Изменим значения флага, чтобы больше не брать время, пока не будет нового движения
    }
    
    if(!lockLow && millis() - lowIn > pause) { //Если время без движение превышает паузу => движение окончено
      lockLow = true; //Изменяем значение флага, чтобы эта часть кода исполнилась лишь раз, до нового движения
      delay(100);
    }
  }
  delay(100);
}
