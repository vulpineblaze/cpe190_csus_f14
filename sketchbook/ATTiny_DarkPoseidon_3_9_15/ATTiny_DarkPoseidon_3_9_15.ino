/*
Adafruit Arduino - Lesson 3. RGB LED
 */


int drawingIROut = 10; // IR
int yellowOnLED = 9; // yellowLED
int proxInSensor = A3;// button
int proxOutLED = 1; // proxOut




float prox_input_analog_threshold = 890.0;  //if too low, stays on
                      //max 1024//      //if too high, stays off 







unsigned long micro_convert = 1000.0;

unsigned long prox_millis = 40.0 * micro_convert;
unsigned long prox_off_time = 400.0 * micro_convert;
unsigned long prox_speed_up = 250.0 * micro_convert;


bool speed_up_bool = false;

int prox_cnt=0;
int prox_threshold_high = 2; //when button seen > this, fast mode
int prox_threshold_low = 1; //when button seen < this, slow mode

bool prox_input_flag = 0;
bool last_prox_input_flag = 0;
bool prox_input_state=0;



unsigned long yellow_time = 0.0; //in millis
unsigned long yellow_delay_time = 300.0 * micro_convert; //in millis

bool current_yellowLED_status=0;
bool current_IR_status=0;
bool flag_prox_input_state=0;
bool current_prox_status=0;

unsigned long timer = 0.0;
unsigned long start_time = 0.0;


unsigned long burst_rate = 50.0 * micro_convert;
unsigned long data_millis = 50.0 * micro_convert;

int data_count= 0;
int blink_number = 0;

long vcc_value = 0.0;


bool IR_draw_state =0;
bool last_IR_draw_state =0;
unsigned long IR_draw_timer =0.0;







int setRBG(int, int);
void proxBlink(int,unsigned long);

void dataBlink(int,int);
void fast_mode_check(bool);
void IR_output_toggle(bool);

bool poll_prox_input();






void setup()
{


  pinMode(drawingIROut,OUTPUT);
  pinMode(proxOutLED,OUTPUT);
  pinMode(proxInSensor,INPUT);
  pinMode(yellowOnLED,OUTPUT);


  //set everything to zero/low
  digitalWrite(yellowOnLED, LOW);
  digitalWrite(drawingIROut, LOW); // IR
  digitalWrite(proxOutLED,LOW);


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



void proxBlink(int prox_input_state, unsigned long timer){


  unsigned long lhs = (timer % (prox_millis+prox_off_time-(prox_speed_up*speed_up_bool))) ;
  unsigned long rhs = prox_millis ;




  if((prox_cnt > prox_threshold_high) ){
    speed_up_bool = true;
  }
  else if((prox_cnt < prox_threshold_low) ){
    speed_up_bool = false;
  }

  if(speed_up_bool && prox_input_flag==0){
    //digitalWrite(redLED, HIGH);
    prox_input_flag = 1;
  }else if(!speed_up_bool && prox_input_flag==1){
    //digitalWrite(redLED, LOW);
    prox_input_flag = 0;
  }
  if(prox_input_flag != last_prox_input_flag){
    last_prox_input_flag = prox_input_flag;
    if(prox_input_flag){
      if(yellow_time == 0){
        yellow_time = timer;
      }
  
      if(!current_yellowLED_status && ((timer-yellow_time)<yellow_delay_time)){
        digitalWrite(yellowOnLED, HIGH);
        current_yellowLED_status = 1;
        flag_prox_input_state = 1;
      }
    }
  }
  if(current_yellowLED_status && ((timer-yellow_time)>=yellow_delay_time)){
    digitalWrite(yellowOnLED, LOW);
    current_yellowLED_status = 0;
    yellow_time = 0;
  }
  

  if(lhs < rhs ){
    if(prox_input_state){
      if(prox_cnt <= prox_threshold_high){
        prox_cnt++;
      }
    }
    else if(!prox_input_state ){
      if(prox_cnt >= prox_threshold_low){
        prox_cnt--;
      }
    }
    digitalWrite(proxOutLED, HIGH);
    current_prox_status = 1;
  }
  
  
  else if(lhs >= rhs){
    digitalWrite(proxOutLED, LOW);
    current_prox_status = 0;
  }
  else{
    digitalWrite(proxOutLED, LOW);
    current_prox_status = 0;
    //prox_timer = timer;
  }


}



void dataBlink(int prox_input_state, int blink_number){


  if(flag_prox_input_state){
    if(start_time == 0){
      start_time = timer;
    }


    if(timer % burst_rate < burst_rate / 2 && current_IR_status == 0){
      digitalWrite(drawingIROut, HIGH);
      current_IR_status = 1;
    }
    else if(timer % burst_rate < burst_rate && current_IR_status == 1){
      digitalWrite(drawingIROut, LOW);
      current_IR_status = 0;
    }
    else{
      //data_count = 0;
    }

    if(timer -start_time > data_millis*blink_number){
      flag_prox_input_state = 0;
      data_count = 0;
      start_time = 0;
      digitalWrite(drawingIROut, LOW);
      current_IR_status = 0;
      blink_number = 0;
    }
  }
  
}




bool poll_prox_input(){
  bool decision = prox_input_state;
  
  float prox_input_analog = analogRead(proxInSensor); //goes high when lit
    

  if(prox_input_analog > prox_input_analog_threshold){ //sees light
    decision = true;
  }else if(prox_input_analog < prox_input_analog_threshold){ //sees dark
    decision = false;
  }

  return decision;
}





void IR_output_toggle(bool prox_input_state){
  
  if(prox_input_state){
    IR_draw_state = 1;
    IR_draw_timer = timer;
  }
  
  if(IR_draw_state && ((timer-IR_draw_timer) > yellow_delay_time) ){
    IR_draw_state = 0;
  }
  
  if(IR_draw_state != last_IR_draw_state){
    last_IR_draw_state = IR_draw_state;
    
    if(IR_draw_state){
      digitalWrite(drawingIROut, HIGH);
    }else{
      digitalWrite(drawingIROut, LOW);
    }
    
  }//end IR state if
}//end void









void loop()
{


  if (vcc_value == 0){
    vcc_value = readVcc();
  }
  
  timer = micros();

  // finds if there's proximity to surface
  prox_input_state = poll_prox_input();
  
  IR_output_toggle(prox_input_state);

  // blinks prox_out_LED, turns on yellow_LED when in prox
  proxBlink(prox_input_state, timer);
  
  // blinks IR for events
  if(blink_number){
    dataBlink(prox_input_state, blink_number);
  }


}





