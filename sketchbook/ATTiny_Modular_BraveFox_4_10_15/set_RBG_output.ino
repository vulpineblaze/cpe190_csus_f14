


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







void set_RBG_output(int colorstate){

  //if(RUNNING_UNO){Serial.print(colorWheelPOT_analog);Serial.print("\t|\t");Serial.println(colorstate);}

  if (colorstate == 1){
    setColor(255, 0, 0);  // red
  }
  else if (colorstate == 2 ){
    setColor(255,140,0); //orange
  }
  else if (colorstate == 3 ){
    setColor(255, 215, 0);  // yellow  
  }
  else if (colorstate == 4 ){
    setColor(0, 128, 0);  // green
  }
  else if (colorstate == 5 ){
    setColor(0, 0, 255);  // blue
  }
  else if (colorstate == 6 ){
    setColor(128, 0, 128);  // purple
  }
  else if (colorstate == 7 ){
    setColor(255, 255, 255);  // white
  }
  else if (colorstate == 8 ){
    setColor(0, 0, 0);  // black
  }  
}


