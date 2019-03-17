#define ledpin 1 // GPIO1/TXD01

void setup() {

pinMode(ledpin, OUTPUT);

}

void loop() {

digitalWrite(ledpin, HIGH);

delay(1000);

digitalWrite(ledpin, LOW);

delay(1000);

}
