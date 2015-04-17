

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






