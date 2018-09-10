/*
 *  Devuelve la temperatura actual del horno y para presentarla en pantalla. 
 */

#include "max6675.h"

// inicializar al sensor
int CLK = 15;   // A1 = D15
int CS = 16;    // A2 = D16
int SO = 17;    // A3 = D17

MAX6675 termopar(CLK, CS, SO);

long tempTref = -3000;

// detecta la temperatura actual y la devuelve para su uso en LCDtempActual() y PWM_PID()
double temp()
{
  if (termopar.readCelsius() <= 290)                     // asegurarse de que no se ha excedido la temperatura máxima de seguridad
  {
    if (millis() - tempTref >= 3000)
    {
      return termopar.readCelsius();
      tempTref = tempTref + 3000;  
    }  
  }
  else                                                   // apagar si detecta temperatura excesiva
  {
    off();  
  }
}
