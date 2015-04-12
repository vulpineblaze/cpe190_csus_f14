

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


