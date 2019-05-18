import time
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
class MissionData:
   firebase = firebase.FirebaseApplication('https://interstellar-d796a.firebaseio.com/', None) 
   pathLocation = 'Simulation'
   pathLocationSensors = ''
   pathLocationAccel = ''
   pathLocationReport = ''
   averageXaccel = 0
   averageYaccel = 0
   averageZaccel = 0
   leftWing = ''
   rightWing = ''
   cabin = ''
   lifes = 0
   
   def __init__(self, simulationCounter, timeStampId, avgAccelx, avgAccely, avgAccelz, lifes, cabinStatus, leftWingStatus, rightWingStatus):
      self.pathLocation = self.pathLocation + str(simulationCounter) + '/Ship Time Logs/' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(timeStampId)))
      self.pathLocationSensors = self.pathLocation + '/Sensors'
      self.pathLocationAccel = self.pathLocation + '/Sensors/Acceleration'
      self.pathLocationReport = self.pathLocation + '/Mission Report'
      self.averageXaccel = avgAccelx
      self.averageYaccel = avgAccely
      self.averageZaccel = avgAccelz
      self.rightWing = rightWingStatus
      self.leftWing = leftWingStatus
      self.cabin = cabinStatus
      self.lifes = lifes
   
   def uploadDataToFirebase(self): 
     timeStamps = './TimeStamps'
     pressure = './ReadPressure'
     sensorDataText = "./PrintSensorData"
     temp = './ReadTemperature'
     log = self.firebase.patch(self.pathLocationSensors, {'Atmos Pressure (hPA)': os.popen(pressure).read(), 'Temperature (C)': os.popen(temp).read()})
     log = self.firebase.patch(self.pathLocationAccel, {'x': self.averageXaccel, 'y': self.averageYaccel, 'z': self.averageZaccel})
     log = self.firebase.patch(self.pathLocationReport, {'Lifes': self.lifes, 'Cabin Status': self.cabin, 'Right Wing Status': self.rightWing, 'Left Wing Status': self.leftWing})
     
