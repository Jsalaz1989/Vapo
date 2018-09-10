  /*  
 *  Autor: Jaime Salazar Lahera
 *  Fecha: 01.06.17
 *  Proyecto: Vaporizador, proyecto de Microcontroladores
 */

#include "PinChangeInt.h"
#include <PID_v1.h>
#include <MsTimer2.h> 
#include <LiquidCrystal.h>
#include <Wire.h>


LiquidCrystal lcd(9, 8, 7, 6, 5, 4);                  // inicializar los pins del LCD

bool ON = false;                                      // activa o desactiva al vaporizador
long int tRef = 0;                                    // ralentizar al loop()

// patillas
#define PULSON 13          // pulsador ON
#define REGTEMP A0         // regulador de temperatura
#define TEMPMAS 2          // pulsador incremento de temp
#define TEMPMENOS 3        // pulsador decremento de temp
#define HORNO 11           // transistor del horno
#define LCD 10             // encendido del LCD
#define ZUMB 12            // zumbador


// PID
double SPactual = 200;
double Kp = 3.2;
double Ki = 0.095;
double Kd = 4.5;
double Input, Output, Setpoint;
PID PIDhorno(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);


// I2C
int message;
char jsonArray[256];
long tRefTemp = millis();


// inicializar LCD, I2C, E/S, interrupciones, temporizadores, y PID
void setup() 
{
  Serial.begin(9600);
  
  // inicializar LCD
  lcd.begin(16,2);            // número de (columnas, filas) de la pantalla
  LCDinit();                  // mensaje de bienvenida

  Wire.begin();               // comunicación I2C
  
  // entradas y salidas
  pinMode(PULSON, INPUT);
  pinMode(REGTEMP, INPUT);
  pinMode(TEMPMAS, INPUT);
  pinMode(TEMPMENOS, INPUT);
  pinMode(HORNO, OUTPUT);
  //pinMode(LCDbacklight, OUTPUT);
  pinMode(LCD, OUTPUT);
  pinMode(ZUMB, OUTPUT);
  
  // interrupciones
  attachInterrupt(0, incrementSP, RISING);                        // interrupción HW digital por flanco positivo del pulsador ON
  attachInterrupt(1, decrementSP, RISING);                        // interrupción HW digital por flanco positivo del pulsador ON
  attachPinChangeInterrupt(PULSON, onOff, RISING);                // interrupción HW digital en patilla distinta a 2 o 3 
  attachPinChangeInterrupt(REGTEMP, regTemp, CHANGE);             // interrupción HW analógica por cambio del regulador de temperatura
  inicializarISR();                                               // incializar ISR del temporizador de seguridad

  MsTimer2::set(800, habilitar);                                  // establecer 800 milisegundos  
  
  // PID
  PIDhorno.SetOutputLimits(0, 255);                               // límites del PWM del horno
  PIDhorno.SetMode(AUTOMATIC);                                    // habilitar el PID    
}

void loop()
{   
  recibirControl();                        // recibir órdenes de control a través de I2C
  
  if (ON)                            // sólo ejecutar al estar encendido
  {
    // Ralentizar el loop()
    if (millis() - tRef >= 5000)     
    {  
      calentarHorno(PWM_PID());            // calentar horno según la salida PWM del PID

      LCDtemp(temp());                     // mostrar la temperatura actual
    
      enviarTemp();                        // enviar temperatura por I2C
    
      tRef = millis();  
    }
  }
}
