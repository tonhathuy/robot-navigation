// ** TEST FOR DRIVING FORWARD 1 METRE **
#include <ros.h>
//#include <std_msgs/String.h>
#include "geometry_msgs/Twist.h"
//#include <std_msgs/Int8.h>/
#include <geometry_msgs/Vector3Stamped.h>
#include <PID_v1.h>

ros::NodeHandle  nh;
double speed_act_left = 0; 
double speed_act_right = 0; 
float demandx, demandz;

float pwd = 100;
float pwd1 = 100;
float rad = 0.325;

void velCallback( const geometry_msgs::Twist& vel){
  demandx = vel.linear.x; 
  demandz = vel.angular.z;

  demandx = constrain(demandx, -0.5, 0.5);
  demandz = constrain(demandz, -0.5, 0.5);
}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", velCallback);
geometry_msgs::Vector3Stamped speed_msg;                                //create a "speed_msg" ROS message
ros::Publisher speed_pub("speed", &speed_msg);    

double P1 = 1;
double I1 = 15;
double D1 = 0.2;

//double P1 = 2.1;
//double I1 = 24;
//double D1 = 0.4;

double Setpoint1, Input1, Output1, Output1a;
PID PID1(&Input1, &Output1, &Setpoint1, P1, I1, D1, DIRECT);


double P2 = 1;
double I2 = 15;
double D2 = 0.2;


//double P2 = 2.1;
//double I2 = 24;
//double D2 = 0.4;

double Setpoint2, Input2, Output2, Output2a;
PID PID2(&Input2, &Output2, &Setpoint2, P2, I2, D2, DIRECT);

float demand1, demand2;

unsigned long currentMillis;
unsigned long previousMillis;

// wheel encoder interrupts 

#define encoder0PinA 2 //encoder 1
#define encoder0PinB 3

#define encoder1PinA 18 //encoder 2
#define encoder1PinB 19

volatile long encoder0Pos = 0;  //encoder 1
volatile long encoder1Pos = 0;  //encoder 2

float encoder0Driff; 
float encoder0Prev;
float encoder0Error;

float encoder1Driff; 
float encoder1Prev;
float encoder1Error;

void setup() {
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(speed_pub);
  
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

  Serial.begin(57600);
}

void loop() {
  currentMillis = millis();

  if (currentMillis - previousMillis >= 10){
    previousMillis = currentMillis;
//    if (Serial.available()>0){
//      char c = Serial.read();
//      
//      if (c == 'a'){
//        // drive meter test
//        demandx = 0.5; // 1509 , 3018
//        demandz = 0;
//      }
//      else if (c == 'b'){
//        demandx = 0.2;
//        demandz = 0;
//      }
//      else if (c == 'c'){
//        demandx = 0;
//        demandz = 1;
//      }
//      else if (c == 'd'){
//        demandx = 0;
//        demandz = -1;
//      }
//      else if (c == 'e'){
//        demandx = 0.25;
//        demandz = 1;
//      }
//      else if (c == 'f'){
//        demandx = 0.25;
//        demandz = -1;
//      }
//      else if (c == 'z'){
//        demandx = 0;
//        demandz = 0;
//      }
//    }
    demand1 = demandx - (demandz*rad);
    demand2 = demandx + (demandz*rad);

//    Serial.print(encoder0Pos);
//    Serial.print(" , ");
//    Serial.println(encoder1Pos);

    encoder0Driff = encoder0Pos - encoder0Prev;
    encoder1Driff = encoder1Pos - encoder1Prev;
    
    encoder0Error = (demand1*pwd1) - encoder0Driff;
    encoder1Error = (demand2*pwd) - encoder1Driff;

    encoder0Prev = encoder0Pos;
    encoder1Prev = encoder1Pos;

    Setpoint1 = demand1*pwd1;
    Input1 = encoder0Driff;
    PID1.Compute();

    Setpoint2 = demand2*pwd;
    Input2 = encoder1Driff;
    PID2.Compute();

    speed_act_left = encoder0Driff/pwd1 ;
    speed_act_right = encoder1Driff/pwd ;

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
    publishSpeed(10);
  }
}


//Publish function for odometry, uses a vector type message to send the data (message type is not meant for that but that's easier than creating a specific message type)
void publishSpeed(double time) {
  speed_msg.header.stamp = nh.now();      //timestamp for odometry data
  speed_msg.vector.x = speed_act_left;    //left wheel speed (in m/s)
  speed_msg.vector.y = speed_act_right;   //right wheel speed (in m/s)
  speed_msg.vector.z = time/1000;         //looptime, should be the same as specified in LOOPTIME (in s)
  speed_pub.publish(&speed_msg);
  nh.spinOnce();
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
