/*
 *  Envía un array de 2 bytes por I2C al Arduino Uno.
 */


// unir 2 bytes en un array y enviar por I2C
void requestEvent()
{
  if (control != lastControl && lastControl == 0)     // si el comando actual es distinto al anterior y el anterior es cero
  {
    byte myArray[2];

    myArray[0] = (control >> 8) & 0xFF;               // mover segundo byte al primer byte y aislar el primer byte (0xFF = 11111111)
    myArray[1] = control & 0xFF;                      // aislar segundo byte
    
    Wire.write(myArray, 2);                           // enviar 2 bytes por I2C
    
    Serial.print("Enviado por I2C a Uno: ");
    Serial.print(myArray[0]);
    Serial.println(myArray[1]);
  }

  lastControl = control;
}
