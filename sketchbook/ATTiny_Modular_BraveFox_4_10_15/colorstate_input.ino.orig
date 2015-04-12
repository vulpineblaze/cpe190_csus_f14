
int colorstate_input(){

  //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}

  if (colorstate !=1 && colorWheelPOT_analog < color_multiple-color_dead_zone){
    colorstate = 1;  // red
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=2 && colorWheelPOT_analog >= color_multiple + color_dead_zone && colorWheelPOT_analog < color_multiple*2 - color_dead_zone){
    colorstate = 2;   //orange
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=3 && colorWheelPOT_analog >= color_multiple*2 + color_dead_zone && colorWheelPOT_analog < color_multiple*3 - color_dead_zone){
    colorstate = 3;  // yellow 
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=4 && colorWheelPOT_analog >= color_multiple*3 + color_dead_zone && colorWheelPOT_analog < color_multiple*4 - color_dead_zone){
    colorstate = 4;  // green
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=5 && colorWheelPOT_analog >= color_multiple*4 + color_dead_zone && colorWheelPOT_analog < color_multiple*5 - color_dead_zone){
    colorstate = 5;  // blue
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=6 && colorWheelPOT_analog >= color_multiple*5 + color_dead_zone && colorWheelPOT_analog < color_multiple*6 - color_dead_zone){
    colorstate = 6;  // purple
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=7 && colorWheelPOT_analog >= color_multiple*6 + color_dead_zone && colorWheelPOT_analog < color_multiple*7 - color_dead_zone){
    colorstate = 7;  // white
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }
  else if (colorstate !=8 && colorWheelPOT_analog >= color_multiple*7 + color_dead_zone ){
    colorstate = 8;  // black
    //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}
  }  
  return colorstate;
}


