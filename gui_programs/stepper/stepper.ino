/*
 * velocidades
 * Lento=800
 * normal=500 microseconds
 * rapido=200
 */

#include <SoftwareSerial.h>

SoftwareSerial BT(2,3);
int dir=8;
int st=9;
int vuelta=200*16;
int v=0;


void setup() {
  Serial.begin(9600);
  BT.begin(9600);
  pinMode(dir,OUTPUT);
  pinMode(st,OUTPUT);

}

void loop() {
  if (BT.available() > 0) {
    //Se crea una variable que servirá como buffer
    char d;
    d=BT.read();
    if (d=='R'){digitalWrite(dir,LOW);}
    else if(d=='L') {digitalWrite(dir,HIGH);}
    else{
      v=(d-48)*100;
      if (v>0){
          digitalWrite(st,HIGH);
          delayMicroseconds(v);
          digitalWrite(st,LOW);
          delayMicroseconds(v);
      }
    }
  }
  else{
    if (v>0){
        digitalWrite(st,HIGH);
        delayMicroseconds(v);
        digitalWrite(st,LOW);
        delayMicroseconds(v);
    }
  }
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
