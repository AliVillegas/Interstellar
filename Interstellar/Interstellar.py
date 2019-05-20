
'''
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
import pygame
from os import walk
import pi3d
import MissionData

#MissionData.MissionData(0,0,0,0,0, 0, '','', '')
def truncate(number, digits):
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper
#To do in C
sense = SenseHat()
sense.set_imu_config(True, True, True)
coordinates =  {"x":0.0,"y":0.0, "z": 0.0}
print("Original Position:")
print(coordinates)
averageXaccel = 0.0
averageYaccel = 0.0
averageZaccel = 0.0
spanAcceleration = 1	#30 yielded good results
earthGAccel = -0.96
averageZgyr = 0.0
pi3d.opengles.glDisable(pi3d.GL_CULL_FACE)
#x=80,y=100,w= 1000, h = 1000, background=(0,0,0,1),use_pygame=True,frames_per_second = 30
#DISPLAY = pi3d.Display.create()
DISPLAY = pi3d.Display.create(x=80,y=100,w= 1000, h = 1300, background=(0,0,0,1),use_pygame=True,frames_per_second = 30)
LOGGER = pi3d.Log(level='INFO', file='pi3d.log')
shader = pi3d.Shader('uv_light')
pi3d.Light(lightpos=(1, -1, -3), lightcol =(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))


flatsh = pi3d.Shader("uv_flat")
asteroidShader = pi3d.Shader("uv_light")
spaceShipTexture = pi3d.Texture('spaceshipTexture.jpg')
asteroidSmall = pi3d.Texture('asteroidSmall.jpg')
asteroidBig = pi3d.Texture('asteroidBig.jpg')
asteroidMed = pi3d.Texture('asteroidM.jpg')
backgroundTexture = pi3d.Texture('background.png')
dangerZoneTexture = pi3d.Texture('dangerZone.jpg')
safeZoneTexture = pi3d.Texture('safeZone.jpg')
ship = pi3d.Sphere(z=20.0)
asteroid = pi3d.Sphere(radius= 50, z = 520)
spaceRocket = pi3d.Model(file_string='ship.obj', name='rocket', z=500.0)

#spaceRocket.set_shader(flatsh)
background = pi3d.Plane(w=1920, h=1080, name="stars", z=800)
escapeSimulation = pi3d.Keyboard()
newCoordinates = {'x':4, 'y':0, 'z':1}

flashGreen = "./FlashGreen"
flashRed = "./FlashRed"
pressure = './ReadPressure'
sensorDataText = "./PrintSensorData"
temp = './ReadTemperature'
humidity = './PrintHumidityData'
timeStamps = './TimeStamps'
readOrientation = './ReadOrientation'
health8 = './Health8'
health7 = './Health7'
health6 = './Health6'
health5 = './Health5'
health4 = './Health4'
health3 = './Health3'
health2 = './Health2'
health1 = './Health1'
health0 = './Health0'
CAMERA = pi3d.Camera.instance()
CAMERA = pi3d.Camera.instance()
####################
#this block added for fast text changing
import time
CAMERA2D = pi3d.Camera(is_3d=False)

myfont = pi3d.Font('FreeSans.ttf', codepoints='0123456789. FPStm:')
myfont2 = pi3d.Font('FreeSans.ttf', codepoints='abcdefghijkmnlopkrstuvwxyzABCDEFGHIJKMNLOPQRSTUVWXYZ: ,.1234567890 ')
myfont.blend = True
myfont2.blend = True
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
humidityText = pi3d.String(camera=CAMERA2D, font=myfont2, is_3d=False, string='Humidity: 21.50 percent rHn')
gameOverText = pi3d.String(camera=CAMERA2D, font=myfont2, is_3d=False, string='Thanks for using this simulation')
calibrationText = pi3d.String(camera=CAMERA2D, font=myfont2, is_3d=False, string='Rotate The Raspberry pi until the leds flash blue')
firebaseText = pi3d.String(camera=CAMERA2D, font=myfont2, is_3d=False, string='Waiting for instructions from firebase HQ')
pText.set_shader(flatsh)
humidityText.set_shader(flatsh)
firebaseText.set_shader(flatsh)
gameOverText.set_shader(flatsh)
calibrationText.set_shader(flatsh)
(lt, bm, ft, rt, tp, bk) = pText.get_bounds()
xpos = (-DISPLAY.width + rt - lt) / 2.0
ypos = (-DISPLAY.height + tp - bm) / 2.0
#pText.position(xpos, ypos + 850, 1.0)
#gameOverText.position(xpos+100,ypos+300,1)
#humidityText.position(xpos-173,ypos+900,1)
pText.position(xpos, ypos, 1.0)
gameOverText.position(xpos+100,ypos+300,1)
humidityText.position(xpos-173,ypos+35,1)
calibrationText.position(xpos+100,ypos+300,1)
firebaseText.position(xpos+100,ypos+300,1)
pText.draw()
humidityText.draw()
gameOverText.draw()
firebaseText.draw()
calibrationText.draw()
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

simulationCounter = 0


f = open("simulation.txt","r")
if f.mode == 'r':
	contents = f.read()
	n = int(contents)
	simulationCounter = n
	f.close()
	
f = open("simulation.txt","w+")
simulationCounter += 1
f.write(str(simulationCounter))
f.close()

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

#DANGER AND SAFE ZONES
danger = pi3d.Plane(w=2000, h=60, name="danger", z=505)
safe  = pi3d.Plane(w=50, h=50, name="safe", z=5)
timeStampId = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(os.popen(timeStamps).read())))

fireBaseLogCounter = 0

firebase = firebase.FirebaseApplication('https://interstellar-d796a.firebaseio.com/', None)
pressureData = os.popen(pressure).read()
tempData = os.popen(temp).read()

#respuesta = firebase.patch('/Ship/SensorData', {'Atmos Pressure (hPA)': pressureData, 'Temperature (C)': tempData})
#print(respuesta)
print("\n")
#salida = firebase.get('/Ship/SensorData','')
#rint("\n")
print(pressureData)

leftWingStatusCounter = 0
rightWingStatusCounter = 0
cabinStatusCounter = 0
leftWingStatus= 'Fine...'
rightWingStatus = 'Fine...'
cabinStatus = 'Fine...'
os.popen(health8)

firebaseMissionReportLogs = []

#Calibration stage with c
gyroCounter = 0
successCalibrationCounter = 0
while DISPLAY.loop_running():
	background.draw(shader,[backgroundTexture])
	calibrationText.draw()
	gyroCounter += 1
	if gyroCounter >0:
		print(sense.orientation['yaw'])
		print(sense.orientation['roll'])
		print(sense.orientation['pitch'])
		yaw1 = (sense.orientation['yaw'] > 0 and sense.orientation['yaw'] < 15) 
		yaw2 = sense.orientation['yaw'] > 150 and sense.orientation['yaw'] < 361
		yaw = yaw1 or yaw2
		roll1 = (sense.orientation['roll'] > 0 and sense.orientation['roll'] < 15) 
		roll2 = sense.orientation['roll'] > 350 and sense.orientation['roll'] < 361
		roll = roll1 or roll2
		pitch1 = (sense.orientation['pitch'] > 0 and sense.orientation['pitch'] < 15) 
		pitch2 = sense.orientation['pitch'] > 350 and sense.orientation['pitch'] < 361
		pitch = pitch1 or pitch2

		if yaw and pitch and roll:
			successCalibrationCounter += 1
			os.popen(flashGreen)
			if successCalibrationCounter >3:
				break
		else:
			successCalibrationCounter = 0
			os.popen(flashRed)
		gyroCounter = 0
	k = escapeSimulation.read()
	print(k)
	if k == 27 or k== 8 or k == 32 or k ==113:
		escapeSimulation.close()
		os.popen(flashGreen)
		break
	
firstTimeRun = True
while DISPLAY.loop_running():
	if firstTimeRun:
		os.popen(health8)
		firstTimeRun = False
	if lifeHits != 0:
		
		background.draw(shader,[backgroundTexture])
		#anger.draw(shader,[dangerZoneTexture])
		rotateStarsCounter += 1
		if rotateStarsCounter == 3:
			background.rotateIncZ(random.randint(-300,300))
			rotateStarsCounter = 0
		rotationAsteroidConter += 10
		if rotationAsteroidConter > 360:
			rotationAsteroidConter = 0
		#mystring.draw()
		rndAsteroid = pi3d.Sphere(x = randomXSpawn, y = randomYSpawn, radius= asteroid1Radius, z = asteroid1Z, ry = rotationAsteroidConter)
		rndAsteroid2 = pi3d.Sphere(x = randomXSpawnBig, y = randomYSpawn, radius= asteroidBigR, z = asteroidBigZ,ry = rotationAsteroidConter)
		rndAsteroid3 = pi3d.Sphere(x = randomXSpawn3, y = randomYSpawn3, radius= asteroid3R, z = asteroid3Z,ry = rotationAsteroidConter)
		
		rndAsteroid3.draw(asteroidShader,[asteroidSmall])
		rndAsteroid.draw(shader,[asteroidBig])
		rndAsteroid2.draw(shader,[asteroidSmall])
		spaceRocket.draw(shader)
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
					humidityText.quick_change(os.popen(humidity).read())
				lasttm = tm
				fcount = 0	
			#mystring.draw()
			pText.draw()
			humidityText.draw()
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
			leftWingStatusCounter += 3
			os.popen(flashRed)
			lifeHits -=1
			if lifeHits == 8:
				os.popen(health8)
			elif lifeHits ==7:
				os.popen(health7)
			elif lifeHits ==6:
				os.popen(health6)
			elif lifeHits ==5:
				os.popen(health5)
			elif lifeHits == 4:
				os.popen(health4)
			elif lifeHits ==3:
				os.popen(health3)
			elif lifeHits ==2:
				os.popen(health2)
			elif lifeHits ==1:
				os.popen(health1)
			elif lifeHits == 0:
				os.popen(health0)
			
			
		if(newCoordinates['y'] > 2.3): #bound derecha
			rightWingStatusCounter += 3
			os.popen(flashRed)
			newCoordinates['y'] = 2.3
			lifeHits -=1
			if lifeHits == 8:
				os.popen(health8)
			elif lifeHits ==7:
				os.popen(health7)
			elif lifeHits ==6:
				os.popen(health6)
			elif lifeHits ==5:
				os.popen(health5)
			elif lifeHits == 4:
				os.popen(health4)
			elif lifeHits ==3:
				os.popen(health3)
			elif lifeHits ==2:
				os.popen(health2)
			elif lifeHits ==1:
				os.popen(health1)
			elif lifeHits == 0:
				os.popen(health0)
			
		if(newCoordinates['x'] < -1.3): #bound de arriba
			newCoordinates['x'] = -1.3
			cabinStatusCounter += 2
			
			os.popen(flashRed)
			lifeHits -=1
			if lifeHits == 8:
				os.popen(health8)
			elif lifeHits ==7:
				os.popen(health7)
			elif lifeHits ==6:
				os.popen(health6)
			elif lifeHits ==5:
				os.popen(health5)
			elif lifeHits == 4:
				os.popen(health4)
			elif lifeHits ==3:
				os.popen(health3)
			elif lifeHits ==2:
				os.popen(health2)
			elif lifeHits ==1:
				os.popen(health1)
			elif lifeHits == 0:
				os.popen(health0)
		
		if leftWingStatusCounter < 2 and leftWingStatusCounter >1:
				leftWingStatus = "ok..."
		elif leftWingStatusCounter < 6 and leftWingStatusCounter >2:
				leftWingStatus = "Damaged"
		elif leftWingStatusCounter > 6:
				leftWingStatus = "Destroyed"
				
		if cabinStatusCounter < 2 and cabinStatusCounter >1:
				cabinStatus = "ok.."
		elif cabinStatusCounter < 6  and cabinStatusCounter >2:
				cabinStatus = "Damaged"
		elif cabinStatusCounter > 6:
				cabinStatus = "Destroyed"
				
		if rightWingStatusCounter < 2 and cabinStatusCounter >1:
				rightWingStatus = "ok..."
		elif rightWingStatusCounter < 6 and cabinStatusCounter >2:
				rightWingStatus = "Severily Damaged"
		elif rightWingStatusCounter > 6:
				rightWingStatus = "Destroyed"
				
		if(newCoordinates['x'] > 12): #bound de abajo
			os.popen(flashRed)
			newCoordinates['x'] = 12
			cabinStatusCounter += 3
			lifeHits -=1
			if lifeHits == 8:
				os.popen(health8)
			elif lifeHits ==7:
				os.popen(health7)
			elif lifeHits ==6:
				os.popen(health6)
			elif lifeHits ==5:
				os.popen(health5)
			elif lifeHits == 4:
				os.popen(health4)
			elif lifeHits ==3:
				os.popen(health3)
			elif lifeHits ==2:
				os.popen(health2)
			elif lifeHits ==1:
				os.popen(health1)
			elif lifeHits == 0:
				os.popen(health0)
		if averageYaccel > 1:
			spaceRocket.rotateIncZ(1*averageYaccel*20)
		elif averageYaccel < 1:
			spaceRocket.rotateIncZ(-1*averageYaccel*20)
			
		if averageXaccel > 1:
			spaceRocket.rotateIncX(-1*averageXaccel*6)
		elif averageXaccel < 1:
			spaceRocket.rotateIncX(averageXaccel*6)
		
		
		#Managing FIREBASE Logs
		'''
		try:
			pid = os.fork()
		except OSError:
			exit("Could not create a child process")
		if pid == 0:
		''' #self, simulationCounter, timeStampId, avgAccelX, avgAccelY, avgAccelZ, lifes, cabinStatus, leftWingStatus, rightWingStatus
		fireBaseLogCounter += 1
		if fireBaseLogCounter >20:
			firebaseText.draw()
		if fireBaseLogCounter == 40:
			firebaseMissionReportLogs.append(MissionData.MissionData(simulationCounter,os.popen(timeStamps).read(),averageXaccel,averageYaccel,averageZaccel, lifeHits, cabinStatus,leftWingStatus, rightWingStatus))
			fireBaseLogCounter = 0	
		
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
	else:
		gameOverText.draw()
		background.draw(shader,[backgroundTexture])
		#anger.draw(shader,[dangerZoneTexture])
		rotateStarsCounter += 1
		if rotateStarsCounter == 3:
			background.rotateIncZ(random.randint(-300,300))
			rotateStarsCounter = 0
		rotationAsteroidConter += 10
		if rotationAsteroidConter > 360:
			rotationAsteroidConter = 0
		#mystring.draw()
		rndAsteroid = pi3d.Sphere(x = randomXSpawn, y = randomYSpawn, radius= asteroid1Radius, z = asteroid1Z, ry = rotationAsteroidConter)
		rndAsteroid2 = pi3d.Sphere(x = randomXSpawnBig, y = randomYSpawn, radius= asteroidBigR, z = asteroidBigZ,ry = rotationAsteroidConter)
		rndAsteroid3 = pi3d.Sphere(x = randomXSpawn3, y = randomYSpawn3, radius= asteroid3R, z = asteroid3Z,ry = rotationAsteroidConter)
		
		rndAsteroid3.draw(asteroidShader,[asteroidSmall])
		rndAsteroid.draw(shader,[asteroidBig])
		rndAsteroid2.draw(shader,[asteroidSmall])
		spaceRocket.draw(shader)
	k = escapeSimulation.read()
	print(k)
	if k == 27 or k== 8 or k == 32 or k ==113:
		escapeSimulation.close()
		DISPLAY.destroy()
		print("UPLOADING SIMULATION REPORT TO FIREBASE PLEASE WAIT...")
		for mission in firebaseMissionReportLogs:
			mission.uploadDataToFirebase()
		os.popen(flashGreen)
		break
	

#To do in C


