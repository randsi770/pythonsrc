#!/usr/bin env python
# -*- coding: utf8 -*-
import time 
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)

os.system('modprobe snd_bcm2835')
os.system('amixer cset numid=3 1')
os.system('mplayer http://1live.akacast.akamaistream.net/7/706/119434/v1/gnl.akacast.akamaistream.net/1live &')

while True:
	if (GPIO.input(23)):
		print("1live")
		os.system('sudo killall mplayer')
		os.system('mplayer http://1live.akacast.akamaistream.net/7/706/119434/v1/gnl.akacast.akamaistream.net/1live &')
	if (GPIO.input(24)):
		print("NDR2")
		os.system('sudo killall mplayer')
		os.system('mplayer -playlist http://www.ndr.de/resources/metadaten/audio/m3u/ndr2.m3u &')
	time.sleep(0.1)
GPIO.cleanup()
