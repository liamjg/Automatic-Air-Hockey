
#include "AccelStepper.h"
AccelStepper stepperX(1, 3, 6);

#define home_switch 2

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

char messageFromPC[buffSize] = {0};

int newPosition = 0;

unsigned long curMillis;

unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;

void setup() {
  Serial.begin(9600);
  // initialize the stepper
  setupStepper();
  
  // tell the PC we are ready
  Serial.println("<Arduino is ready>");
}

void setupStepper(){
  long initial_homing = -1;

  pinMode(home_switch, INPUT_PULLUP);

  delay(5);  // Wait for EasyDriver wake up

  //  Set Max Speed and Acceleration of each Steppers at startup for homing
  stepperX.setMaxSpeed(1000.0);      // Set Max Speed of Stepper (Slower to get better accuracy)
  stepperX.setAcceleration(1000.0);  // Set Acceleration of Stepper

  while (digitalRead(home_switch)) {  // Make the Stepper move CCW until the switch is activated
    stepperX.moveTo(initial_homing);  // Set the position to move to
    initial_homing++;  // Decrease by 1 for next move if needed
    stepperX.run();  // Start moving the stepper
    delay(2);
  }
  stepperX.setCurrentPosition(1650);
  
  stepperX.runToNewPosition(1610);
  stepperX.setCurrentPosition(1650);
  
  stepperX.setMaxSpeed(16000.0);      // Set Max Speed of Stepper (Faster for regular movements)
  stepperX.setAcceleration(16000.0);  // Set Acceleration of Stepper
}


void loop() {
  curMillis = millis();
  getDataFromPC();
  updateStepperPosition();
  replyToPC();
}

void getDataFromPC() {
    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

 
void parseData() {
  newPosition = atoi(inputBuffer);     // convert this part to an integer
}

void replyToPC() {
  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<Msg ");
    Serial.print(messageFromPC);
    Serial.print(" StprPos ");
    Serial.print(newPosition);
    Serial.print(" Time ");
    Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");
  }
}

void updateStepperPosition(){
  stepperX.runToNewPosition(newPosition);
}
