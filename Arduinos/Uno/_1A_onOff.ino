/*
 *  Enciende o apaga al vaporizador dependiendo del estado actual. Por seguridad y ahorro de energía, al transcurrir un valor determinado, se apaga.
 */

// si el vaporizador está apagado, enciéndelo y viceversa
void onOff() 
{
  if(!ON)                            
  {    
    on();   
  }
  else 
  {                                 
    off();
  }
}                                          

void on()
{
  TIMSK1 |= (1 << OCIE1A);          // empezar la temporización de seguridad
  tone(ZUMB, 400, 200);
  digitalWrite(LCD, HIGH);
  ON = true;
  tRefTemp = millis();
}

void off()
{
  TIMSK1 &= ~(1 << OCIE1A);         // detener la temporización de seguridad
  tone(ZUMB, 200, 400);
  digitalWrite(LCD, LOW);
  ON = false;
}
