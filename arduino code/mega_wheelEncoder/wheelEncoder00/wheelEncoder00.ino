// **TEST TO READ WHEEL ENCODERS ** 

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

  Serial.begin(115200);
}

void loop() {
  currentMillis = millis();

  if (currentMillis - previousMillis >= 10){
    previousMillis = currentMillis;

    Serial.print(encoder0Pos);
    Serial.print(" , ");
    Serial.println(encoder1Pos);
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
