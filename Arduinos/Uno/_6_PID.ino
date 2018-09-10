/*
 *  Controlador PID que cuya salida es el valor PWM del transistor del horno, que se introduce como parámetro en la función horno().  
 */


double PWM_PID()
{
  Input = temp();             // vigilar temperatura actual
  Setpoint = SPactual;        // seguir el setpoint actual
  
  PIDhorno.Compute();         // calcular salida PWM
  
  return Output;              // devolver salida PWM
}
