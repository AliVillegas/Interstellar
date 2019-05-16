from firebase import firebase
import random
import os
from subprocess import call
from sense_hat import SenseHat #To do in C
import time
import math
from os import walk
import pi3d
def truncate(number, digits):
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper
#To do in C

sense = SenseHat()
sense.set_imu_config(False, True, False)
coordinates =  {"x":0.0,"y":0.0, "z": 0.0}
print("Original Position:")
print(coordinates)
averageXaccel = 0.0
averageYaccel = 0.0
averageZaccel = 0.0
spanAcceleration = 5#30 yielded good results
earthGAccel = -0.96
averageZgyr = 0.0
DISPLAY = pi3d.Display.create(x=80,y=100,w= 1000, h = 1000, background=(0,0,0,1),use_pygame=True,frames_per_second = 30)
#DISPLAY = pi3d.Display.create()
shader = pi3d.Shader('uv_light')
flatsh = pi3d.Shader("uv_flat")
spaceShipTexture = pi3d.Texture('spaceshipTexture.jpg')
#backgroundTexture = pi3d.Texture('spaceTexture.jpg')

ship = pi3d.Sphere(z=20.0)
background = pi3d.Plane(w=50, h=50, name="stars", z=30)
escapeSimulation = pi3d.Keyboard()
newCoordinates = {'x':1, 'y':1, 'z':1}

flashGreen = "./FlashGreen"
flashRed = "./FlashRed"
pressure = './ReadPressure'
temp = './ReadTemperature'


#os.popen(flashRed)
rotCounter = 0
while DISPLAY.loop_running():
	ship.draw(shader,[spaceShipTexture])
	averageXaccel = 0.0
	averageYaccel = 0.0
	averageZaccel = 0.0
	for x in range(0,spanAcceleration):
		raw = sense.get_accelerometer_raw()
		averageXaccel += round(raw["x"],3)
		averageYaccel += round(raw["y"],3)
		averageZaccel += round(raw["z"],3) + earthGAccel
		raw = sense.get_gyroscope_raw()
		averageZgyr += round(raw["z"],3)
		#print("x: {x}, y: {y}, z: {z}".format(**raw))
	
	averageXaccel = averageXaccel / spanAcceleration
	averageYaccel = averageYaccel / spanAcceleration
	averageZaccel = averageZaccel / spanAcceleration
	averageXaccel = truncate(averageXaccel,2)
	averageYaccel = truncate(averageYaccel,2)
	averageZaccel = truncate(averageZaccel,2)
	'''if averageXaccel < 0.01:
		averageXaccel = 0
	if averageYaccel < 0.01:
		averageYaccel = 0
	if averageZaccel< -1000:
		averageZaccel = 0	'''
	
	averageAccelerations =  {'x':averageXaccel,'y':averageYaccel, 'z': averageZaccel}
	print("AVERAGE CHANGE")
	print(averageAccelerations)
	if averageXaccel < -0.8 or averageXaccel > 0.8:
		averageXaccel *= 1
	if averageYaccel < -1 or averageYaccel > 1:
		averageYaccel *= 10
	if averageZaccel < -0.2 or averageZaccel > 0.2:
		averageZaccel *= 1
	
	if averageXaccel > 0.8:
		averageXaccel = 0.8
	if averageXaccel < -0.8:
		averageXaccel = -0.8
	if (averageXaccel < 0.01 and averageXaccel > 0 ):
		averageXaccel = 0
	newCoordinates = {"x":newCoordinates["x"] + averageXaccel,"y":coordinates["y"] + averageYaccel, "z": newCoordinates["z"] + averageZaccel}
	print("MovingTO:")
	print(newCoordinates)
	if(newCoordinates['y'] < -1.5):
		newCoordinates['y'] = -1.5
		#os.popen(flashRed)
	if(newCoordinates['y'] > 1.5):
		#os.popen(flashRed)
		newCoordinates['y'] = 1.5
		
	if(newCoordinates['x'] < -6):
		newCoordinates['x'] = -6
		#os.popen(flashRed)
	if(newCoordinates['x'] > 25):
		os.popen(flashRed)
		newCoordinates['x'] = 25
	k = escapeSimulation.read()
	print(k)
	if k == 27 or k== 8 or k == 32 or k ==113:
		escapeSimulation.close()
		DISPLAY.destroy()
		break
	ship = pi3d.Sphere(x = newCoordinates['y']*2.5, y = 0, z = 10  + newCoordinates['x']/1.1 )
	#CORRECT x = newCoordinates['y']*2.5 z = 10  + newCoordinates['x']/1.1
	#ship = pi3d.Sphere(x = 0, y = 0,z = 10*newCoordinates['y']) working front back
	
	rotCounter += 10
	ship.rotateIncY(rotCounter)
	if rotCounter > 1000:
		rotCounter = 0
	#background.rotateIncZ(0.01)
	#background.draw(flatsh,[backgroundTexture])

	

#To do in C

firebase = firebase.FirebaseApplication('https://interstellar-d796a.firebaseio.com/', None)
pressureData = os.popen(pressure).read()
tempData = os.popen(temp).read()

respuesta = firebase.patch('/Ship/SensorData', {'Atmos Pressure (hPA)': pressureData, 'Temperature (C)': tempData})
print(respuesta)
print("\n")
salida = firebase.get('/Ship/SensorData','')
print("\n")
print(salida)


