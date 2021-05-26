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

def readSensors():
    global pinSensors
    global isSensorHit
    global isCalibrated
    
    for drum in range(numberOfDrums):
        if GPIO.input(pinSensors[drum]): 
            isSensorHit[drum] = True
        else:
            if isSensorHit[drum] and not isCalibrated[drum]:
                isCalibrated[drum] = True
                isSensorHit[drum] = False
                
###########################################
def moveDrums():
    global pinSensors
    global isSensorHit
    global isCalibrated
    global isDrumActive
    global numberOfDrums
    
    
    for step in range(4):
        for pin in range(4):
            for drum in range(numberOfDrums):
                if (isDrumActive[drum]):
                    GPIO.output(controlPins[drum][pin], seq[step][pin])
                else:
                    GPIO.output(controlPins[drum][pin], GPIO.LOW)
        time.sleep(0.002) # + ((numberOfDrums ) * 0.0004))
    
###########################################
try:
    while True:
        readSensors()
        for drum in range(numberOfDrums):
            if not isCalibrated[drum]:
                isDrumActive[drum] = True
                #print("activating",drum);
            else:
                isDrumActive[drum] = False
                #print("deactivating",drum);

        
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
                
#while isSensorHit[0] == False:
#    for step in range(4):
#        for pin in range(4):
#            GPIO.output(controlPins[0][pin], seq[step][pin])
#        time.sleep(0.002)
#    readSensors()





#GPIO.output(2,GPIO.LOW)
#GPIO.output(3,GPIO.LOW)
#GPIO.output(4,GPIO.LOW)
#GPIO.output(17,GPIO.LOW)


#GPIO.cleanup()
exit(0)

