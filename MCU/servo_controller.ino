 
#include <Servo.h>

Servo pitch; 
Servo yaw;
Servo roll;

int pitchdata;
int yawdata;
int rolldata;

int rcv = 0;

void setup()
{
  //attaching the different servos to pyhsical pins on the MCU 
  pitch.attach(9);
  yaw.attach(10);  
  roll.attach(11);
  // Setting a BAUD-rate
  Serial.begin(115200);
}

void loop()
{
  while (Serial.available()){
    pitchdata = Serial.parseInt();
    yawdata = Serial.parseInt();
    rolldata = Serial.parseInt();
    
    if (Serial.read() == '\n') {
      String s = String(String(pitchdata,DEC) + "," + String(yawdata,DEC) + "," + String(rolldata,DEC) +String('\n'));
      Serial.println(s);
    }
    pitch.writeMicroseconds(pitchdata);
    yaw.writeMicroseconds(yawdata);
    roll.writeMicroseconds(rolldata);
  }
}

