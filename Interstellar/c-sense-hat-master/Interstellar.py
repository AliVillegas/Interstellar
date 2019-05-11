from firebase import firebase
import random
import os

cmd = './humidity'
firebase = firebase.FirebaseApplication('https://interstellar-d796a.firebaseio.com/', None)
sensor = os.popen(cmd).read()
respuesta = firebase.post('/data', {'sensor': sensor})
print(respuesta)


salida = firebase.get('/data','')
print(salida)
