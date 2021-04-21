const int dirPin = 8;
const int stepPin = 9;
 
const int steps = 200;
int stepDelay;
 
void setup() {
   // Marcar los pines como salida
   pinMode(dirPin, OUTPUT);
   pinMode(stepPin, OUTPUT);
}
 
void loop() {
   //Activar una direccion y fijar la velocidad con stepDelay
   digitalWrite(dirPin, HIGH);
   stepDelay = 250;
   // Giramos 200 pulsos para hacer una vuelta completa
   for (int x = 0; x < steps; x++) {
      digitalWrite(stepPin, HIGH);
      //delayMicroseconds(stepDelay);
      delay(1);
      digitalWrite(stepPin, LOW);
      //delayMicroseconds(stepDelay);
      delay(1);
   }
   delay(1000);
 
   //Cambiamos la direccion y aumentamos la velocidad
   digitalWrite(dirPin, LOW);
   stepDelay = 800;
   // Giramos 400 pulsos para hacer dos vueltas completas
   for (int x = 0; x < 400; x++) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(stepDelay);
      //delay(2);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(stepDelay);
      //delay(2);
   }
   delay(1000);
}
