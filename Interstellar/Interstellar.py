from firebase import firebase
import random
import os

pressure = './ReadPressure'
temp = './ReadTemperature'
firebase = firebase.FirebaseApplication('https://interstellar-d796a.firebaseio.com/', None)
pressureData = os.popen(pressure).read()
tempData = os.popen(temp).read()

respuesta = firebase.patch('/Ship/SensorData', {'Atmos Pressure (hPA)': pressureData, 'Temperature (C)': tempData})
print(respuesta)


salida = firebase.get('/data','')
print(salida)

