/*
 *  Establece la temperatura deseada como consigna y la muestra en pantalla.
 */

// incrementar la consigna en uno mientras se mantenga presionado el pulsador TEMPMAS
void incrementSP()
{
  ON = false;             // pausar las funciones del vaporizador
  LCDtemp(SPactual);   

  while (digitalRead(TEMPMAS) == HIGH)
  {
    SPactual++;
    LCDtemp(SPactual);   
    delay(26000);
  }
  
  MsTimer2::start();      // iniciar cuenta para rehabilitar la marca ON
}


// disminuir la consigna en uno mientras se mantenga presionado el pulsador TEMPMENOS
void decrementSP()
{
  ON = false;             // pausar las funciones del vaporizador
  LCDtemp(SPactual);   

  while (digitalRead(TEMPMENOS) == HIGH)
  {
    SPactual--;
    LCDtemp(SPactual);   
    delay(26000);
  }
  
  MsTimer2::start();      // iniciar cuenta para rehabilitar la marca ON   
}


// variar la cosigna según un potenciómetro
void regTemp()
{
  ON = false;             // pausar las funciones del vaporizador
  LCDtemp(SPactual);   
  
  int SPactual1; 
  int SPactual2;
  int cont = 0;
  
  while (cont < 250 && SPactual1 == SPactual2)      // comparar valores del potenciómetro
  {
    SPactual2 = map(analogRead(REGTEMP), 0, 1023, 180, 280);      // interpolar lectura analógica entre 180 y 280 °C
    LCDtemp(SPactual2);                                           // mostrar último valor 

    SPactual1 = SPactual2;                                        // almacenar última lectura
    cont++;                                                       // contador sirve como temporizador
  }

  SPactual = SPactual2;                             // actualizar consigna con último valor de potenciómetro
  
  MsTimer2::start();   
}


// recibir valor de consigna de la interfaz remota
void enterSP(int SPdeseada)
{
  SPactual = SPdeseada;
  LCDtemp(SPactual);
  MsTimer2::start();
}

// habilitar las funciones del loop() y confirma la nueva consigna con un zumbido
void habilitar()
{
  ON = true;              
  tone(ZUMB, 600, 200);   // confirmar la nueva consigna
  lcd.clear();
  tRef = 5000;       // acelerar la transición
  MsTimer2::stop();       // detener el temporizador
}
