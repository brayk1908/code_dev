#!/usr/bin/env python3
# chat

import rospy
import RPi.GPIO as GPIO
from std_msgs.msg import Bool

# Constants
SERVO_PIN = 18       # GPIO pin connected to the servo (BOARD numbering)
PWM_FREQ = 50        # 50 Hz for servo
SPIN_FORWARD_DUTY = 9.0
SPIN_REVERSE_DUTY = 6.0
STOP_DUTY = 7.5

# Global references
pwm = None
sub_a = None

def callback_a(msg_in):
    global pwm
    if msg_in.data:
        rospy.loginfo("Received True - Spinning servo forward")
        pwm.ChangeDutyCycle(SPIN_FORWARD_DUTY)
    else:
        rospy.loginfo("Received False - Spinning servo in reverse")
        pwm.ChangeDutyCycle(SPIN_REVERSE_DUTY)

def shutdown():
    global sub_a, pwm
    rospy.loginfo("Shutting down the continuous servo controller node...")
    if sub_a is not None:
        sub_a.unregister()
    if pwm is not None:
        pwm.ChangeDutyCycle(STOP_DUTY)
        rospy.sleep(0.5)  # Allow it to stop
        pwm.stop()
    GPIO.cleanup()
    rospy.loginfo("GPIO cleanup complete. Shutdown successful.")

if __name__ == '__main__':
    rospy.init_node('continuous_servo_controller', anonymous=True)
    rospy.loginfo("Continuous servo controller node started...")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
    pwm.start(STOP_DUTY)
    rospy.loginfo("PWM started at neutral (stop) position.")

    sub_a = rospy.Subscriber('/actuator_control/actuator_a', Bool, callback_a)
    rospy.loginfo("Subscribed to /actuator_control/actuator_a")

    rospy.on_shutdown(shutdown)
    rospy.spin()
