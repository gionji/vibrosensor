#Sensor examples for everything builtin the board such as 
#Magnometer -> Magnetic pull on device
#Gyroscope - > xyz tilt degree on the device
#Accelerometer -> xyz directional force measurment

import time
import math
import numpy as np
import matplotlib.pyplot  as plt
from neo import Accel # import accelerometer
from time import sleep # to add delays

accel = Accel()

#accel.calibrate()

SAMPLES = 100
FREQ    = float(200)
SLEEP_TIME = 1/FREQ

print "Sleeping time:  " + str(SLEEP_TIME)


accelVals = [None] * SAMPLES

def updateAccelData():
	global accelVals
	startTime = 0
	endTime = 0

	startTime = int(round(time.time() * 1000))

	for i in range (0, SAMPLES):
		value = accel.get()
		mod = int(math.sqrt(value[0]*value[0] + value[1]*value[1] + value[2]*value[2]))
		accelVals[i] = mod
		sleep(SLEEP_TIME)
	
	#endTime = int(round(time.time() * 1000))
	#print str(len(accelVals)) + "   " + str(endTime - startTime)

	fft = np.fft.rfft(accelVals)
	
	endTime = int(round(time.time() * 1000))
	print str(len(accelVals)) + "   " + str(endTime - startTime)
	
	return abs(fft)


ffft = updateAccelData()

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlabel('samples')
plt.ylabel('module')
plt.title('About as simple as it gets, folks')
plt.ylim((0,20000))
line1, = ax.plot(ffft[1:])

while 1:
	ffft = updateAccelData()
	line1.set_ydata(ffft[1:])
	fig.canvas.draw()
	
plt.show()
