#!/usr/bin/env python3
#chat
import rospy
import RPi.GPIO as GPIO
from std_msgs.msg import Bool

# Constants
SERVO_PIN = 13       # GPIO pin connected to the servo (BOARD numbering)
PWM_FREQ = 50        # 50 Hz is typical for hobby servos

# Global references
pwm = None
sub_a = None

def callback_a(msg_in):
    global pwm
    if msg_in.data:
        rospy.loginfo("Received True - Moving servo to 180 degrees")
        pwm.ChangeDutyCycle(12.5)  # Adjust if necessary for your servo
    else:
        rospy.loginfo("Received False - Moving servo to 0 degrees")
        pwm.ChangeDutyCycle(2.5)   # Adjust if necessary for your servo

def shutdown():
    global sub_a, pwm
    rospy.loginfo("Shutting down the servo controller node...")
    if sub_a is not None:
        sub_a.unregister()
    if pwm is not None:
        pwm.stop()
    GPIO.cleanup()
    rospy.loginfo("GPIO cleanup complete. Shutdown successful.")

if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node('servo_controller', anonymous=True)
    rospy.loginfo("Servo controller node started...")

    # GPIO setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO_PIN, GPIO.OUT)

    # Start PWM at neutral position (7.5% duty cycle ≈ 90 degrees)
    pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
    pwm.start(7.5)
    rospy.loginfo("PWM started at neutral position (90 degrees).")

    # Subscribe to actuator control topic
    sub_a = rospy.Subscriber('/actuator_control/actuator_a', Bool, callback_a)
    rospy.loginfo("Subscribed to /actuator_control/actuator_a")

    # Register shutdown behavior
    rospy.on_shutdown(shutdown)

    # Keep the node running
    rospy.spin()