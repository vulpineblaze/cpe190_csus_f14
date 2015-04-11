/*
Adafruit Arduino - Lesson 3. RGB LED
 */



//uncomment this line if using a Common Anode LED
//#define COMMON_ANODE

bool RUNNING_UNO = 1; // debug mode for running uno

int proxOutReader = 0;

int analogDebugOutput = 1;

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
float prox_input_analog_lit = 0.0;
float prox_input_analog_unlit = 0.0;
float last_prox_input_analog = 0.0;
float last_prox_input_analog_lit = 0.0;
float last_prox_input_analog_unlit = 0.0;
float running_avg_prox_input_analog = 320.0;
float running_diff_prox_input_analog = 0.0;

float on_off_diff_value = 0.0;

float last_timer = 0.0;
float start_test_timer = 0.0;
float end_test_timer = 0.0;
float edge_margin_timer = 0.0;
bool last_isProxOutOn = 0;

int toggle_tally = 0;

int edge_margin_micros = 130;
float measured_pwm_freq = 1000.0;

bool speed_up_bool = false;

int prox_duty_cycle = 65 ; //out of 255

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

float colorwheel_timer = 0.0;
int colorwheel_delay_millis = 200 * micro_convert;


int setRBG(int, int);
void proxBlink(int,unsigned long);
void proxPWMBlink(int,unsigned long);

void dataBlink(int,int);
void fast_mode_check(bool);
void IR_output_toggle(bool);

bool poll_prox_input();

void yellow_indicator_toggle();




void setup()
{

 
  //if(RUNNING_UNO){Serial.begin(115200);}

  pinMode(proxOutReader,INPUT);
  pinMode(drawingIROut,OUTPUT);
  pinMode(analogDebugOutput,OUTPUT);
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
  analogWrite(analogDebugOutput,LOW);
  

  analogWrite(RBGLED_redPin, 0);
  analogWrite(RBGLED_greenPin, 0);
  analogWrite(RBGLED_bluePin, 0); 
  
  //pullup button setup
  pinMode(button_1, INPUT);
  digitalWrite(button_1, HIGH);
  pinMode(button_1, INPUT_PULLUP);

}






void loop()
{

  
  timer = micros();

  // finds if there's proximity to surface
  prox_input_state = poll_prox_input_reader();
  
  IR_output_toggle(prox_input_state);

  // blinks prox_out_LED, turns on yellow_LED when in prox
  proxPWMBlink(prox_input_state, timer);
  
  
  // get colorwheel and do color changing
  if(timer - colorwheel_timer > colorwheel_delay_millis){
    colorwheel_timer = timer;
    //colorWheelPOT_analog = analogRead(colorWheelPOT);
  }
  //colorstate = setRBG(colorWheelPOT_analog,colorstate);
  
  //set the threshold maunally with cal button
  set_prox_threshold_reader();
  
  //yellow indicator LED
  yellow_indicator_toggle();
  
  
  //if(RUNNING_UNO){Serial.print(prox_input_analog_threshold);Serial.print("\t|prox|\t");Serial.print(running_diff_prox_input_analog);Serial.print("\t|\t");Serial.println(prox_input_analog);}


}





