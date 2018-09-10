#!/usr/bin/python3
import http.client
import urllib.request
import urllib.parse
import json

import time

# Enviar sesión y temperaturas a Carriots
def postCarriots(mydata):
    api_url = "http://api.carriots.com/streams"
    device = "RPi@jsalaz1989.jsalaz1989" 
    api_key = "ccac8a816ebe0554d68294cfbffa8cd9c33bfb75e5795d8fc337167d285e915d"
    content_type = "application/json"     


    timestamp = int(time.time())
    
    params = {"protocol": "v2",
                  "device": device,
                  "at": timestamp,
                  "data": mydata}
    binary_data = json.dumps(params).encode('ascii')

    header = {"User-Agent": "raspberrycarriots", "Content-Type": content_type,"carriots.apikey": api_key}

    req = urllib.request.Request(api_url,binary_data,header)
    f = urllib.request.urlopen(req)
    print(f.read().decode('utf-8'))


# Recibir sesión y temperatura de Carriots
def getCarriots():

    api_url = "http://api.carriots.com/streams"
    api_key = "ccac8a816ebe0554d68294cfbffa8cd9c33bfb75e5795d8fc337167d285e915d"
    content_type = "application/json"     


    header = {"carriots.apikey": api_key}

    req = urllib.request.Request(api_url,None,header)
    req.get_method = lambda: "GET"
    f = urllib.request.urlopen(req)

    data=json.loads(f.read().decode('utf-8'))
    return data


# Borrar de Carriots los datos de la sesión
def deleteCarriotsSession(sesion):

    data = getCarriots()
    total = data['total_documents']

    for i in range(total):

        if data['result'][i]['data']['sesion'] == sesion:

            id_developer = data['result'][i]['id_developer']

            api_url = "http://api.carriots.com/streams/" + id_developer + "/"
            api_key = "ccac8a816ebe0554d68294cfbffa8cd9c33bfb75e5795d8fc337167d285e915d"
            print (api_url)

            params = {"protocol": "v2"}
            binary_data = json.dumps(params).encode('ascii')
            header = {"carriots.apikey": api_key}
            req = urllib.request.Request(api_url,binary_data,header)
            req.get_method = lambda: "DELETE"
            f = urllib.request.urlopen(req)

