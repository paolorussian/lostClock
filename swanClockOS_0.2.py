import RPi.GPIO as GPIO
import time
import datetime
import sys
import traceback

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

pinSensors = [27,22,5,24,8]

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
drumOffsets = [0,20,0,0,0]

simpleCounter = 0
#mode = "CLOCK"
mode = "LOST"
timerLostMinutes = 109
timerLostSeconds = 00
fullTurn = 2042;
stepsPerFlap = fullTurn / 20

flapsCrono = [0,1,2,3,4,5,6,7,8,11]
flapsTimer = [0,19,18,17,16,15,14,13,12,11]
flapsHieroglyphPosition = 1024
flapsEmptyPosition = 922

def readSensors():
    #global pinSensors
    #global isSensorHit
    #global isCalibrated

    for drum in range(numberOfDrums):

        if GPIO.input(pinSensors[drum]):
            isSensorHit[drum] = True
        else:
            if isSensorHit[drum]:

#                drumPositions[drum] = 0 # self calibrate position
                drumPositions[drum] = drumOffsets[drum]

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

                    GPIO.output(controlPins[drum][pin], seq[step][pin])
                else:
                    GPIO.output(controlPins[drum][pin], GPIO.LOW)

        time.sleep(0.002)

###########################################
try:
    start_time = time.time()
    current_time = start_time

#    x = datetime.datetime.now()
#    hour = '{:02d}'.format(x.hour)
#    hourArr = list(map(int, str(x.hour).zfill(2)))
#    print(hourArr[0], hourArr[1])


    while True:

        current_time = time.time()

        if mode == "CRONO":
#            current_time = time.time()
            tick = int(current_time - start_time)
            simpleCounter = tick
            flapTargets = list(map(int, str(simpleCounter).zfill(5)))
            flapTargets.reverse()

        elif mode == "LOST":
#            time.sleep(1)
#            print(time.time() - start_time >= 1)
            if time.time() - start_time >= 1:
               start_time = time.time()
               timerLostSeconds -= 1
               if timerLostSeconds < 1:
#                   if timerLostMinutes > 0:
#                       timerLostSeconds = 10
#                   if timerLostMinutes >= 1:
#                       timerLostMinutes  -= 1
                   if timerLostMinutes > 0:
                       timerLostSeconds = 60
                       if timerLostMinutes >= 1:
                           timerLostMinutes -= 1 
                   else:
                       timerLostSeconds = 0

#            print(timerLostMinutes, timerLostSeconds)
            valueMinutes = list(map(int,str(timerLostMinutes).zfill(3)))
            if timerLostMinutes > 4:
                valueSeconds = [0, 0]
            else:
                valueSeconds = list(map(int,str(timerLostSeconds).zfill(2)))

            flapTargets = [valueMinutes[0],valueMinutes[1],valueMinutes[2], valueSeconds[0],valueSeconds[1]]
            flapTargets.reverse()

        elif mode == "CLOCK":
            now = datetime.datetime.now()
            hourArr = list(map(int, str(now.hour).zfill(2)))
            minArr = list(map(int, str(now.minute).zfill(2)))
            flapTargets = [-1, hourArr[0], hourArr[1], minArr[0], minArr[1]]
            flapTargets.reverse()



        for drum in range(numberOfDrums):

            if not isCalibrated[drum]:    #if not calibrated yet, move drum until it is
                isDrumActive[drum] = True

            else:                         # if this drum is already calibrated, behave normally

                if flapTargets[drum] != -1:
                    if mode == "CLOCK":
                        newPos = flapsCrono[flapTargets[drum]] * stepsPerFlap
                    elif mode == "LOST":
                        newPos = flapsTimer[flapTargets[drum]] * stepsPerFlap
                else:
                    newPos = flapsEmptyPosition

                if newPos < drumTargetPositions[drum]:
                    newPos += fullTurn

                drumTargetPositions[drum] = newPos # + drumOffsets[drum]

                if drumTargetPositions[drum] > drumPositions[drum] + drumOffsets[drum]:
                    isDrumActive[drum] = True

                else:
                    isDrumActive[drum] = False

        readSensors()
        moveDrums()

#        if True:
#        if isDrumActive[0] == False and isDrumActive[1] == False and isDrumActive[2] == False and isDrumActive[3] == False and isDrumActive[4] == False:
#            if mode == "LOST" and timerLostMinutes >= 0:
#                time.sleep(1)
#                timerLostSeconds -= 1
#                if timerLostSeconds < 0:
#                    timerLostSeconds = 60
#                    timerLostMinutes -= 1

except KeyboardInterrupt:
    print("Interrupted by keyboard")

except Exception as err:
    print("EXCEPTION!")
    print("Ops!", err)
    
    

finally:
    #GPIO.cleanup()
    for drum in range(numberOfDrums):
        for pin in range(4):
            GPIO.output(controlPins[drum][pin], GPIO.LOW)
            exit(0)



exit(0)

