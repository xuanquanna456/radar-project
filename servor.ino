#include<Servo.h>
#define trigPin 4  
#define echoPin 3
unsigned long LastChange = 0;
unsigned long debounceDelay = 100;
const int servo_pin = 9;
Servo servo;
unsigned long previous_distance = 400;
void triggerUltrasonicSensor(){
  digitalWrite(trigPin , LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin , HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin , LOW);
}
long getUltrasonicDistance(){
  long duration = pulseIn(echoPin , HIGH);
  long distance = duration / 58.0;
  if (distance > 400){
    distance = previous_distance;
  }
  else{
    distance = previous_distance * 0.6 + distance * 0.4;
    previous_distance = distance;
  }
  return distance;
}
void setup() {
  Serial.begin(115200);
  servo.attach(servo_pin);
  pinMode(trigPin , OUTPUT);
  pinMode(echoPin , INPUT);
}

void loop() {
  for (int pos = 0 ; pos <= 180 ; pos++){
    servo.write(pos);
    triggerUltrasonicSensor();
    int x = getUltrasonicDistance();
    Serial.print(x);
    Serial.print(",");
    Serial.println(pos);
    delay(10);
  }
  for (int pos = 180  ; pos >= 0 ; pos--){
    servo.write(pos);
    triggerUltrasonicSensor();
    int x = getUltrasonicDistance();
    Serial.print(x);
    Serial.print(",");
    Serial.println(pos);
    delay(10);
  }
  delay(2000);
}
