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

SAMPLES = 128
FREQ    = float(1000)
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
		#mod = int(math.sqrt(value[0]*value[0] + value[1]*value[1] + value[2]*value[2]))
		mod = int(value[2])
		accelVals[i] = abs(mod)
		sleep(SLEEP_TIME)
	
	endTime = int(round(time.time() * 1000))
	avgDelay = float(endTime - startTime) / float(len(accelVals))
	avgFreq = (1 / avgDelay ) * 1000
	
	print str(avgDelay) + " ms  -  " + str(avgFreq) + " Hz"
	
	return accelVals


data = updateAccelData()
ffft = abs(np.fft.rfft(data))

plt.ion()

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

plt.xlabel('samples')
plt.ylabel('module')
plt.title('About as simple as it gets, folks')
ax1.set_ylim([8000,25000])
ax2.set_ylim([0,50000])
#x2.set_yscale('log')
line1, = ax1.plot(data[1:])
line2, = ax2.plot(ffft[1:])

while 1:
	data = updateAccelData()
	ffft = abs(np.fft.rfft(data))
	line1.set_ydata(data[1:])
	line2.set_ydata(ffft[1:])
	fig.canvas.draw()
	
plt.show()
