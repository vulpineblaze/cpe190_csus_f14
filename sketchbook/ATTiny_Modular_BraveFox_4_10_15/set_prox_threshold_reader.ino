float calibrate_timer = 0;
float calibrate_delay = 200 * micro_convert;



void set_prox_threshold_reader(){
  
  // if the set-threshold button goes low, it is pressed
  if(timer-calibrate_timer > calibrate_delay){
    if(digitalRead(button_1)){
      
    }else{
      // make sure the proxOUT is on, then set calibrate
      if(on_off_diff_value > 0){
        prox_input_analog_threshold = on_off_diff_value;
      }else{
        prox_input_analog_threshold = 0;
      }//if prox
    
    }// if button pressed
      
    calibrate_timer = timer; 
  }
  
  //if(RUNNING_UNO){Serial.print(prox_input_analog_threshold);Serial.print("\t|cal|\t");Serial.println(digitalRead(button_1));}

}




