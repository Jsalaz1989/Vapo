Proyecto de la asignatura de Computadores y Programación del Máster. Es un sistema de traspaso de datos y comandos entre un vaporizador basado en Arduino (proyecto de la asignatura de Microntroladores y Lógica Programable) y una interfaz gráfica en una Raspberry Pi. 

El Arduino se comunica con la RPi mediante MQTT, la cual presenta los datos en una GUI y en la web (html, Flask), los almacena (mongoDB, Carriots, fichero .proto de perfiles) y envía comandos de vuelta al Arduino.
