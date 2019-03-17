/*
Controller for tower with 2 servos.
Horizontal and vertical stepper servos named
upperServo and bottomServo.
*/
 
#include <Servo.h> 
 
int headServoPin = 2;
int baseServoPin = 3;

// MODE = 0; listen to serial port for command. 
// MODE = 1; observe loop mode.
// MODE = 2; demo mode
int MODE = 0;

String switchCommand = "sm";

Servo upperServo; 
Servo bottomServo; 

String readString;

int vAngle;
int hAngle;

int showDemo = 0;

/**
 * Initial setup for tower
 */
void setup() 
{ 
  Serial.begin(9600);
  upperServo.attach(headServoPin);  
  upperServo.write(70);
  bottomServo.attach(baseServoPin);  
  bottomServo.write(90);
} 


/** 
 *  The main board loop.
 *  If demo mode is on - shows demo in loop.
 *  If not - we listen to serial port.
 *  Expecting format:
 *  <horizontal_angle,vertical_angle>*
 *  * is command terminator.
 *  , is delimeter
 */
void loop() 
{   
  delay(1000);
  
  if (Serial.available())  {
      String wholeString = Serial.readStringUntil(";");
      wholeString.trim();
    
      Serial.println(wholeString);
      
      if (wholeString.endsWith(";")) {
        // first check if we recieved switch mode command
        if (wholeString.startsWith(switchCommand)) {
          // split by =
          Serial.println("Got switch command");
          int delimInd = wholeString.indexOf('=');
          Serial.println(delimInd);
          if (delimInd > 0) {
            int newMode = wholeString.substring(delimInd+1).toInt();
            MODE = newMode;
            Serial.println("NewMode set = ");
            Serial.println(MODE);
            wholeString = "";
            return;
          }
        }
        else {
          if (MODE == 0) {
              int ind1 = wholeString.indexOf(',');
              hAngle = wholeString.substring(0, ind1).toInt();
              vAngle = wholeString.substring(ind1+1).toInt();
              wholeString = "";
              turnLeftAndRight(hAngle);
              turnUpAndDown(vAngle);
          }
        }
      }  
      else {     
        Serial.println("Invalid command");
      }
    }
    else {
          //usual command
          switch(MODE) {
            case 0: {
              //Serial.println("Entered case 0 section");
              delay(200);
              break;
            }
            case 1: {
              Serial.println("Entered case 1 section");
              enableObserveLoop();              
              delay(200);
              break;
            }
            case 2: {
              demo();
              break;
            }
          }
  }
} 


/**
 * Normalizing angle to [0;180]
 */
int normalizeAngle(int x) {
  int angle = x;
  if (x > 180) {
    angle = 180;
  }
  if (x < 0) {
    angle = 0;
  }
  return angle;
}


// turns head left
void turnLeftAndRight(int angle) {
    int fixedAngle = normalizeAngle(angle);  
    hAngle = fixedAngle;
    bottomServo.write(hAngle);
    delay(50);
}

/**
 * Observe loop.
 * Head looks left. Then right.
 */
void enableObserveLoop() {
  Serial.println("Observing loop...");
  
  turnLeftAndRight(70);
  
  int startAngle = 30;
  int endAngle = 140;

  for(int i = startAngle; i <= endAngle; i += 10 ) {
    turnLeftAndRight(i);
    delay(2000);
  }
  // turning back
  for(int i = endAngle; i >= startAngle; i -= 10 ) {
    turnLeftAndRight(i);
    delay(2000);
  }

}


// turns head up
void turnUpAndDown(int angle) {
  
    int fixedAngle = normalizeAngle(angle);  
    if(fixedAngle > 130) {
      fixedAngle = 130;
    }
    vAngle = fixedAngle;
    upperServo.write(vAngle);
    delay(50);
}


/**
 * Just a demo.
 * Moves head up and down. Left and right
 */
void demo() 
{

  for (int i = 20; i<=120; i+=5)
  {
    bottomServo.write(i);
    delay(500);  
  }
  for (int i = 90; i<=10; i-=5)
  {
    upperServo.write(i);  
    delay(500);
  }
}


