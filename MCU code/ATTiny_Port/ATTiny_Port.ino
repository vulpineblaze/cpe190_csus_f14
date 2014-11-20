/*
Adafruit Arduino - Lesson 3. RGB LED
 */

int redPin = 7;
int greenPin = 8;
int bluePin = 5;
int sensor = A2;
int IR = 10;
int button = 1;


int sensorvalue = 0;
int buttonstate = 0;

int sensor2value = 0; //depr
int red;   // not used
int sensor2 = A1;  //decprecated

int timer = 0;

int test = 0;


void setColor(int, int, int);
void setRBG(int);
void proxBlink(int);

void colorTest();
void offRBG();

void colorFade();


//uncomment this line if using a Common Anode LED
//#define COMMON_ANODE

void setup()
{
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(sensor, INPUT);  
  pinMode(IR,OUTPUT);
  pinMode(button,INPUT);

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


void setRBG(int){
  
 if (sensorvalue >= 0 && sensorvalue < 128){
    setColor(0, 255, 0);  // red

    //purple test
    //setColor(200, 255, 0);  // purple
    //setColor(200, 255, 0); //green
    //setColor(200, 0, 255); //blue
    //setColor(255, 200, 0); //green
    //setColor(255, 0, 200); //blue
    //setColor(0, 255, 200); //red
    //setColor(0, 200, 255); //red
  }
  else if (sensorvalue >= 129 && sensorvalue < 256){
    //setColor(100, 50, 150);  // orange 
    setColor(100,50,255); //red
    //setColor(50,100,150); //wrong//redish
    //setColor(150,100,50); // aqua
    // setColor(50,150,100);// red still
    // setColor(100,150,50); //red still
    // setColor(150,50,100);// aqua
  }
  else if (sensorvalue >= 257 && sensorvalue < 384){
    setColor(120, 10, 255);  // yellow  
    //setColor(120, 10, 255);//blue
    //setColor(120, 255, 10);//red
    //setColor(10, 120, 255); //redish
    //setColor(10, 255, 120);//redish
    //setColor(255, 10, 120); //aqua
    //setColor(255, 120, 10); //aqua
  }
  else if (sensorvalue >= 385 && sensorvalue < 512){
    setColor(255, 0, 255);  // green
  }
  else if (sensorvalue >= 513 && sensorvalue < 640){
    setColor(255, 255, 0);  // blue
  }
  else if (sensorvalue >= 641 && sensorvalue < 768){
    setColor(200, 255, 0);  // purple
  }
  else if (sensorvalue >= 769 && sensorvalue < 896){
    setColor(180, 50, 100);  // white
  }
  else if (sensorvalue >= 897 && sensorvalue < 1024){
    setColor(255, 255, 255);  // black
  }  
}


void proxBlink(int){}

void offRBG(){
  analogWrite(redPin, 255); //Turns off the RED Element
  analogWrite(greenPin, 255); //Turns off the GREEN Element
  analogWrite(bluePin, 255); //Turns off the BLUE Element
}

void colorTest(){
  float waiter = 1;
  float duty_cycle = 4;
  digitalWrite(IR, HIGH);
  for (int i = 0; i < 255; i+=5) { 
    for(int j=0;j<255;j +=5){
      for(int k=0;k<255;k += 5){
        offRBG();
        delay(waiter*duty_cycle);
        setColor(i,j,k);
        delay(waiter);
      }
    } 
  }
  digitalWrite(IR, LOW);
  delay(500);
}


void colorFade(){
  // Red Element fade

  digitalWrite(IR, LOW);
  int waiter = 10;
  delay(210);
  digitalWrite(IR, HIGH);
  
  for(int fadeValue = 255 ; fadeValue >= 100; fadeValue -=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(redPin, fadeValue);         
    delay(waiter);                            
  } 
  for(int fadeValue = 100 ; fadeValue <= 255; fadeValue +=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(redPin, fadeValue);         
    delay(waiter);                            
  }
  
// Green Element Fade  
  
  for(int fadeValue = 255 ; fadeValue >= 100; fadeValue -=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(greenPin, fadeValue);         
    delay(waiter);                            
  } 
  for(int fadeValue = 100 ; fadeValue <= 255; fadeValue +=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(greenPin, fadeValue);         
    delay(waiter);                            
  }
  
// Blue Element Fade

  for(int fadeValue = 255 ; fadeValue >= 100; fadeValue -=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(bluePin, fadeValue);         
    delay(waiter);                            
  } 
  for(int fadeValue = 100 ; fadeValue <= 255; fadeValue +=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(bluePin, fadeValue);         
    delay(waiter);                            
  } 
  
// Red+Green Elements Fade

  for(int fadeValue = 255 ; fadeValue >= 100; fadeValue -=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(redPin, fadeValue);         
    analogWrite(greenPin, fadeValue);         
    delay(waiter);                            
  } 
  for(int fadeValue = 100 ; fadeValue <= 255; fadeValue +=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(redPin, fadeValue);         
    analogWrite(greenPin, fadeValue);         
    delay(waiter);                            
  } 

// Green+Blue Elements Fade

  for(int fadeValue = 255 ; fadeValue >= 100; fadeValue -=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(greenPin, fadeValue);         
    analogWrite(bluePin, fadeValue);         
    delay(waiter);                            
  } 
  for(int fadeValue = 100 ; fadeValue <= 255; fadeValue +=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(greenPin, fadeValue);         
    analogWrite(bluePin, fadeValue);         
    delay(waiter);                            
  } 

// Blue+Red Elements Fade

  for(int fadeValue = 255 ; fadeValue >= 100; fadeValue -=5) {   
    offRBG();  
    delay(waiter);     
    analogWrite(redPin, fadeValue);         
    analogWrite(bluePin, fadeValue);         
    delay(waiter);                            
  } 
  for(int fadeValue = 100 ; fadeValue <= 255; fadeValue +=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(redPin, fadeValue);         
    analogWrite(bluePin, fadeValue);         
    delay(waiter);                            
  } 


// All Elements Fade

  for(int fadeValue = 255 ; fadeValue >= 100; fadeValue -=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(redPin, fadeValue);         
    analogWrite(greenPin, fadeValue);         
    analogWrite(bluePin, fadeValue);         
    delay(waiter);                            
  } 
  for(int fadeValue =100 ; fadeValue <= 255; fadeValue +=5) { 
    offRBG();     
    delay(waiter);    
    analogWrite(redPin, fadeValue);         
    analogWrite(greenPin, fadeValue);         
    analogWrite(bluePin, fadeValue);         
    delay(waiter);                            
  } 
}

void loop()
{
  //analogWrite(redPin, 255); //Turns off the RED Element
  //analogWrite(greenPin, 255); //Turns off the GREEN Element
  //analogWrite(bluePin, 255); //Turns off the BLUE Element
  
  timer = millis();
  sensorvalue = analogRead(sensor);
  buttonstate = digitalRead(button);
  
  //test = (1024 - sensorvalue)/4;
  //setColor(255, 0, 255);
  //colorTest();
  //offRBG();
  //setColor(150, 80+(buttonstate*60), test);
  
  //colorFade();
  
  if(test > 128){
    digitalWrite(IR, HIGH);
  }else{
    digitalWrite(IR, LOW);
  }

 //test = 255 - (255*sensorvalue)/1024;
  //setColor(test, 0, 0); 
  setRBG(sensorvalue);
  proxBlink(buttonstate);
  
   
}



