

int avg_num = 20;

int decision_tally = 0;
int decision_tallies_required = 3;

bool poll_prox_input_reader(){
  bool decision = prox_input_state;
  
  bool isProxOutOn = digitalRead(proxOutReader);
  
  if(last_isProxOutOn != isProxOutOn){
    edge_margin_timer = timer;
    last_timer = timer;
    last_isProxOutOn = isProxOutOn;
  }
  
  if(edge_margin_timer != 0){
    if(timer - edge_margin_timer > edge_margin_micros ){ 
      
      prox_input_analog = analogRead(proxInSensor); //goes high when lit
      //colorWheelPOT_analog = analogRead(colorWheelPOT);


//  running_diff_prox_input_analog = (19*running_diff_prox_input_analog + abs(prox_input_analog-last_prox_input_analog))/20;

  
      if(isProxOutOn){
        prox_input_analog_lit = ((avg_num-1)*prox_input_analog_lit + prox_input_analog)/avg_num;
      }else{
        prox_input_analog_unlit = ((avg_num-1)*prox_input_analog_unlit + prox_input_analog)/avg_num;
      }
      
      on_off_diff_value = prox_input_analog_lit - prox_input_analog_unlit;
      
      if(on_off_diff_value > prox_input_analog_threshold){
        decision_tally +=1;
        if(decision_tally>decision_tallies_required){decision_tally=decision_tallies_required;}
        //decision = true;
      }else{
        decision_tally -=1;
        if(decision_tally<1){decision_tally=0;}
        //decision = false;
      }
      
      if(decision_tally>=decision_tallies_required){
        decision = true;
      }else if(decision_tally<1){
        decision = false;
      }
    
    
//      last_prox_input_analog = prox_input_analog;
//      last_prox_input_analog_lit = prox_input_analog_lit;
//      last_prox_input_analog_unlit = prox_input_analog_unlit;

      
      toggle_tally += 1;
      
//      if(RUNNING_UNO && toggle_tally > 20 ){
//        toggle_tally = 0;
//        Serial.print(prox_input_analog_threshold);
//        Serial.print("\t|prox|\t");
//        Serial.print(timer-edge_margin_timer);
//        Serial.print("\t|\t");
//        Serial.print(isProxOutOn);
//        Serial.print("|\t");
//        Serial.print(decision);
//        Serial.print("|\t");
//        Serial.print(on_off_diff_value);
//        Serial.print("|\t");
//        Serial.print(prox_input_analog_lit);
//        Serial.print("|\t");
//        Serial.print(prox_input_analog_unlit);    
//        Serial.print("|\t");
//        Serial.println(prox_input_analog);
//        //Serial.println(timer-last_timer);
//      }
      analogWrite(analogDebugOutput, on_off_diff_value );
      
      edge_margin_timer = 0;
    }
  }
  
  
  return decision;
  
}


