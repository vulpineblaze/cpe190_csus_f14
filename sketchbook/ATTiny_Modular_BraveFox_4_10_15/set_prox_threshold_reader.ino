

void set_prox_threshold_reader(){
  
  // if the set-threshold button goes low, it is pressed
  if(digitalRead(button_1)){
    
  }else{
    
    // make sure the proxOUT is on, then set calibrate

    if(on_off_diff_value > 0){
      prox_input_analog_threshold = on_off_diff_value;
    }else{
      prox_input_analog_threshold = 0;
    }
    

    
  }
  //if(RUNNING_UNO){Serial.print(prox_input_analog_threshold);Serial.print("\t|cal|\t");Serial.println(digitalRead(button_1));}

}




