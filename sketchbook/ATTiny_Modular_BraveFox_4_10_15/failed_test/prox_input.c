#include "prox_input.h"



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

  
      if(isProxOutOn){
        prox_input_analog_lit = prox_input_analog;
      }else{
        prox_input_analog_unlit = prox_input_analog;
      }
      
      on_off_diff_value = prox_input_analog_lit - prox_input_analog_unlit;
      
      if(on_off_diff_value > prox_input_analog_threshold){
        decision = true;
      }else{
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

