/*
 *  Publicar json por MQTT.
 */

// publicar un array de caracteres
void mqttPub(char jsonArray[])
{
  Ciao.write(CONNECTOR, TOPIC1, jsonArray);       // #define CONNECTOR "mqtt"
                                                  // #define TOPIC1 "vape/temp"
  Serial.print("Publicado json: ");
  Serial.println(jsonArray);

  publicado = true;                               // indica que ya se han publicado los datos
}
