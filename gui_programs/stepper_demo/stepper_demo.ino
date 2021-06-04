/*
 * velocidades
 * Lento=800
 * normal=500 microseconds
 * rapido=200
 */

int dir=8;
int st=9;
int vuelta=400*32;
int v=0;


void setup() {
  pinMode(dir,OUTPUT);
  pinMode(st,OUTPUT);

}

void loop() {
  digitalWrite(dir,LOW);
  for (int i=0;i<vuelta;i++){
    digitalWrite(st,HIGH);
    delayMicroseconds(800);
    digitalWrite(st,LOW);
    delayMicroseconds(800);
    }
  delay(1000);

}




/*
void loop() {
  digitalWrite(dir,LOW);
  for (int i=0;i<vuelta/16;i++){
    digitalWrite(st,HIGH);
    //delay(1);
    delayMicroseconds(800);
    digitalWrite(st,LOW);
    //delay(1);
    delayMicroseconds(800);
    }
  //delay(5);
}




String vel = "";
    int v=0;
    int cont=100;
    a=Serial.read();
    if (a=='X'){
      a=Serial.read();
      while (a!='Y'){//Serial.available() > 0) {
        vel += a;
        v+=(a-48)*cont;
        a=Serial.read();
      }
    }
    else{
      while (a!='Y'){
        a=Serial.read();
      }
    }
    velocidad=vel.toInt();
*/
