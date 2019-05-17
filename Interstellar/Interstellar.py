
'''
- Firebase each 10seconds Timestamps (Record Crashes)
- Animate going sideways and up and down 
- 8 C programs to show life going down in the leds
- 4 C programs to flash Screen red where you hit the border
'''
from firebase import firebase
import random
import os
from subprocess import call
from sense_hat import SenseHat 
import time
import math
import random
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
spanAcceleration = 1	#30 yielded good results
earthGAccel = -0.96
averageZgyr = 0.0
#x=80,y=100,w= 1000, h = 1000, background=(0,0,0,1),use_pygame=True,frames_per_second = 30
DISPLAY = pi3d.Display.create(x=80,y=100,w= 1000, h = 1300, background=(0,0,0,1),use_pygame=True,frames_per_second = 30)
shader = pi3d.Shader('uv_light')
pi3d.Light(lightpos=(1, -1, -3), lightcol =(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))
pi3d.opengles.glDisable(pi3d.GL_CULL_FACE)

flatsh = pi3d.Shader("uv_flat")
spaceShipTexture = pi3d.Texture('spaceshipTexture.jpg')
asteroidSmall = pi3d.Texture('asteroidSmall.jpg')
asteroidBig = pi3d.Texture('asteroidBig2.jpg')
asteroidMed = pi3d.Texture('asteroidM.jpg')
backgroundTexture = pi3d.Texture('background.png')

ship = pi3d.Sphere(z=20.0)
asteroid = pi3d.Sphere(radius= 50, z = 520)
spaceRocket = pi3d.Model(file_string='ship.obj', name='xWing', z=500.0)

#spaceRocket.set_shader(flatsh)
background = pi3d.Plane(w=1920, h=1080, name="stars", z=800)
escapeSimulation = pi3d.Keyboard()
newCoordinates = {'x':1, 'y':1, 'z':1}

flashGreen = "./FlashGreen"
flashRed = "./FlashRed"
pressure = './ReadPressure'
sensorDataText = "./PrintSensorData"
temp = './ReadTemperature'
CAMERA = pi3d.Camera.instance()
CAMERA = pi3d.Camera.instance()
####################
#this block added for fast text changing
import time
CAMERA2D = pi3d.Camera(is_3d=False)

