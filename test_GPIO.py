import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
pin = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
GPIO.setup(12, GPIO.OUT)


    func = GPIO.gpio_function(n)
    if func == GPIO.OUT:
        GPIO.setup(n, GPIO.IN)
        print("Pin %d is set to input" % n)
    elif func == GPIO.IN:
        GPIO.setup(n, GPIO.OUT)
        print("Pin %d is set to output" % n)
    else:
        print("Pin %d is not set to input or output" % n)


try:
    while True:
        GPIO.output(12, GPIO.HIGH)
        sleep(0.5)
        if GPIO.input(12):
            print("LED ON")
        GPIO.output(12, GPIO.LOW)
        sleep(0.5)
        if not GPIO.input(12):
            print("LED OFF")
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program terminated")