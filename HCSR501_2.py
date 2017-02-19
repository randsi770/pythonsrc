#!/usr/bin env python
# -*- coding: utf8 -*-
# Quelle:
# https://www.einplatinencomputer.com/raspberry-pi-pir-bewegungsmelder-ansteuern/
#
#Import
import RPi.GPIO as GPIO
import time
import datetime
import os
 
print "BEWEGUNGSMELDER"
print ""
 
#Board Mode: Angabe der Pin-Nummer
GPIO.setmode(GPIO.BOARD)
 
#GPIO Pin definieren fuer den Dateneingang vom Sensor
PIR_GPIO = 8
GPIO.setup(PIR_GPIO, GPIO.IN)
 
def MOTION(PIR_GPIO):
     os.system("echo  \"Bewegung erkannt\"")
 
print "%s - Warten auf Bewegung" % datetime.datetime.now()  
try:
     GPIO.add_event_detect(PIR_GPIO, GPIO.RISING, callback=MOTION)
     while 1:
          time.sleep(60)
except KeyboardInterrupt:
	GPIO.cleanup() 
