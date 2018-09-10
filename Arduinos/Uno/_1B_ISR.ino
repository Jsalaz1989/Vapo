/*
 *  Inicializa la interrupción por temporizador, que se lanza cada segundo. Cada 30 minutos se lanza llama a la función off() para apagar el vaporizador. 
 */

int segundos = 0;           // manteniene la cuenta de interrupciones consecutivas
int tiempoApagado = 600;    // apagar cada 600 seg = 5 min, 1800 seg = 30 min

// inicilizar al temporizador 1 con una cuenta de 1 segundo, en modo CTC, y con prescaler de 1024
void inicializarISR()
{
  cli();          // dishabilitar interrupciones globales
  TCCR1A = 0;     // resetear el registro TCCR1A entero a 0
  TCCR1B = 0;     // resetear el registro TCCR1B entero a 0

  OCR1A = 15624;              // establecer una comparación con este valor, que asegura interrupciones cada 1 segundo
  TCCR1B |= (1 << WGM12);     // modo CTC
  TCCR1B |= (1 << CS10);      // prescaler de 1024 
  TCCR1B |= (1 << CS12);      // prescaler de 1024
  TIMSK1 |= (1 << OCIE1A);    // habilitar la interrupción de comparación
  sei();                      // habilitar interrupciones globales
}

// cada 1800 interrupciones se lanza la función off()
ISR(TIMER1_COMPA_vect)
{
    segundos++;           // añadir 1 segundo al contador
    
    if (segundos == tiempoApagado)                // si pasan 1800 segundos, apagar el sistema                         
    {
        segundos = 0;     // reiniciar la cuenta
        off();            // apagar el sistema
    }
}   
