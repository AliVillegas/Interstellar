
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
coordinates =  {"x":0.0,"y":1.0, "z": 0.0}
print("Original Position:")
print(coordinates)
averageXaccel = 0.0
averageYaccel = 0.0
averageZaccel = 0.0
spanAcceleration = 50#30 yielded good results
earthGAccel = -0.96
shader = pi3d.Shader('uv_light')
flatsh = pi3d.Shader("uv_flat")
spaceShipTexture = pi3d.Texture('spaceshipTexture.jpg')
for x in range(0,spanAcceleration):
	
	raw = sense.get_gyroscope_raw()
	averageXaccel += round(raw["x"],3)
	averageYaccel += round(raw["y"],3)
	averageZaccel += round(raw["z"],3) + earthGAccel
	#print("x: {x}, y: {y}, z: {z}".format(**raw))

	averageXaccel = averageXaccel / spanAcceleration
	averageYaccel = averageYaccel / spanAcceleration
	averageZaccel = averageZaccel / spanAcceleration
	averageXaccel = truncate(averageXaccel,2)
	averageYaccel = truncate(averageXaccel,2)
	averageZaccel = truncate(averageXaccel,2)
	'''if averageXaccel < 0.01:
		averageXaccel = 0
	if averageYaccel < 0.01:
		averageYaccel = 0
	if averageZaccel< -1000:
		averageZaccel = 0	'''

	averageAccelerations =  {'x':averageXaccel,'y':averageYaccel, 'z': averageZaccel}
	print("AVERAGE CHANGE")
	print(averageAccelerations)
	if averageXaccel < -0.2 or averageXaccel > 0.2:
		averageXaccel *= 10
	if averageYaccel < -1 or averageYaccel > 1:
		averageYaccel *= 10
	if averageZaccel < -0.2 or averageZaccel > 0.2:
		averageZaccel *= 1
	newCoordinates = {"x":coordinates["x"] + averageXaccel,"y":coordinates["y"] + averageYaccel, "z": coordinates["z"] + averageZaccel}
	print("MovingTO:")
	print(newCoordinates)
	if(newCoordinates['y'] < 0.3):
		newCoordinates['y'] = 0.3
		os.popen(flashRed)
	if(newCoordinates['y'] > 50):
		os.popen(flashRed)
		newCoordinates['y'] = 50


