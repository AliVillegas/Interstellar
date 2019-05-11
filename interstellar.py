from firebase import firebase
import random
import os

cmd = './SensorData'
firebase = firebase.FirebaseApplication('https://interstellar-d796a.firebaseio.com/', None)
sensor = os.popen(cmd).read()
respuesta = firebase.post('/data', {'sensor': sensor, 'name':'Interstellar-069'})
print(respuesta)


salida = firebase.get('/data','')
print(salida)

