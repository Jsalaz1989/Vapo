#!/usr/bin/python3

from tkinter import *
from tkinter import messagebox


import matplotlib
matplotlib.use('TkAgg')
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


import carriotsVape
from carriotsVape import getCarriots


fA = Figure(figsize=(9, 3), dpi=100)
aA = fA.add_subplot(111)

fB = Figure(figsize=(9, 3), dpi=100)
aB = fB.add_subplot(111)



def animate(i):
    
    carriotsData = getCarriots()
    total = carriotsData['total_documents']


    tiemposA = []
    tempsA = []

    tiemposB = []
    tempsB = []

    print("")
    
    for j in range(total):

        if carriotsData['result'][j]['data']['sesion'] == "A":

            dataTiempoA = carriotsData['result'][j]['data']['t']
            tiemposA.append(dataTiempoA)

            dataTempA = carriotsData['result'][j]['data']['T']
            tempsA.append(dataTempA)

        elif carriotsData['result'][j]['data']['sesion'] == "B":

            dataTiempoB = carriotsData['result'][j]['data']['t']
            tiemposB.append(dataTiempoB)

            dataTempB = carriotsData['result'][j]['data']['T']
            tempsB.append(dataTempB)



            
    print("tiemposA = ", tiemposA)
    print("tempsA = ", tempsA)

    print("tiemposB = ", tiemposB)
    print("tempsB = ", tempsB)

    aA.clear()
    aA.plot(tiemposA, tempsA)

    aB.clear()
    aB.plot(tiemposB, tempsB)




def guiHistorial():

    top = Tk()
    top.geometry("1000x700")
    top.title("Historial")


    # SESIÓN A    
    sesionA_label = Label( top, text = "Sesión A:", relief = FLAT )
    sesionA_label.place(x = 60,y = 20)

    canvasA = FigureCanvasTkAgg(fA, master=top)
    canvasA.get_tk_widget().place(x = 60, y = 40)
        

    # SESIÓN B    
    sesionB_label = Label( top, text = "Sesión B:", relief = FLAT )
    sesionB_label.place(x = 60,y = 360)

    canvasB = FigureCanvasTkAgg(fB, master=top)
    canvasB.get_tk_widget().place(x = 60, y = 380)



    # Tasks
    aniA = animation.FuncAnimation(fA, animate, interval = 800)
    aniB = animation.FuncAnimation(fB, animate, interval = 1200)
    top.mainloop()

#guiHistorial()
