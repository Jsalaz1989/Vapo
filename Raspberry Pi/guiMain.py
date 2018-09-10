#fuente: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

#!/usr/bin/python3

import tkinter as tk                
from tkinter import font  as tkfont 
from tkinter import *
from tkinter import messagebox

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as animation
from matplotlib import style


import guiHistorial
from guiHistorial import *

import mqttVape
from mqttVape import *

import mongoVape
from mongoVape import *

import hilos
from hilos import crearHilos
crearHilos()


import readmessage
from readmessage import *

usuario = ""
preset1 = ""
preset2 = ""
preset3 = ""


# Borrar la info de mongo (borrar la gráfica) cada vez que arrancas el programa
arranque = True 
if arranque == True:
    deleteAllMongo()
    arranque = False


# Gráfica de tiempos y temperatura actuales    
f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
       
# Rellena la gráfica con los datos de mongo
def animate(i):
    
    if mqttVape.On == False: # borrar la info de mongo (borrar la gráfica) cada vez que apagas la sesión
        deleteAllMongo()        
            
    
    data = getMongo()
    total = data['_meta']['total']

    tiempos = []
    temps = []

    # Llenar las listas tiempos y temps con los datos de mongo    
    for j in range(total):

        dataTiempo = data['_items'][j]['t']
        tiempos.append(dataTiempo)

        dataTemp = data['_items'][j]['T']
        temps.append(dataTemp)
        
    print("De mongo se saca la lista tiempos = ", tiempos)
    print("De mongo se saca la lista temps = ", temps)


    a.clear() # borrar la gráfica cada vez 
    a.plot(tiempos, temps) # rellenar la gráfica con las listas actualizadas



# Inicializar container y alternar entre frames
class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # Contiene a los frames superpuestos
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Main, CambiarUsuario):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # todos los frames superpuesto en el mismo sitio
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("CambiarUsuario") # la primera página mostrada es la de elegir el perfil

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


