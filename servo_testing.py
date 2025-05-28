import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) 

#Setup pins X and Y as an Output Pin instead of the default Input
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)


#This function sends the signal on and off in 2 second intervals.
def valve_OnOff(PIN):
    while True:
        GPIO.output(12,GPIO.HIGH)
        sleep(2)
        GPIO.output(12, GPIO.LOW)
        sleep(2)
        valve_OnOff(12)
        GPIO.cleanup()