#! /usr/bin/python3
import perfiles_pb2
#import sys


usuarioActual = ""
presetActual1 = ""
presetActual2 = ""
presetActual3 = ""

# Recibir el perfil de ./PERFILES_FILE
def readPerfil(usuario):

  # Extraer usuario + presets
  def listPerfil():

    for i in perfiles.perfil:
      print ("")

      if i.user == usuario:
        global usuarioActual
        usuarioActual = i.user
        print ("Username: ", usuarioActual)

        global passwordActual
        passwordActual = i.password
        print ("Password: ", passwordActual)
        
        for j in i.preset:
          if j.numPreset == perfiles_pb2.Perfil.PRESET1:
            global presetActual1
            presetActual1 = j.valorPreset
            print ("Preset 1: ", presetActual1)
          elif j.numPreset == perfiles_pb2.Perfil.PRESET2:
            global presetActual2
            presetActual2 = j.valorPreset
            print ("Preset 2: ", presetActual2)
          elif j.numPreset == perfiles_pb2.Perfil.PRESET3:
            global presetActual3
            presetActual3 = j.valorPreset
            print ("Preset 3: ", presetActual3)
        


  # Leer el archivo ./PERFILES_FILE
  perfiles = perfiles_pb2.Perfiles()

  f = open("./PERFILES_FILE", "rb")
  perfiles.ParseFromString(f.read())
  f.close()

  listPerfil()

  
