


import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

pinSensors = [27,22,5,24,25]

controlPins = [ [2,3,4,17],
                [10,9,11,0],
                [6,13,19,26],
                [14,15,18,23],
                [12,16,20,21] ]

isSensorHit = [False, False, False, False, False]
isCalibrated = [False, False, False, False, False]
isDrumActive = [False, False, False, False, False]

numberOfDrums = len(controlPins)

for drum in range(numberOfDrums):
    for pin in range(4):
        GPIO.setup(controlPins[drum][pin],GPIO.OUT)
        GPIO.output(controlPins[drum][pin],0)


for pin in range(len(pinSensors)):
    GPIO.setup(pinSensors[pin],GPIO.IN)

seq = [ [1,0,0,1],
        [1,1,0,0],
        [0,1,1,0],
        [0,0,1,1] ]

drumPositions = [0,0,0,0,0]
drumTargetPositions = [0,0,0,0,0]

simpleCounter = 0
mode = "CRONO"
fullTurn = 2042;
stepsPerFlap = fullTurn / 20

flapsCrono = [0,1,2,3,4,5,6,7,8,11]

def readSensors():
    global pinSensors
    global isSensorHit
    global isCalibrated

    for drum in range(numberOfDrums):

        if GPIO.input(pinSensors[drum]):
            isSensorHit[drum] = True
        else:
            if isSensorHit[drum]:

                drumPositions[drum] = 0 # self calibrate position

                if not isCalibrated[drum]:
                    isCalibrated[drum] = True
                isSensorHit[drum] = False


###########################################
def moveDrums():
#    global pinSensors
#    global drumTargetPositions
#    global isCalibrated
#    global isDrumActive
#    global numberOfDrums
#    global drumPositions
#    global fullTurn
#    global controlPins

    for step in range(4):
        for pin in range(4):
            for drum in range(numberOfDrums):
                if (isDrumActive[drum]):

                    if step == 0:
                        drumPositions[drum] += 1

                        if drumPositions[drum] >= fullTurn:
                            drumPositions[drum] -= fullTurn
                            drumTargetPositions[drum] -= fullTurn
#                if (drum == 0):
#		    print("patching excess: ", drumPositions[drum], drumTargetPositions[drum])

                    GPIO.output(controlPins[drum][pin], seq[step][pin])

                else:
                    GPIO.output(controlPins[drum][pin], GPIO.LOW)

        time.sleep(0.002)

###########################################
try:
    start_time = time.time()

    while True:

        if mode == "CRONO":
            current_time = time.time()

            tick = int(current_time - start_time)
	    if tick > 9:
		tick = 0
		start_time = current_time

            if tick != simpleCounter:
                print(tick, drumPositions[0], drumTargetPositions[0])

            simpleCounter = tick




        for drum in range(numberOfDrums):

            if not isCalibrated[drum]:    #if not calibrated yet, move drum until it is
                isDrumActive[drum] = True

            else:                         # if this drum is already calibrated, behave normally

		newPos = flapsCrono[simpleCounter] * stepsPerFlap

		if newPos < drumTargetPositions[drum]:
		    newPos += fullTurn
#		    drumPositions[drum] = drumPositions[drum] - fullTurn
#                    print("position reset to (2): ", drumPositions[drum])

                drumTargetPositions[drum] = newPos

                if drumTargetPositions[drum] > drumPositions[drum]:
		    if drum == 0:
                        isDrumActive[drum] = True

                else:
                    isDrumActive[drum] = False

	readSensors()
        moveDrums()

except KeyboardInterrupt:
    print("Interrupted by keyboard")

except:
    print("EXCEPTION!")

finally:
    #GPIO.cleanup()
    for drum in range(numberOfDrums):
        for pin in range(4):
            GPIO.output(controlPins[drum][pin], GPIO.LOW)
            exit(0)



exit(0)

