/*
 *  Envía tiempos (intervalos desde la primera lectura de temperatura) y temperaturas en formato JSON al Arduino Uno Wifi. 
 */


#include <ArduinoJson.h>

// escribir un json en el I2C como maestro
void enviarTemp() 
{
  if (tRefTemp == 0)
  {
    tRefTemp = millis();
  }
  
  int tiempo = int((millis() - tRefTemp)/1000);     // calcular intervalo en segundos
  int temperatura = temp();;

  StaticJsonBuffer<256> jsonBuffer;                 // reservar memoria para el JSON (array de caracteres)
  
  JsonObject& json = jsonBuffer.createObject();     // crear objeto JSON = {"t": tiempo, "T": temperatura, "SP": SPactual}
  json["t"] = tiempo;                               
  json["T"] = temperatura;
  json["SP"] = SPactual;

  json.printTo(jsonArray, sizeof(jsonArray));       // rellenar array de caracteres

 
  Wire.beginTransmission(1);          // transmitir a dispositivo #1
  Wire.write(jsonArray);              // enviar JSON por I2C 
  Wire.endTransmission();             // finalizar transmisión
  
  Serial.print("Temperatura enviada por I2C a Uno Wifi: ");
  Serial.println(jsonArray);    
}


// Leer del I2C un comando como maestro
void recibirControl()
{  
  byte a,b;

  Wire.requestFrom(1, 2);     // exigir 2 bytes del esclavo #1

  while (Wire.available())    
  { 
    a = Wire.read();          // leer el primer byte
    b = Wire.read();          // leer el segundo byte

    message = a;                    // almacenar el primer byte leído en el segundo byte de message
    message = message << 8 | b;     // almacenar el segundo byte leído en el primer byte de message

    Serial.print("Recibido del Uno Wifi el message = ");     
    Serial.println(message);              

    switch (message)
    {
      case 999:     // comando ON
      {
        onOff();            // apagar o encender el vaporizador
        break;
      }
      case 255:     // ignorar valor 255
      {
        break;
      }
      case 300:     // convertir valor 300 en 255
      {
        message = 255;
        enterSP(message);   // asignar valor a SPactual 
        break;
      }
      default:
        enterSP(message);   // asignar valores distintos a 999, 255, y 300 a SPactual
      break;
    }  
  }  

  delay(500);
}
