// ** TEST FOR DRIVING FORWARD 1 METRE **
#include <PID_v1.h>

//double P1 = 2;
//double I1 = 24;
//double D1 = 0.6;

double P1 = 1;
double I1 = 15;
double D1 = 0.2;

double Setpoint1, Input1, Output1, Output1a;
PID PID1(&Input1, &Output1, &Setpoint1, P1, I1, D1, DIRECT);


//double P2 = 2;
//double I2 = 24;
//double D2 = 0.6;

double P2 = 1;
double I2 = 15;
double D2 = 0.2;

double Setpoint2, Input2, Output2, Output2a;
PID PID2(&Input2, &Output2, &Setpoint2, P2, I2, D2, DIRECT);


float demand1;
float demand2;

unsigned long currentMillis;
unsigned long previousMillis;

// wheel encoder interrupts 

#define encoder0PinA 2 //encoder 1
#define encoder0PinB 3

#define encoder1PinA 18 //encoder 2
#define encoder1PinB 19

volatile long encoder0Pos = 0;  //encoder 1
volatile long encoder1Pos = 0;  //encoder 2

void setup() {
  
  pinMode(4, OUTPUT); // motor PWM pins
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);

  pinMode(encoder0PinA, INPUT_PULLUP); //encoder pins
  pinMode(encoder0PinB, INPUT_PULLUP); //encoder pins
  pinMode(encoder1PinA, INPUT_PULLUP); //encoder pins
  pinMode(encoder1PinB, INPUT_PULLUP); //encoder pins

  attachInterrupt(0, doEncoderA, CHANGE);
  attachInterrupt(1, doEncoderB, CHANGE);
  
  attachInterrupt(4, doEncoderC, CHANGE);
  attachInterrupt(5, doEncoderD, CHANGE);

  PID1.SetMode(AUTOMATIC);
  PID1.SetOutputLimits(-250, 250);
  PID1.SetSampleTime(10);

  PID2.SetMode(AUTOMATIC);
  PID2.SetOutputLimits(-250, 250);
  PID2.SetSampleTime(10);

  Serial.begin(115200);
}

void loop() {
  currentMillis = millis();

  if (currentMillis - previousMillis >= 10){
    previousMillis = currentMillis;
    if (Serial.available()>0){
      char c = Serial.read();
      
      if (c == 'a'){
        // drive meter test
        demand1 = 10000; // 1509 , 3018
        demand2 = 10000;
      }
      else if (c == 'z'){
        demand1 = 0;
        demand2 = 0;
    }
    }

    Serial.print(encoder0Pos);
    Serial.print(" , ");
    Serial.println(encoder1Pos);

    Setpoint1 = demand1;
    Input1 = encoder0Pos;
    PID1.Compute();

    Setpoint2 = demand2;
    Input2 = encoder1Pos;
    PID2.Compute();

    // drive motor 
    if (Output1 > 0){
      Output1a = abs(Output1);
      analogWrite(6, Output1a);
      analogWrite(7, 0);
    }
    else if (Output1 < 0){
      Output1a = abs(Output1);
      analogWrite(7, Output1a);
      analogWrite(6, 0);
    }
    else {
      analogWrite(7, 0);
      analogWrite(7, 0);
    }

    // other motor 
    if (Output2 > 0){
      Output2a = abs(Output2);
      analogWrite(5, Output2a);
      analogWrite(4, 0);
    }
    else if (Output2 < 0){
      Output2a = abs(Output2);
      analogWrite(4, Output2a);
      analogWrite(5, 0);
    }
    else {
      analogWrite(4, 0);
      analogWrite(5, 0);
    }
  }
}


// ************** encoders interrupts **************

// ************* encoder 1 ************************

void doEncoderA(){
  // look for a low-to-high on channel A 
  if (digitalRead(encoder0PinA) == HIGH){
    // check channel B to see which way encoder is turning 
    if (digitalRead(encoder0PinB) == LOW){
      encoder0Pos = encoder0Pos + 1;        // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;        // CCW
    }
  }
  else{   // must be a high-to-low edge on channel A
    // check channel B to see which way encoder is turning 
    if (digitalRead(encoder0PinB) == HIGH){
      encoder0Pos = encoder0Pos + 1;        // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;        // CCW
    }
  }
}

void doEncoderB(){
  // look for a low-to-high on channel B 
  if (digitalRead(encoder0PinB) == HIGH){
    // check channel A to see which way encoder is turning 
    if (digitalRead(encoder0PinA) == HIGH){
      encoder0Pos = encoder0Pos + 1;        // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;        // CCW
    }
  }
  else{   // must be a high-to-low edge on channel B
    // check channel A to see which way encoder is turning 
    if (digitalRead(encoder0PinA) == LOW){
      encoder0Pos = encoder0Pos + 1;        // CW
    }
    else {
      encoder0Pos = encoder0Pos - 1;        // CCW
    }
  }
}

// ************* encoder 2 ************************

void doEncoderC(){
  // look for a low-to-high on channel A 
  if (digitalRead(encoder1PinA) == HIGH){
    // check channel B to see which way encoder is turning 
    if (digitalRead(encoder1PinB) == LOW){
      encoder1Pos = encoder1Pos - 1;        // CW
    }
    else {
      encoder1Pos = encoder1Pos + 1;        // CCW
    }
  }
  else{   // must be a high-to-low edge on channel A
    // check channel B to see which way encoder is turning 
    if (digitalRead(encoder1PinB) == HIGH){
      encoder1Pos = encoder1Pos - 1;        // CW
    }
    else {
      encoder1Pos = encoder1Pos + 1;        // CCW
    }
  }
}

void doEncoderD(){
  // look for a low-to-high on channel B 
  if (digitalRead(encoder1PinB) == HIGH){
    // check channel A to see which way encoder is turning 
    if (digitalRead(encoder1PinA) == HIGH){
      encoder1Pos = encoder1Pos - 1;        // CW
    }
    else {
      encoder1Pos = encoder1Pos + 1;        // CCW
    }
  }
  else{   // must be a high-to-low edge on channel B
    // check channel A to see which way encoder is turning 
    if (digitalRead(encoder1PinA) == LOW){
      encoder1Pos = encoder1Pos - 1;        // CW
    }
    else {
      encoder1Pos = encoder1Pos + 1;        // CCW
    }
  }
}