myfont = pi3d.Font('FreeSans.ttf', codepoints='0123456789. FPStm:')
myfont2 = pi3d.Font('FreeSans.ttf', codepoints='abcdefghijkmnlopkrstuvwxyzABCDEFGHIJKMNLOPQRSTUVWXYZ: ,.1234567890 ')
myfont.blend = True
tstring = "{:.0f}FPS tm:{:.1f} "
lasttm = time.time()
tdel = 0.23
fcount = 0
'''
mystring = pi3d.String(camera=CAMERA2D, font=myfont, is_3d=False, string=tstring)
mystring.set_shader(flatsh)
(lt, bm, ft, rt, tp, bk) = mystring.get_bounds()
xpos = (-DISPLAY.width + rt - lt) / 2.0
ypos = (-DISPLAY.height + tp - bm) / 2.0
mystring.position(xpos + 100, ypos + 200, 1.0)
mystring.draw() 
'''
pText = pi3d.String(camera=CAMERA2D, font=myfont2, is_3d=False, string='Pressure: 00.000 hPA,Temp: 00.00 C Life:5000')
pText.set_shader(flatsh)
(lt, bm, ft, rt, tp, bk) = pText.get_bounds()
xpos = (-DISPLAY.width + rt - lt) / 2.0
ypos = (-DISPLAY.height + tp - bm) / 2.0
pText.position(xpos + 10, ypos + 10, 1.0)
pText.draw()
# NB has to be drawn before quick_change() is called as buffer needs to exist
####################
'''
CAMERA2D = pi3d.Camera(is_3d=False)
myfont = pi3d.Font('FreeSans.ttf', codepoints='0123456789. FPStm:')
myfont.blend = True
tstring = "{:.0f}FPS tm:{:.1f} ".format(60,time.time())
lasttm = time.time()
tdel = 0.23
fcount = 0
mystring = pi3d.String(camera=CAMERA2D, font=myfont, is_3d=False, string=tstring)
xpos = -0.5
ypos = 0                     
mystring.position(xpos, ypos, 1.0)
mystring.draw()
'''
#os.popen(flashRed)
rotCounter = 0
lifeHits = 8
asteroid1Radius = 5
asteroidBigR = 3
asteroid3R = 10
asteroid3Z = 520
asteroidBigZ = 540
asteroid1Z = 520
randomXSpawn = random.randint(-180,-50)
randomYSpawn = randomYSpawn = random.randint(-30,15)
randomXSpawnBig = random.randint(-180,-50)
randomYSpawnBig = randomYSpawn = random.randint(-30,15)
randomXSpawn3 = random.randint(-180,-50)
randomYSpawn3 = randomYSpawn = random.randint(-30,15)
rotationAsteroidConter = 0
rotateStarsCounter = 0
while DISPLAY.loop_running():
	background.draw(shader,[backgroundTexture])
	rotateStarsCounter += 1
	if rotateStarsCounter == 3:
		background.rotateIncZ(random.randint(-300,300))
		rotateStarsCounter = 0
	if lifeHits == 0:
		break
	rotationAsteroidConter += 10
	if rotationAsteroidConter > 360:
		rotationAsteroidConter = 0
	#mystring.draw()
	rndAsteroid = pi3d.Sphere(x = randomXSpawn, y = randomYSpawn, radius= asteroid1Radius, z = asteroid1Z, ry = rotationAsteroidConter)
	rndAsteroid2 = pi3d.Sphere(x = randomXSpawnBig, y = randomYSpawn, radius= asteroidBigR, z = asteroidBigZ,ry = rotationAsteroidConter)
	rndAsteroid3 = pi3d.Sphere(x = randomXSpawn3, y = randomYSpawn3, radius= asteroid3R, z = asteroid3Z,ry = rotationAsteroidConter)
	
	rndAsteroid3.draw(flatsh,[asteroidMed])
	rndAsteroid.draw(flatsh,[asteroidBig])
	rndAsteroid2.draw(flatsh,[asteroidSmall])
	spaceRocket.draw()
	#pressure.draw()<
	#ship.draw(shader,[spaceShipTexture])
	averageXaccel = 0.0
	averageYaccel = 0.0
	averageZaccel = 0.0
	if asteroid1Z > 30:
		if asteroid1Z < 50:
			asteroid1Radius = 20
		#asteroid1Radius += asteroid1Z/1000
		asteroid1Z -= 20
	else:
		asteroid1Z = 520
		asteroid1Radius = 15
		randomXSpawn = random.randint(-180,-50)
		randomYSpawn = random.randint(-30,15)
		
	if asteroid3Z > 30:
		if asteroid3Z < 50:
			asteroid3R = 12
		#asteroid1Radius += asteroid1Z/1000
		asteroid3Z -= 69
	else:
		asteroid3Z = 520
		asteroid3R = 8
		randomXSpawn3 = random.randint(50,180)
		randomYSpawn3 = random.randint(-30,15)
		
	if asteroidBigZ > 30:
		if asteroidBigZ < 50:
			asteroidBigR = 10
		#asteroid1Radius += asteroid1Z/1000
		asteroidBigZ -= 50
	else:
		asteroidBigZ = 520
		asteroidBigR = 5
		randomXSpawnBig = random.randint(-130,-50)
		randomYSpawnBig = random.randint(-30,15)
	'''
	if asteroid1Z > 30:
		if asteroid1Z < 50:
			asteroid1Radius = 2
		#asteroid1Radius += asteroid1Z/1000
		asteroid1Z -= 10
	else:
		asteroid1Radius = 0.001
			'''
	
	for x in range(0,spanAcceleration):	
		tm = time.time()
		fcount += 1
		if tm > (lasttm + tdel):
			#newtstring = "{:.0f}FPS tm:{:.1f}".format(fcount / (tm - lasttm), tm)
			if x == 0:
				sensorsText = os.popen(sensorDataText).read() + " Life:" + str(lifeHits)
				pText.quick_change(sensorsText)
			lasttm = tm
			fcount = 0	
		#mystring.draw()
		pText.draw()
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
	if (averageXaccel < 0.2 and averageXaccel > 0 ):
		averageXaccel = 0
		

	if (averageYaccel < 0.2 and averageYaccel > 0 ):
		averageYaccel = 0
		
	newCoordinates = {"x":newCoordinates["x"] + averageXaccel,"y":newCoordinates["y"] + averageYaccel, "z": newCoordinates["z"] + averageZaccel}
	print("MovingTO:")
	print(newCoordinates)
	
	if(newCoordinates['y'] < -2.3): #bound izquierda
		newCoordinates['y'] = -2.3
		os.popen(flashRed)
		lifeHits -=1
	if(newCoordinates['y'] > 2.3): #bound derecha
		os.popen(flashRed)
		newCoordinates['y'] = 2.3
		lifeHits -=1
		
	if(newCoordinates['x'] < -1.3): #bound de arriba
		newCoordinates['x'] = -1.3
		os.popen(flashRed)
		lifeHits -=1
		
	if(newCoordinates['x'] > 12): #bound de abajo
		os.popen(flashRed)
		newCoordinates['x'] = 12
		lifeHits -=1
	if averageYaccel > 1:
		spaceRocket.rotateIncZ(1*averageYaccel*15)
	elif averageYaccel < 1:
		spaceRocket.rotateIncZ(-1*averageYaccel*15)
		
	if averageXaccel > 1:
		spaceRocket.rotateIncX(-1*averageXaccel*3)
	elif averageXaccel < 1:
		spaceRocket.rotateIncX(averageXaccel*3)
	#ship = pi3d.Sphere(x = newCoordinates['y']*3, y = -1*newCoordinates['x']/1.1, z = 10 )
	#ship = pi3d.Sphere(x = newCoordinates['y']*3, y = -1*newCoordinates['x']/1.1, z = 10 )
	#spaceRocket = pi3d.Model(file_string='ship.obj', name='xWing', x = newCoordinates['y']*100, y = -1*newCoordinates['x']*30,  z=500.0)
	spaceRocket.position(x = newCoordinates['y']*60, y = -1*newCoordinates['x']*15,  z=500.0)
	#CORRECT x = newCoordinates['y']*2.5 z = 10  + newCoordinates['x']/1.1
	#ship = pi3d.Sphere(x = 0, y = 0,z = 10*newCoordinates['y']) working front back
	'''
	rotCounter += 10
	ship.rotateIncY(rotCounter)
	if rotCounter > 1000:
		rotCounter = 0'''
	#background.rotateIncZ(0.01)
	#background.draw(flatsh,[backgroundTexture])

	

#To do in C

firebase = firebase.FirebaseApplication('https://interstellar-d796a.firebaseio.com/', None)
pressureData = os.popen(pressure).read()
tempData = os.popen(temp).read()

#respuesta = firebase.patch('/Ship/SensorData', {'Atmos Pressure (hPA)': pressureData, 'Temperature (C)': tempData})
#print(respuesta)
print("\n")
#salida = firebase.get('/Ship/SensorData','')
#rint("\n")
print(pressureData)


