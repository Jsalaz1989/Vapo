from flask import Flask
from flask import render_template
import datetime
import jinja2


import carriotsVape
from carriotsVape import getCarriots


app = Flask(__name__)


@app.route("/usuario/<sesion>")
def sesionData(sesion):
    
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")

   templateData = {'title' : 'Datos de Sesión!', 'time': timeString}

   data = getCarriots()
   total = data['total_documents']

   templateData['sesion'] = sesion

   for i in range(total):

       if data['result'][i]['data']['sesion'] == sesion:
           templateData['tiempo' + str(i)] = data['result'][i]['data']['t']
           templateData['temp' + str(i)] = data['result'][i]['data']['T']
           
   return render_template('main.html', **templateData)


if __name__ == "__main__":
   # Run
   app.run(host='0.0.0.0', port=8080, debug=True)
