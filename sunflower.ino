#include <servo.h>

int sensorPin=A0;
int servoPin=9;
int sensorValue=0;
int servoGrad=90;
int tolerance=40;

Servo myservo;

void setup() {
  pinMode(sensorPin,INPUT);
  myservo.attach(servoPin);
  myservo.write(servoGrad);

}

void loop() {
  sensorValue <(512-tolerance)){
    if(servoGrad <180){
      servoGrad++;
    }
  }
  if(sesorValue >(512+tolerance)){
    if(servoGrad>0){
      servoGrad--;
    }
  }

}
