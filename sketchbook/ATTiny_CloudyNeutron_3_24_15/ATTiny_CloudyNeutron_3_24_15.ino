/*
Adafruit Arduino - Lesson 3. RGB LED
 */



//uncomment this line if using a Common Anode LED
//#define COMMON_ANODE

bool RUNNING_UNO = 0; // debug mode for running uno


int drawingIROut = 9; // IR
int yellowOnLED = 3; // yellowLED
int proxInSensor = A4;// button
int proxOutLED = 5; // proxOut
int colorWheelPOT = A2; // sensor

int RBGLED_bluePin = 8;
int RBGLED_redPin = 6; 
int RBGLED_greenPin = 7;

int button_1 = 10;
int button_2 = 0;
int button_3 = 1;


/*
int drawingIROut = 10; // IR
int yellowOnLED = 9; // yellowLED
int proxInSensor = A3;// button
int proxOutLED = 1; // proxOut
int colorWheelPOT = A2 // sensor
int RBGLED_redPin = 7; 
int RBGLED_greenPin = 8;
int RBGLED_bluePin = 5;
*/


float prox_input_analog_threshold = 890.0;  //if too low, stays on
                      //max 1024//      //if too high, stays off 







unsigned long micro_convert = 1000.0;

unsigned long prox_millis = 40.0 * micro_convert;
unsigned long prox_off_time = 400.0 * micro_convert;
unsigned long prox_speed_up = 250.0 * micro_convert;

float prox_input_analog = 0.0;
float last_prox_input_analog = 0.0;
float running_avg_prox_input_analog = 320.0;
float running_diff_prox_input_analog = 0.0;

bool speed_up_bool = false;

int prox_duty_cycle = 1 ; //out of 255

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

int color_dead_zone = 10; //creates dead zone in pot double this number
int color_multiple = 128; //true for vcc=5VDC
int colorstate = 0;       // state of the current output color

int colorWheelPOT_analog =0;


int setRBG(int, int);
void proxBlink(int,unsigned long);
void proxPWMBlink(int,unsigned long);

void dataBlink(int,int);
void fast_mode_check(bool);
void IR_output_toggle(bool);

bool poll_prox_input();

void set_prox_threshold();
void yellow_indicator_toggle();




void setup()
{

 
  //if(RUNNING_UNO){Serial.begin(9600);}

  pinMode(drawingIROut,OUTPUT);
  pinMode(proxOutLED,OUTPUT);
  pinMode(proxInSensor,INPUT);
  pinMode(yellowOnLED,OUTPUT);
  pinMode(colorWheelPOT, INPUT);  
  pinMode(RBGLED_redPin, OUTPUT);
  pinMode(RBGLED_greenPin, OUTPUT);
  pinMode(RBGLED_bluePin, OUTPUT);


  //set everything to zero/low
  digitalWrite(yellowOnLED, LOW);
  digitalWrite(drawingIROut, LOW); // IR
  
  analogWrite(proxOutLED,LOW);

  analogWrite(RBGLED_redPin, 0);
  analogWrite(RBGLED_greenPin, 0);
  analogWrite(RBGLED_bluePin, 0); 
  
  //pullup button setup
  pinMode(button_1, INPUT);
  digitalWrite(button_1, HIGH);
  pinMode(button_1, INPUT_PULLUP);

}




void setColor(int red, int green, int blue)
{
#ifdef COMMON_ANODE
  red = 255 - red;
  green = 255 - green;
  blue = 255 - blue;
#endif
  analogWrite(RBGLED_redPin, red);
  analogWrite(RBGLED_greenPin, green);
  analogWrite(RBGLED_bluePin, blue);  
}




