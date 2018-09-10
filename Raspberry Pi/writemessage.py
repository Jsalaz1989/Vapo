#! /usr/bin/python3
import perfiles_pb2



# Crear nuevo perfil
def PedirPerfil(perfil):

  perfil.user = input("Usuario: ")
  perfil.password = input("Contraseña: ")

  # Crear múltiples presets
  while True:
    number = input("Introducir un valor de preset (o dejar en blanco para acabar): ")
    if number == "":
      break

    preset = perfil.preset.add() # crear un nuevo preset
    preset.valorPreset = number # asignar el valor de preset
    
    num = input("Preset 1, 2, o 3?: ") # asignar valor a uno de los tres presets
    if num == "1":
        preset.numPreset = perfiles_pb2.Perfil.PRESET1
    elif num == "2":
        preset.numPreset = perfiles_pb2.Perfil.PRESET2
    elif num == "3":
        preset.numPreset = perfiles_pb2.Perfil.PRESET3
    

     
file = "./PERFILES_FILE"

perfiles = perfiles_pb2.Perfiles() # crear una instancia de tipo Perfil

# Abrir el archivo existente, o crear uno nuevo si no existe
try:
  f = open(file, "rb") 
  perfiles.ParseFromString(f.read())
  f.close()
except IOError:
  print (file + ": Could not open file.  Creating a new one.")

# Ejecutar la función PedirPerfil para crear un nuevo perfil
PedirPerfil(perfiles.perfil.add())

# Escibir los datos al archivo
f = open(file, "wb") 
f.write(perfiles.SerializeToString())
f.close()
