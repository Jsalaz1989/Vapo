#include <UnoWiFiDevEd.h>
#include <Wire.h>

char json[256];
bool publicado = false;
int control = 0;
int lastControl;
long tRef = millis();


#define CONNECTOR "mqtt"
#define TOPIC1 "vape/temp"
#define TOPIC2 "vape/control"

// inicializar el monitor serie, I2C, y MQTT
void setup() 
{
  Serial.begin(9600);
  
  Wire.begin(1);                    // establecerse como esclavo I2C en la dirección 1
  Wire.onReceive(receiveEvent);     // ejecutar función al recibir por I2C
  Wire.onRequest(requestEvent);     // ejectura
  
  Ciao.begin();                     // mqtt
}

// envíar json de temperaturas y esperar comandos remotos
void loop() 
{
  delay(500);

  if (publicado == false)                   // publicar json sólo si no se ha publicado ya        
  {
    mqttPub(json);  
  }

  control = mqttSub();                      // subscribirse a comandos remotos
}
