/*
Adafruit Arduino - Lesson 3. RGB LED
 */
#define PROX_MILLIS 1
#define PROX_OFF_TIME 160
#define SPEED_UP 100

#define DATA_MILLIS 100
#define BURST_RATE 100


//int redPin = 7;
//int greenPin = 8;
//int bluePin = 5;
//int sensor = A2;
int IR = 10;
int button = A3;
int proxOut = 1;
int yellowLED = 9;
int redLED = 6;
int toggle_switch = 0;


int sensorvalue = 0;

float button_analog_threshold = 10000.0;
float button_analog_avg = 0.0;
int prox_in_cnt = 0;

int buttonstate = 0;
int last_buttonstate = 0;
bool flag_buttonstate=0;
int delay_buttonstate=0;

int colorstate = 0;
int last_colorstate = 0;
bool flag_colorstate=0;
int delay_colorstate=0;

bool switch_state=0;

int data_count= 0;

unsigned long timer = 0.0;
unsigned long prox_timer = 0.0;
unsigned long start_time = 0.0;




//unsigned long prox_millis = 5.0;
//unsigned long prox_off_time = 200.0;
//unsigned long prox_speed_up = 150.0;

unsigned long real_mode_speed_up = 0.0;
unsigned long real_mode_speed_factor = 10.0;

unsigned long micro_convert = 1000.0;


unsigned long yellow_time = 0.0; //in millis
unsigned long yellow_delay_time = 300.0 * micro_convert; //in millis

unsigned long prox_millis = 40.0 * micro_convert;
unsigned long prox_off_time = 400.0 * micro_convert;
unsigned long prox_speed_up = 250.0 * micro_convert;

unsigned long burst_rate = 50.0 * micro_convert;
unsigned long data_millis = 50.0 * micro_convert;

bool fast_mode_state = false;



bool on_off_state = true;

int prox_cnt=0;
int prox_threshold_high = 2; //when button seen > this, fast mode
int prox_threshold_low = 1; //when button seen < this, slow mode
bool speed_up_bool = false;


bool current_IR_status=0;
bool current_prox_status=0;
bool current_redLED_status=0;
bool current_yellowLED_status=0;

bool last_redLED_status=0;

//bool check_vcc_once = true;
long vcc_value = 0.0;


int color_dead_zone = 10; //creates dead zone in pot double this number
int color_multiple = 128; //true for vcc=5VDC

//void setColor(int, int);
int setRBG(int, int);
void proxBlink(int,unsigned long);

void dataBlink(int,int);
void fast_mode_check(bool);

bool poll_prox_button();







//uncomment this line if using a Common Anode LED
//#define COMMON_ANODE

void setup()
{
  //pinMode(redPin, OUTPUT);
  //pinMode(greenPin, OUTPUT);
  //pinMode(bluePin, OUTPUT);
  //pinMode(sensor, INPUT);  
  pinMode(IR,OUTPUT);
  pinMode(proxOut,OUTPUT);
  pinMode(button,INPUT);
  pinMode(yellowLED,OUTPUT);
  pinMode(redLED,OUTPUT);
  pinMode(toggle_switch,INPUT);
  
  //set everything to zero/low
  digitalWrite(redLED, LOW);
  digitalWrite(yellowLED, LOW);
  digitalWrite(IR, LOW);
  digitalWrite(proxOut,LOW);

  //analogWrite(redPin, 0);
  //analogWrite(greenPin, 0);
  //analogWrite(bluePin, 0); 
  
  ///analogReference(INTERNAL);
}


long readVcc() {
 long result;
 // Read 1.1V reference against AVcc
 ADMUX =  0b00100001;// adc source=1.1 ref; adc ref (base for the 1023 maximum)=Vcc
 delay(2); // Wait for Vref to settle
 ADCSRA |= 1<<ADSC; // Convert
 while (bit_is_set(ADCSRA,ADSC));
 result = ADCL;
 result |= ADCH<<8;
 result = 1126400L / result; // Back-calculate AVcc in mV
 return result;
}



void proxBlink(int buttonstate, unsigned long timer){

  //if(timer % (PROX_MILLIS+(PROX_MILLIS*4*(!buttonstate))) == 0 && prox_cnt == 0){
  //PROX_DUTY_CYCLE

  unsigned long lhs = (timer % (prox_millis+prox_off_time-(prox_speed_up*speed_up_bool))) ;
  unsigned long rhs = prox_millis ;




  if((prox_cnt > prox_threshold_high) ){
    speed_up_bool = true;
  }
  else if((prox_cnt < prox_threshold_low) ){
    speed_up_bool = false;
  }

  if(speed_up_bool && current_redLED_status==0){
    digitalWrite(redLED, HIGH);
    current_redLED_status = 1;
  }else if(!speed_up_bool && current_redLED_status==1){
    digitalWrite(redLED, LOW);
    current_redLED_status = 0;
  }
  if(current_redLED_status != last_redLED_status){
    last_redLED_status = current_redLED_status;
    if(current_redLED_status){
      if(yellow_time == 0){
        yellow_time = timer;
      }
  
      if(!current_yellowLED_status && ((timer-yellow_time)<yellow_delay_time)){
        digitalWrite(yellowLED, HIGH);
        current_yellowLED_status = 1;
        flag_buttonstate = 1;
      }
    }
  }
  if(current_yellowLED_status && ((timer-yellow_time)>=yellow_delay_time)){
    digitalWrite(yellowLED, LOW);
    current_yellowLED_status = 0;
    yellow_time = 0;
  }
  

  if(lhs < rhs ){
    if(buttonstate){
      if(prox_cnt <= prox_threshold_high){
        prox_cnt++;
      }
    }
    else if(!buttonstate ){
      if(prox_cnt >= prox_threshold_low){
        prox_cnt--;
      }
    }
    digitalWrite(proxOut, HIGH);
    current_prox_status = 1;
  }
  
  
  else if(lhs >= rhs){
    digitalWrite(proxOut, LOW);
    current_prox_status = 0;
  }
  else{
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
//  if(buttonstate != last_buttonstate){
//    if(buttonstate){
//      flag_buttonstate = true;
//    }
//    last_buttonstate = buttonstate;
//  }
  else{
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
  }
  else if(flag_colorstate){
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




bool poll_prox_button(){
  bool decision = buttonstate;


  // for cool pen
  float button_analog = analogRead(button); //goes high when lit
    
  button_analog_threshold = 890.0; //move to top after debug
                                  //if too low, stays on
                                  //if too high, stays off
  
  if(button_analog > button_analog_threshold){ //sees light
    decision = true;
    //prox_in_cnt++;
  }else if(button_analog < button_analog_threshold){ //sees dark
    decision = false;
    //prox_in_cnt--;
  }



  
  return decision;
}













void loop()
{


  //timer = millis();
  if (vcc_value == 0){
    vcc_value = readVcc();
    //color_multiple = color_multiple * (vcc_value / 5.0);
  }
  
  timer = micros();

  buttonstate = poll_prox_button();
  

  proxBlink(buttonstate, timer);
  dataBlink(0,buttonstate);


}