int setRBG(int colorWheelPOT_analog,int colorstate){

  
  if (colorstate !=1 && colorWheelPOT_analog < color_multiple-color_dead_zone){
    setColor(0, 255, 0);  // red
    colorstate = 1;
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=2 && colorWheelPOT_analog >= color_multiple + color_dead_zone && colorWheelPOT_analog < color_multiple*2 - color_dead_zone){
    setColor(100,50,255); //red
    colorstate = 2;
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=3 && colorWheelPOT_analog >= color_multiple*2 + color_dead_zone && colorWheelPOT_analog < color_multiple*3 - color_dead_zone){
    setColor(120, 10, 255);  // yellow  
    colorstate = 3;
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=4 && colorWheelPOT_analog >= color_multiple*3 + color_dead_zone && colorWheelPOT_analog < color_multiple*4 - color_dead_zone){
    setColor(255, 0, 255);  // green
    colorstate = 4;
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=5 && colorWheelPOT_analog >= color_multiple*4 + color_dead_zone && colorWheelPOT_analog < color_multiple*5 - color_dead_zone){
    setColor(255, 255, 0);  // blue
    colorstate = 5;
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=6 && colorWheelPOT_analog >= color_multiple*5 + color_dead_zone && colorWheelPOT_analog < color_multiple*6 - color_dead_zone){
    setColor(200, 255, 0);  // purple
    colorstate = 6;
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=7 && colorWheelPOT_analog >= color_multiple*6 + color_dead_zone && colorWheelPOT_analog < color_multiple*7 - color_dead_zone){
    setColor(180, 50, 100);  // white
    colorstate = 7;
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=8 && colorWheelPOT_analog >= color_multiple*7 + color_dead_zone ){
    setColor(255, 255, 255);  // black
    colorstate = 8;
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }  
  return colorstate;
}












void proxPWMBlink(int prox_input_state, unsigned long timer){
  analogWrite(proxOutLED, prox_duty_cycle);
  
  /*
  if(RUNNING_UNO){
    Serial.print(prox_input_analog_threshold);
    Serial.print("\t|PWM|\t");
    Serial.print(running_avg_prox_input_analog);
    Serial.print("\t|\t");
    Serial.print(running_diff_prox_input_analog);
    Serial.print("\t|\t");
    Serial.println(prox_input_analog);
  }
  */

}









/*
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
*/


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
  
  prox_input_analog = analogRead(proxInSensor); //goes high when lit
  
  float temp_diff = prox_input_analog-last_prox_input_analog;
  running_diff_prox_input_analog = (19*running_diff_prox_input_analog + abs(prox_input_analog-last_prox_input_analog))/20;
    
  //checks the difference between this blink and last blink
  if(prox_input_analog-last_prox_input_analog > prox_input_analog_threshold){ //sees light
    decision = true; // we have artificially bright conditions when this occurs
  }else{ //sees dark
    decision = false;
  }

  last_prox_input_analog = prox_input_analog;

  

  //if(RUNNING_UNO){Serial.print(prox_input_analog);Serial.print("\t|prox|\t");Serial.println(decision);}
  return decision;
}





void IR_output_toggle(bool prox_input_state){
  
  if(prox_input_state){
    IR_draw_state = 1;
    IR_draw_timer = timer;
  }
  
  if(IR_draw_state && ((timer-IR_draw_timer) > yellow_delay_time*2) ){
    IR_draw_state = 0;
  }
  
  if(IR_draw_state != last_IR_draw_state){
    last_IR_draw_state = IR_draw_state;
    
    if(IR_draw_state){
      digitalWrite(drawingIROut, HIGH);
      prox_input_flag = 1; //for yellow
    }else{
      digitalWrite(drawingIROut, LOW);
      prox_input_flag = 0; //for yellow
    }
    
  }//end IR state if
}//end void




void set_prox_threshold(){
  
  // if the set-threshold button goes low, it is pressed
  if(digitalRead(button_1)){
    
  }else{
    
    // make sure the proxOUT is on, then set calibrate

    prox_input_analog_threshold = running_diff_prox_input_analog;

    
  }
  //if(RUNNING_UNO){Serial.print(prox_input_analog_threshold);Serial.print("\t|cal|\t");Serial.println(digitalRead(button_1));}

}











void yellow_indicator_toggle(){
  
  //prox_input_state
  
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
  
}
























void loop()
{


 
  
  timer = micros();

  // finds if there's proximity to surface
  prox_input_state = poll_prox_input();
  
  IR_output_toggle(prox_input_state);

  // blinks prox_out_LED, turns on yellow_LED when in prox
  //proxBlink(prox_input_state, timer);
  proxPWMBlink(prox_input_state, timer);
  
  // blinks IR for events
  if(blink_number){
    //dataBlink(prox_input_state, blink_number);
  }
  
  // get colorwheel and do color changing
  colorWheelPOT_analog = analogRead(colorWheelPOT);
  colorstate = setRBG(colorWheelPOT_analog,colorstate);
  
  //set the threshold maunally with cal button
  set_prox_threshold();
  
  //yellow indicator LED
  yellow_indicator_toggle();

}





