/*
 *  Recibir array de json del Arduino Uno.
 */

// recibir caracteres por I2C como esclavo y almacenar en un array
int receiveEvent(int bytes) 
{
  int i = 0;

  while (Wire.available())
  {
    json[i] = Wire.read();                      // leer los bytes en el I2C y almacenar en un array
    
    Serial.print("Recibido del Uno: ");
    Serial.println(json[i]);       
    
    i++;  
    publicado = false;                          // indicar que hay que publicar estos datos
  }  
}
