



int PinA = 2;
int PinB = 4;


int pinA_input_analog = 0;
int pinB_input_analog = 0;

int phase_AB = 0;
int last_phase_AB = 0;

// 1 = CW // -1 = CCW
int read_out = 0;


float timer = 0;
float rotary_timer = 0;
float rotary_delay = 2*1000;


// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(PinA, INPUT);     
  pinMode(PinB, INPUT);     
  
  Serial.begin(9600);
  
}

// the loop routine runs over and over again forever:
void loop() {
  
  timer = micros();
  
  if(timer - rotary_timer > rotary_delay ){
      
    pinA_input_analog = digitalRead(PinA);
    pinB_input_analog = digitalRead(PinB);
    
    if(pinA_input_analog == 0 && pinB_input_analog == 0){
      phase_AB = 0;    
    }else if(pinA_input_analog == 0 && pinB_input_analog == 1){
      phase_AB = 1;
    }else if(pinA_input_analog == 1 && pinB_input_analog == 1){
      phase_AB = 3;
    }else if(pinA_input_analog == 1 && pinB_input_analog == 0){
      phase_AB = 2;
    }
  
  
    if(phase_AB != last_phase_AB){
      
      switch (phase_AB) {
       case 0:
         if(last_phase_AB==1){read_out=1;}
         else if(last_phase_AB==2){read_out=-1;}
         break;
       case 1:
         if(last_phase_AB==3){read_out=1;}
         //else if(last_phase_AB==0){read_out=-1;}
         break;
       case 2:
         //if(last_phase_AB==0){read_out=1;}
         if(last_phase_AB==3){read_out=-1;}
         break;
       case 3:
         if(last_phase_AB==2){read_out=1;}
         else if(last_phase_AB==1){read_out=-1;}
         break;
       default:
         // default stuff here
         break;
      }
      
      Serial.print(phase_AB);
      Serial.print("|");
      Serial.print(last_phase_AB);
      Serial.print("|");
      
      last_phase_AB = phase_AB;
      
      
      if(read_out==1){
        Serial.println("CW");
      }else if(read_out==-1){
        Serial.println("CCW");
      }else{
        Serial.println(read_out);
      }
      read_out = 0;
      
      
    }// if not equals
    Serial.print(phase_AB);
    rotary_timer = timer;
  }//if timer > rotary delay
  
  //delay(0.001);
  //Serial.print(phase_AB);
  
//  Serial.print(pinA_input_analog);
//  Serial.print("|");
//  Serial.println(pinB_input_analog);
  
}
