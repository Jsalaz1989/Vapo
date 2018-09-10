/*
 *  Pantalla de bienvenida y pantalla de temperatura actual.
 */


// bienvenida
void LCDinit()
{
  lcd.setCursor(3,0);
  lcd.print("Bienvenid@");
}


// mostrar la temperatura actual
void LCDtemp(double temp)                                                                   
{
  if (ON)
  {
    lcd.clear();              // borra la pantalla de bienvenida la primera vez que se enciende el vaporizador
  }
  
  lcd.setCursor(0,0);
  lcd.print("Temp: ");        

  // posicionar al valor de la temperatura actual según su número de dígitos
  if (temp < 100)
  {
    lcd.setCursor(7,0);           
  }
  else
  {
    lcd.setCursor(6,0);           
  }
  
  lcd.print(temp);            // imprimir la temperatura actual
}
