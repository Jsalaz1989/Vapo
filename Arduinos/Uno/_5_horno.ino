/*
 *  Asigna un valor PWM a la patilla digital del transistor del horno. 
 */


void calentarHorno(int valorPWM)
{
  analogWrite(HORNO, valorPWM);   // escribir el valor PWM (la salida del controlador PID) en el pin digital del transistor del horno
}
