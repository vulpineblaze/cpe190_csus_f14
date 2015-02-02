/*
Adafruit Arduino - Lesson 3. RGB LED
 */
#define PROX_MILLIS 1
#define PROX_OFF_TIME 160
#define SPEED_UP 100

#define DATA_MILLIS 100
#define BURST_RATE 100

int redPin = 7;
int greenPin = 8;
int bluePin = 5;
int sensor = A2;
int IR = 10;
int button = 1;
int proxOut = 3;


int sensorvalue = 0;

int buttonstate = 0;
int last_buttonstate = 0;
bool flag_buttonstate;
int delay_buttonstate;

int colorstate = 0;
int last_colorstate = 0;
bool flag_colorstate;
int delay_colorstate;

int data_count= 0;

unsigned long timer = 0.0;
unsigned long prox_timer = 0.0;
unsigned long start_time = 0.0;

//unsigned long prox_millis = 5.0;
//unsigned long prox_off_time = 200.0;
//unsigned long prox_speed_up = 150.0;

unsigned long micro_convert = 1000.0;
unsigned long prox_millis = 10.0 * micro_convert;
unsigned long prox_off_time = 400.0 * micro_convert;
unsigned long prox_speed_up = 250.0 * micro_convert;

unsigned long burst_rate = 50.0 * micro_convert;
unsigned long data_millis = 50.0 * micro_convert;



bool on_off_state = true;
int prox_cnt;

int current_IR_status=0;
int current_prox_status=0;


//void setColor(int, int);
int setRBG(int, int);
void proxBlink(int,unsigned long);

void dataBlink(int,int);









//uncomment this line if using a Common Anode LED
//#define COMMON_ANODE

void setup()
{
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(sensor, INPUT);  
  pinMode(IR,OUTPUT);
  pinMode(proxOut,OUTPUT);
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


int setRBG(int sensorvalue,int colorstate){

  if (sensorvalue >= 0 && sensorvalue < 128){
    setColor(0, 255, 0);  // red
    colorstate = 1;
  }
  else if (sensorvalue >= 129 && sensorvalue < 256){
    setColor(100,50,255); //red
    colorstate = 2;
  }
  else if (sensorvalue >= 257 && sensorvalue < 384){
    setColor(120, 10, 255);  // yellow  
    colorstate = 3;
  }
  else if (sensorvalue >= 385 && sensorvalue < 512){
    setColor(255, 0, 255);  // green
    colorstate = 4;
  }
  else if (sensorvalue >= 513 && sensorvalue < 640){
    setColor(255, 255, 0);  // blue
    colorstate = 5;
  }
  else if (sensorvalue >= 641 && sensorvalue < 768){
    setColor(200, 255, 0);  // purple
    colorstate = 6;
  }
  else if (sensorvalue >= 769 && sensorvalue < 896){
    setColor(180, 50, 100);  // white
    colorstate = 7;
  }
  else if (sensorvalue >= 897 && sensorvalue < 1024){
    setColor(255, 255, 255);  // black
    colorstate = 8;
  }  
  return colorstate;
}


void proxBlink(int buttonstate, unsigned long timer){

  //if(timer % (PROX_MILLIS+(PROX_MILLIS*4*(!buttonstate))) == 0 && prox_cnt == 0){
    //PROX_DUTY_CYCLE
  unsigned long lhs = (timer % (prox_millis+prox_off_time-(prox_speed_up*buttonstate))) ;
  unsigned long rhs = prox_millis ;
        
  
  
//  if(lhs > 1000){
//    digitalWrite(IR, HIGH);
//  }else{
//    digitalWrite(IR, LOW);
//  }
  
  if(lhs < rhs && current_prox_status==0){
    digitalWrite(proxOut, HIGH);
    current_prox_status = 1;
  }else if(lhs >= rhs && current_prox_status==1){
    digitalWrite(proxOut, LOW);
    current_prox_status = 0;
  }else{
    digitalWrite(proxOut, LOW);
    current_prox_status = 0;
    //prox_timer = timer;
  }


}

void dataBlink(int colorstate, int buttonstate){
  if(colorstate != last_colorstate){
    flag_colorstate = true;
    last_colorstate = colorstate;
  }
  if(buttonstate != last_buttonstate){
    if(buttonstate){flag_buttonstate = true;}
    last_buttonstate = buttonstate;
  }else{
    //last_buttonstate = 0; 
  }

  if(flag_buttonstate){
    //data_count++;
    if(start_time == 0){
      start_time = timer;
    }

    if(timer % burst_rate < burst_rate / 2 && current_IR_status == 0){
      digitalWrite(IR, HIGH);
      current_IR_status = 1;
    }
    else if(timer % burst_rate < burst_rate && current_IR_status == 1){
      digitalWrite(IR, LOW);
      current_IR_status = 0;
    }
    else{
      //data_count = 0;
    }

    if(timer -start_time > data_millis*9){
      flag_buttonstate = 0;
      data_count = 0;
      start_time = 0;
      digitalWrite(IR, LOW);
      current_IR_status = 0;
    }
  }else if(flag_colorstate){
    if(start_time == 0){
      start_time = timer;
    }

    if(timer % burst_rate < burst_rate / 2 && current_IR_status == 0){
      digitalWrite(IR, HIGH);
      current_IR_status = 1;
    }
    else if(timer % burst_rate < burst_rate 
          && timer % burst_rate > burst_rate / 2 
          && current_IR_status == 1){
      digitalWrite(IR, LOW);
      current_IR_status = 0;
    }
    else{
      //data_count = 0;
    }

    if(timer - start_time > data_millis*colorstate){
      flag_colorstate = 0;
      //data_count = 0;
      start_time = 0;
      digitalWrite(IR, LOW);
      current_IR_status = 0;
    }
  }
}



void loop()
{


  //timer = millis();
  timer = micros();
  sensorvalue = analogRead(sensor);
  buttonstate = digitalRead(button);


  colorstate = setRBG(sensorvalue,colorstate);
  proxBlink(buttonstate, timer);
  dataBlink(colorstate,buttonstate);


}




