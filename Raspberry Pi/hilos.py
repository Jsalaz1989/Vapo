import threading
import time


import mqttVape
from mqttVape import *



class myThread(threading.Thread):

    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("Starting thread " + str(self.threadID))

        if self.threadID == 0:

            while True:
                
                print("subTemp() thread running")
                time.sleep(1)
                subTemp()
    
        #elif self.threadID == 1:

            #while True:

                #print("readPerfil() thread running")                
                #time.sleep(5)

                #readPerfiles()
                
                #print("In main.py, guiMain.usuario =  ", guiMain.usuario)
                #import readmessage

                #print("In main.py, readmessage.usuarioActual =  ", readmessage.usuarioActual)
                #print("In main.py, readmessage.presetActual1 =  ", readmessage.presetActual1)
                #print("In main.py, readmessage.presetActual2 =  ", readmessage.presetActual2)
                #print("In main.py, readmessage.presetActual3 =  ", readmessage.presetActual3)
                    

        print("Ending thread " + str(self.threadID))

def crearHilos():
    newThread0 = myThread(0)
    newThread0.start()


    newThread1 = myThread(1)
    newThread1.start()
