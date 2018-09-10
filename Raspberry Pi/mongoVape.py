#!/usr/bin/python3
import http.client
import urllib.request
import urllib.parse
import json
import time

api_url = "http://127.0.0.1:5000/medida/"

# Borrar los datos de mongo (para borrar la gráfica)
def deleteAllMongo():

    data = getMongo()
    total = data['_meta']['total']

    time.sleep(1)
    while total > 0:

        time.sleep(0.3)

        data = getMongo()
        total = data['_meta']['total']
        
        if total == 0: # no debería hacer falta pero previene un error: out of range 
            break

        else:
            
            for i in range(total):

                time.sleep(0.3)

                id = data['_items'][i]['_id']
                etag = data['_items'][i]['_etag']
                
                api_url = "http://127.0.0.1:5000/medida/" + str(id)
                req = urllib.request.Request(api_url)
                req.add_header('If-Match', str(etag))

                req.get_method = lambda: "DELETE"
                f = urllib.request.urlopen(req)


# Enviar tiempo y temperatura a mongo
def postMongo(dict):

    print("Posting to mongo dict = ", dict)
  
    headers = {'Content-type': 'application/json; charset=utf-8'}
    binary_data = json.dumps(dict).encode('ascii')
    req = urllib.request.Request(api_url,binary_data,headers)

    req.get_method = lambda: "POST"
    f = urllib.request.urlopen(req)

# Leer los datos de mongo
def getMongo():
    
    req = urllib.request.Request(api_url)

    req.get_method = lambda: "GET"
    f = urllib.request.urlopen(req)

    data=json.loads(f.read().decode('utf-8'))
    return data