# Panel de Control
class Main(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        pubControl(0) # preparar al Arduino para que pueda recibir las siguientes publicaciones


        # GRÁFICA
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=100, pady=100) 


        # BARRA DE NAVEGACIÓN
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        def on_key_event(event):
            print('you pressed %s' % event.key)
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect('key_press_event', on_key_event)


        def _quit():
            root.quit()     # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate


        # USUARIO
        usuario_label = Label( self, text = "Usuario:", relief = FLAT, font=("Helvetica", 20))
        usuario_label.place(x = 180,y = 20)

        # Si cambia el usuario, actualizar la variable con la info del protobuf
        def actualizarUsuario():
            usuario = readmessage.usuarioActual
            usuario_val = StringVar()
            usuario_label2 = Label( self, textvariable = usuario_val, relief = RIDGE, font=("Helvetica", 20) )
            usuario_label2.place(x = 300,y = 20)
            usuario_val.set(usuario)
            
            self.after(500, actualizarUsuario) # actualizar cada medio segundo
        
        actualizarUsuario()

        # Establecer los valores iniciales, aunque suelen ser strings vacíos
        usuario_val = StringVar()
        usuario_label2 = Label( self, textvariable = usuario_val, relief = RIDGE, font=("Helvetica", 20) )
        usuario_label2.place(x = 300,y = 20)
        usuario_val.set(usuario)

        # Volver al frame inicial donde se elije el perfil
        boton_cambiar_usuario = tk.Button(self, text = "Cambiar de usuario", command=lambda: controller.show_frame("CambiarUsuario"))
        boton_cambiar_usuario.place(x = 450,y = 23)

        # SESIÓN ACTUAL
        
        Sesionbox1 = Label( self, text = "Sesión: ", relief = FLAT, font=("Helvetica", 14) )
        Sesionbox1.place(x = 500,y = 70)

        sesion_val = StringVar()
        Sesionbox2 = Label( self, textvariable = sesion_val, relief = RIDGE, font=("Helvetica", 14) )
        Sesionbox2.place(x = 580,y = 70)

        def actualizarSesion():            
            if mqttVape.On == False:
                sesion_val.set("")
            else:             
                sesion_val.set(str(mqttVape.sesion))
            self.after(500, actualizarSesion)
        
        actualizarSesion()
        

        #TEMPERATURA ACTUAL
        Tempbox1 = Label( self, text = "Temperatura Actual: ", relief = FLAT, font=("Helvetica", 14) )
        Tempbox1.place(x = 100,y = 70)

        temp_val = StringVar()
        Tempbox2 = Label( self, textvariable = temp_val, relief = RIDGE, font=("Helvetica", 14) )
        Tempbox2.place(x = 310,y = 70)

        def actualizarTemp():
            temp_val.set(str(mqttVape.temp) + " ºC")
            self.after(500, actualizarTemp)
        
        actualizarTemp()


        # HISTORIAL
        ver_historial = tk.Button(self, text="Ver Historial", command = guiHistorial)
        ver_historial.place(x = 600,y = 250)
        

        #BOTÓN ON
        led_on = Canvas(self, width=25, height=25)
        oval1 = led_on.create_oval(5,5,22,22,fill='grey')
        led_on.place(x = 140,y = 520)

        def leerOn():
            if mqttVape.On == True:
                oval1 = led_on.create_oval(5,5,22,22,fill='green')
            elif mqttVape.On == False:
                oval1 = led_on.create_oval(5,5,22,22,fill='grey')
            self.after(500, leerOn)

        leerOn()
                
        boton_on = Button(self, text = "ON", command = lambda: pubControl(999)) # 999 es el código para encender/apagar, los demás valores son temperaturas
        boton_on.place(x = 130,y = 550)


        #SP
        temp_arriba = Button(self, text = "+1", width = 2, command = lambda: pubControl(int(mqttVape.SP) + 1)) # SP++
        temp_arriba.place(x = 300,y = 540)

        temp_abajo = Button(self, text = "-1", width = 2, command = lambda: pubControl(int(mqttVape.SP) - 1)) # SP--
        temp_abajo.place(x = 300,y = 570)

        label_SP = Label( self, text = "SP", relief = FLAT, font=("Helvetica", 14))
        label_SP.place(x = 380, y = 520)

        sp_val = StringVar()
        label_SPtemp = Label( self, textvariable = sp_val, relief = RIDGE, font=("Helvetica", 16) )
        label_SPtemp.place(x = 360, y = 550)
        sp_val.set(mqttVape.SP)
        
        def actualizarSP():
            sp_val.set(str(mqttVape.SP) + " ºC")
            self.after(3000, actualizarSP)

        actualizarSP()
        

        entrySP = Entry(self, width = 5)
        entrySP.place(x = 375, y = 580)

        # al darle al Enter, se publica el valor introducido en la casilla
        def enterSP(event):
            print(entrySP.get())
            global SP
            SP = entrySP.get()
            pubControl(SP)
        entrySP.bind('<Return>', enterSP)


        #BOTONES PRESET
        def actualizarPresets():
            preset1 = readmessage.presetActual1
            preset2 = readmessage.presetActual2
            preset3 = readmessage.presetActual3

            # Actualizar el valor publicado al hacer click al botón
            presetButton1 = Button(self, text= str(preset1), command = lambda: pubControl(preset1)) 
            presetButton1.place(x = 440,y = 520)

            presetButton2 = Button(self, text = str(preset2), command = lambda: pubControl(preset2))
            presetButton2.place(x = 440,y = 550)

            presetButton3 = Button(self, text = str(preset3), command = lambda: pubControl(preset3))
            presetButton3.place(x = 440,y = 580)

            self.after(3000, actualizarPresets)

        actualizarPresets()
        
        presetButton1 = Button(self, text= str(preset1), command = lambda: pubControl(preset1))
        presetButton1.place(x = 440,y = 520)

        presetButton2 = Button(self, text = str(preset2), command = lambda: pubControl(preset2))
        presetButton2.place(x = 440,y = 550)

        presetButton3 = Button(self, text = str(preset3), command = lambda: pubControl(preset3))
        presetButton3.place(x = 440,y = 580)
        

# Página de elección del perfil
class CambiarUsuario(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Elije tu perfil:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # Esta función permite llamar a dos funciones al hacer click sobre un botón
        def elegirUsuario(usuario):
            readPerfil(usuario)
            controller.show_frame("Main")

        buttonUsuario1 = tk.Button(self, text="Jaime", command=lambda: elegirUsuario("Jaime"))
        buttonUsuario1.place(x = 300, y = 100)

        buttonUsuario2 = tk.Button(self, text="Pepito", command=lambda: elegirUsuario("Pepito"))
        buttonUsuario2.place(x = 300, y = 150)
    

  

if __name__ == "__main__":
    app = SampleApp()    
    ani = animation.FuncAnimation(f, animate, interval = 6000)
    #ani = animation.FuncAnimation(f, animate, interval = 1000)
    app.mainloop()
