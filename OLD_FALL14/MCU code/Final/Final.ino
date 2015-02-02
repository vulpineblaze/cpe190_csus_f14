/*
Adafruit Arduino - Lesson 3. RGB LED
*/

int redPin = 11;
int greenPin = 10;
int bluePin = 9;
int sensor = A0;
int sensor2 = A1;
int sensorvalue = 0;
int sensor2value = 0;
int red;
int IR = 7;
int button = 4;
int buttonstate = 0;



//uncomment this line if using a Common Anode LED
//#define COMMON_ANODE

void setup()
{
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  Serial.begin(9600);
  pinMode(sensor, INPUT);  
  pinMode(sensor2,INPUT);
  pinMode(IR,OUTPUT);
  pinMode(button,INPUT);
  
}

void loop()
{
  sensorvalue = analogRead(sensor);
  sensor2value = analogRead(sensor2);
  Serial.println(sensor2value);
 buttonstate = digitalRead(button);

 if (sensor2value < 300)
 
 {
     digitalWrite(IR, HIGH);
   }
      else 
    // turn LED off:
    digitalWrite(IR, LOW);
  
  if (buttonstate == HIGH){
    digitalWrite(IR,HIGH);
    delay (250);
    digitalWrite(IR,LOW);
    delay (250);
    digitalWrite(IR,HIGH);
    delay (250);
    digitalWrite(IR,LOW);
    delay (250);
  }
  
  if (sensorvalue > 0 && sensorvalue < 128){
      setColor(0, 255, 0);  // red
   
      }
  
  if (sensorvalue > 129 && sensorvalue < 256){
      setColor(100, 50, 150);  // orange 
        
      }
  
  if (sensorvalue > 257 && sensorvalue < 384){
      setColor(120, 10, 255);  // yellow  
         
      }
  
  if (sensorvalue > 385 && sensorvalue < 512){
      setColor(255, 0, 255);  // green
       
      }
  
  if (sensorvalue > 513 && sensorvalue < 640){
      setColor(255, 255, 0);  // blue
          
      }
  
  if (sensorvalue > 641 && sensorvalue < 768){
      setColor(200, 255, 0);  // purple
             
      }
      
  if (sensorvalue > 769 && sensorvalue < 896){
      setColor(180, 50, 100);  // white
             
      }
      
  if (sensorvalue > 897 && sensorvalue < 1024){
      setColor(255, 255, 255);  // black
             
      }  
}

void setColor(int red, int green, int blue)
{
  #ifdef COMMON_ANODE
    red = 255 - red;
    green = 255 - green;
    blue = 255 - blue;
  #endif
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
}
