/*
 *  Subscribirse a comandos de control por MQTT.
 */


// recibir comandos y convertirlos en un entero
int mqttSub()
{
  CiaoData data = Ciao.read(CONNECTOR, TOPIC2);             // #define CONNECTOR "mqtt"
                                                            // #define TOPIC2 "vape/control"
  if (!data.isEmpty())
  {
    const char* value = data.get(2);                        // recibir comando en formato char
    
    int valueInt = atoi(value);                             // convertir char a int 
    
    Serial.print("Subscrito y recibido valor int =  ");
    Serial.println(valueInt);
    
    return valueInt;
  }
}
