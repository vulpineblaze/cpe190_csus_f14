/*
  Blink (modified slightly for ATTiny84/44 ICs
  Turns on an LED on for one second, then off for one second, repeatedly.

  This example code is in the public domain.
 */

// ATTIny84 / 44 does not have Pin 13, so we use pin 7 instead.
// A current limiting resistor should be connected in line with the LED.


int led = 7;
int button = 8;

int button_state;

int rate = 1000; //one second
int burst = 5;
int burst_ratio = 100;
int down_time = burst * burst_ratio;

void blink_LED(int, int);




// the setup routine runs once when you press reset:
void setup() {
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);
  pinMode(button, INPUT);
  
  //Serial.begin(9600);
  
}

// blinks at the rate
void blink_LED(int on_time, int off_time){
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(on_time);               // wait for a second
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  delay(off_time); 
}

// the loop routine runs over and over again forever:
void loop() {
  //Serial.println(button);
  button_state = digitalRead(button);
  
  if(button_state == HIGH){
    blink_LED(burst,down_time);
  }else{
    blink_LED(burst,down_time*4);
  }
                // wait for a second
}


