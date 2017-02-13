#!/usr/bin env python
# -*- coding: utf8 -*-
#
#Quelle https://www.raspberrypi.org/forums/viewtopic.php?t=45235
#It also checks free disk space and if under a set limit it starts to delete the oldest images to make sure there is always enough free space #for new images.
#
#While running on my rev1 B it consumes around 12% CPU / 4% ram and manages to capture a full size image once ever 2-3 secs.
#
#If you need to install PIL run "sudo aptitude install python-imaging-tk"

import StringIO
import subprocess
import os
import time
from datetime import datetime
from PIL import Image

# Motion detection settings:
# Threshold (how much a pixel has to change by to be marked as "changed")
# Sensitivity (how many changed pixels before capturing an image)
# ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)
threshold = 10
sensitivity = 20
forceCapture = True
forceCaptureTime = 60 * 60 # Once an hour
li = -1

# File settings
saveWidth = 1280
saveHeight = 960
diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk

# Capture a small test image (for motion detection)
def captureTestImage():
    command = "raspistill -w %s -h %s -t 1 -e bmp -o -" % (100, 75) 
    imageData = StringIO.StringIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer

# Save a full size image to disk
def saveImage(width, height, diskSpaceToReserve):
    keepDiskSpaceFree(diskSpaceToReserve)
    time = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
    subprocess.call("raspistill -w 1296 -h 972 -t 1 -e jpg -q 15 -o %s" % filename, shell=True)
    print "Captured %s" % filename

# Keep free space above given level
def keepDiskSpaceFree(bytesToReserve):
    if (getFreeSpace() < bytesToReserve):
        for filename in sorted(os.listdir(".")):
            if filename.startswith("capture") and filename.endswith(".jpg"):
                os.remove(filename)
                print "Deleted %s to avoid filling disk" % filename
                if (getFreeSpace() > bytesToReserve):
                    return

# Get available disk space
def getFreeSpace():
    st = os.statvfs(".")
    du = st.f_bavail * st.f_frsize
    return du
           
    # Get first image
    image1, buffer1 = captureTestImage()

    # Reset last capture time
    lastCapture = time.time()

while (True):

    # Get comparison image
    image2, buffer2 = captureTestImage()
    
    if li == -1:
		image1 = image2
		buffer1 = buffer2
		lastCapture = time.time()
		li = 0
        
    # Count changed pixels
    changedPixels = 0
    for x in xrange(0, 100):
        for y in xrange(0, 75):
            # Just check green channel as it's the highest quality channel
            pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
            if pixdiff > threshold:
                changedPixels += 1

    # Check force capture
    if forceCapture:
        if time.time() - lastCapture > forceCaptureTime:
            changedPixels = sensitivity + 1
                   
    # Save an image if pixels changed
    if changedPixels > sensitivity:
        lastCapture = time.time()
        saveImage(saveWidth, saveHeight, diskSpaceToReserve)
       
    # Swap comparison buffers
    image1 = image2
    buffer1 = buffer2
 
