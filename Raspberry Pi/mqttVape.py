import paho.mqtt.client as mqtt  #import the client1
import json
import time

import mongoVape
from mongoVape import postMongo

import carriotsVape
from carriotsVape import *

temp = 0
SP = 0
tiempo = 0

On = False
tRef = time.clock()
sesion = "A"


broker_address="127.0.0.1"


# Enviar al Arduino una consigna de temperatura o una señal de apagado/encendido (999)
def pubControl(value):

    def on_connect(client, userdata, flags, rc):
        m="Pub connected with flags: " + str(flags) + " result code: " + str(rc) + " client1_id: " + str(client)
        print(m)

    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker_address, 1883, 60)

    client.loop_start()    
    client.publish("vape/control", int(value)) # Publicar el valor
    time.sleep(1.5)
    client.publish("vape/control", 0) # Necesario para que el Arduino pueda recibir el siguiente comando

    if int(value) == 999: # 999 es el código para encender/apagar, los demás valores son temperaturas
        onOff()

    client.disconnect()
    client.loop_stop()
    

# Recibir del Arduino el tiempo y temperatura actual
def subTemp():

    def on_connect(client, userdata, flags, rc):

        print("Sub connected with result code "+str(rc))
        client.subscribe("/vape/temp")

    
    def on_message(client1, userdata, message):

        jsonms = message.payload.decode("utf-8")
        dict = json.loads(jsonms)

        
        global On                
        On = True       # si recibe un mensaje, indica que está encendido

        global tRef             # para un watch-dog
        tRef = time.clock()
        
        # No puedo post a mongo sin antes reconstruir el dict (???)
        tiempo = dict['t']
        global temp
        temp = dict['T']
        global SP
        SP = dict['SP']
        dict = {
                't': str(tiempo),
                'T': str(temp),
                'SP': str(SP)
               }
        
        postMongo(dict) # enviar datos a mongo (para mostrarlos en la gráfica)

            
        dict['sesion'] = sesion # añadir el dato de la sesión para enviarlo junto con el dict anterior a carriots 

        time.sleep(1)
        postCarriots(dict) # enviar datos a carriots para mostrarlos en el historial



    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address, 1883, 60)


    client.loop_start() # no me funciona con loop_forever()

    time.sleep(0.3) # ralentizar al loop_start()

    # Si no recibe datos del Arduino en 8 segundos, asumir que está apagado
    if time.clock() - tRef >= 8:
        
        global On
        On = False

        cambioSesion()
        
        global tRef
        tRef = time.clock()
        

    client.loop_stop()


def cambioSesion():
        
    if sesion == "A":
        global sesion
        sesion = "B"
        

    elif sesion == "B":
        global sesion
        sesion = "A"
        

    deleteCarriotsSession(sesion) # borrar los datos de carriots de esta sesión para llenarlos con la nueva sesión

    print("La sesión ha cambiado a: ", sesion)

# Indicar al gui si el Arduino está encendido/apagado
# Intento evitar que el Arduino, aún apagado, tenga que constantemente publicar que lo está
def onOff():
    if On == True:
        global On
        On = False

    elif On == False:
        global On
        On = True
        cambioSesion()
