const int pinLED = 13;
const int pinJoyX = A0;
const int pinJoyY = A1;

int Xvalue = 0;
int Yvalue = 0;

//const int pinJoyButton = 9;

void setup() {
  //pinMode(pinJoyButton , INPUT_PULLUP); //activar resistencia pull up 
  Serial.begin(9600);
}

void loop() {
  //leer valores
  Xvalue = analogRead(pinJoyX);//va entre 0 a 1024
  delay(10);           //es necesaria una pequeña pausa entre lecturas analógicas
  Yvalue = analogRead(pinJoyY);
  //mostrar valores por serial
  Serial.print("X" );
  Serial.print(Xvalue);
  Serial.print("Y");
  Serial.print(Yvalue);
  //Serial.print(" | Pulsador: ");
  //Serial.println(buttonValue);
  delay(10);
}
