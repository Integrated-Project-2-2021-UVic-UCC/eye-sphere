#include <Servo.h>
//
//#define arribaR 155;
//#define arribaL 25;
//#define abajoR 25;
//#define arribaL 155;
//#define centro 90;


Servo izquierda;  // create servo object to control a servo
Servo derecha;
int pos;
int pos_anterior=90;
char a;
int n;

void moure_up(int pos){
    for(int i=pos_anterior;i<=pos;i++){
        derecha.write(i);
        izquierda.write(180- i);
        delay(8);
      }
    pos_anterior=pos;
  }

void moure_down(int pos){
    for(int i=pos_anterior;i>=pos;i--){
        derecha.write(i);
        izquierda.write(180- i);
        delay(8);
      }
    pos_anterior=pos;
  }


void setup() {
  Serial.begin(9600);
  derecha.attach(7);  // attaches the servo on pin 9 to the servo object
  izquierda.attach(8);
  derecha.write(90);
  izquierda.write(90);
}

void loop() {//90 centro, 0 abajo, 180 arriba
  
  if (Serial.available() > 0) {
    //Se crea una variable que servirá como buffer
    String bufferString = "";
    //int n=0;
    a='0';
    a=Serial.read();
    if (a=='X'){
      a=Serial.read();
      //int cont=1;
      while(a!='Y'){
        bufferString += a;
        //n+=(a-48)*cont;
        //cont=cont*10;
        a=Serial.read();
      }
      Serial.println(bufferString);
      n=bufferString.toInt();
      Serial.println(n);
      if (n>130){n=130;}
      if (n<20){n=20;}
      if (n>pos_anterior){
        moure_up(n);
        }
      else{
        moure_down(n);
        }
    }
    else{
      while (a!='Y'){
        a=Serial.read();
      }
    }
  }
}
