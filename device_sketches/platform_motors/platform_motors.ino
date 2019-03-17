// wired connections
#define HG7881_A_IA 2  // D8 --> Motor A Input A --> MOTOR A +
#define HG7881_A_IB 3  // D9 --> Motor A Input B --> MOTOR A -
#define HG7881_B_IA 5 // D10 --> Motor B Input A --> MOTOR B +
#define HG7881_B_IB 4 // D11 --> Motor B Input B --> MOTOR B -
 
// functional connections
#define MOTOR_A_PWM HG7881_A_IA // Motor A PWM Speed
#define MOTOR_A_DIR HG7881_A_IB // Motor A Direction
#define MOTOR_B_PWM HG7881_B_IA // Motor B PWM Speed
#define MOTOR_B_DIR HG7881_B_IB // Motor B Direction

// the actual values for "fast" and "slow" depend on the motor
#define PWM_SLOW 50  // arbitrary slow speed PWM duty cycle
#define PWM_FAST 250 // arbitrary fast speed PWM duty cycle
#define DIR_DELAY 1000 // brief delay for abrupt motor changes

#define TOWER_HEAD_PIN 6
#define TOWER_BASE_PIN 7

#include <Servo.h>

Servo upperServo; // верхня часть башни (вниз-вверх)
Servo bottomServo; // основа башни(влево-вправо)
int vAngle = 0;
int hAngle = 0;


void setup()
{
  Serial.begin( 9600 );
  
  pinMode( MOTOR_A_DIR, OUTPUT );
  pinMode( MOTOR_A_PWM, OUTPUT );
  
  digitalWrite( MOTOR_A_DIR, LOW );
  digitalWrite( MOTOR_A_PWM, LOW );
  
  pinMode( MOTOR_B_DIR, OUTPUT );
  pinMode( MOTOR_B_PWM, OUTPUT );
  
  digitalWrite( MOTOR_B_DIR, LOW );
  digitalWrite( MOTOR_B_PWM, LOW );

  upperServo.attach(TOWER_HEAD_PIN);  
  upperServo.write(30);
  
  bottomServo.attach(TOWER_BASE_PIN);  
  bottomServo.write(90);

}


void forward_left_wheel(int speed) {
  digitalWrite( MOTOR_A_DIR, HIGH ); // вперед
  analogWrite( MOTOR_A_PWM, speed );  
}

void backward_left_wheel(int speed) {
  digitalWrite( MOTOR_A_DIR, LOW ); // назад
  analogWrite( MOTOR_A_PWM, speed );  
}

void forward_right_wheel(int speed) {
  digitalWrite( MOTOR_B_DIR, HIGH ); // вперед
  analogWrite( MOTOR_B_PWM, speed );  
}

void backward_right_wheel(int speed) {
  digitalWrite( MOTOR_B_DIR, LOW ); // назад
  analogWrite( MOTOR_B_PWM, speed );  
}


void stop_all_wheels() {
  // остановка всех двигателей
  digitalWrite( MOTOR_A_DIR, LOW );
  digitalWrite( MOTOR_A_PWM, LOW );
  digitalWrite( MOTOR_B_DIR, LOW );
  digitalWrite( MOTOR_B_PWM, LOW );
  // ждем остановки двигателей
  delay( DIR_DELAY );
}

void fast_forward() {
  stop_all_wheels();
  // включаем двигатели согласно команде
  forward_left_wheel(PWM_FAST);
  forward_right_wheel(PWM_FAST);
}

void forward() {
  stop_all_wheels();
  // включаем двигатели согласно команде
  forward_left_wheel(PWM_SLOW);
  forward_right_wheel(PWM_SLOW);
}

void backward() {
  stop_all_wheels();
  forward_left_wheel(PWM_SLOW);
  forward_right_wheel(PWM_SLOW);
}

void fast_backward() {
  stop_all_wheels();
  backward_left_wheel(PWM_FAST);
  backward_right_wheel(PWM_FAST);
}

void turn_left_wheels() {
  forward_left_wheel(PWM_FAST);
  backward_right_wheel(PWM_FAST);
}

void turn_right_wheels() {
  backward_left_wheel(PWM_FAST);
  forward_right_wheel(PWM_FAST);
}

void turn_tower_left() {
  hAngle += 20;
  turnLeftAndRight(hAngle);
}

void turn_tower_right() {
  hAngle -= 20;
  turnLeftAndRight(hAngle);
}

void turn_tower_up() {
  vAngle -= 20;
  turnUpAndDown(vAngle);
  
}

void turn_tower_down() {
  vAngle += 20;
  turnUpAndDown(vAngle);
  
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
    //delay(50);
}


// turns head up
void turnUpAndDown(int angle) {
  
    int fixedAngle = normalizeAngle(angle);  
    if(fixedAngle > 130) {
      fixedAngle = 130;
    }
    vAngle = fixedAngle;
    upperServo.write(vAngle);
    //delay(50);
}


void print_menu() {
  // draw a menu on the serial port
  Serial.println( "-----------------------------" );
  Serial.println( "MENU:" );
  Serial.println( "1) Fast forward" );
  Serial.println( "2) Forward" );
  Serial.println( "3) Soft stop (coast)" );
  Serial.println( "4) Reverse" );
  Serial.println( "5) Turn left" );
  Serial.println( "6) Turn right" ); 
  Serial.println( "7) Turn up" );
  Serial.println( "8) Turn down" ); 
  Serial.println( "-----------------------------" );  
}


void loop() {
  boolean isValidInput; // флаг что команда корректная
  print_menu();
  
  do
  {
    byte c;
    
    // get the next character from the serial port
    Serial.print( "?" );
    
    while( !Serial.available() )
      ; // Ждем пока что-то есть в буфере
     
    c = Serial.read();
    Serial.print(c);
    delay(100); // даем время буферу заполнится
    Serial.print(c);
    // Определяем какая опция выбрана
    switch( c )
    {
      case '1': // 1) Fast forward
        fast_forward();        
        isValidInput = true;// команда была правильно разобрана и выполнена
        break;      
        
      case '2': // 2) Forward      
        forward();
        isValidInput = true;
        break;      
        
      case '3': // 3) Soft stop (preferred)
        stop_all_wheels();
        isValidInput = true;
        break;    

      case '4': // 4) rev
        fast_backward();
        isValidInput = true;
        break;    

      case '5': // 4) turn left
        turn_left_wheels();
      
        isValidInput = true;
        break;    

      case '6': // 4) turn right
        turn_right_wheels();
        isValidInput = true;
        break;    
        
      case '7': // 4) turn up
        turn_tower_up();
        isValidInput = true;
        break;    

      case '8': // 4) turn down
        turn_tower_down();
        isValidInput = true;
        break;    
      case '9': // 4) turn left head
        turn_tower_left();
        isValidInput = true;
        break;    
      case '0': // 4) turn left head
        turn_tower_right();
        isValidInput = true;
        break;    

      default:
        // wrong character! display the menu again!
        isValidInput = false;
        Serial.println("Error");
        break;
    }
  } while( isValidInput == true );
  // repeat the main loop and redraw the menu...
  
}

