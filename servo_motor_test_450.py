#!/usr/bin/env python3
import rospy
from time import sleep
import RPi.GPIO as GPIO
from std_msgs.msg import Bool

sub_a = None
chan_list = [12,13] # Set the channels you want to use (see RPi.GPIO docs!)

def callback_a(msg_in):
	# A bool message contains one field called "data" which can be true or false
	# http://docs.ros.org/melodic/api/std_msgs/html/msg/Bool.html
	# XXX: The following "GPIO.output" should be replaced to meet the needs of your actuators!
	if msg_in.data:
		rospy.loginfo("Setting output high!")
		while True:
			GPIO.setmode(GPIO.BOARD)# Use physical pin numbering
			GPIO.setup(chan_list, GPIO.OUT)
			GPIO.output(chan_list, GPIO.HIGH)
			sleep(2)
			GPIO.output(chan_list, GPIO.LOW)
			rospy.loginfo("Complete")
	else:
		rospy.loginfo("Setting output low!")
		GPIO.output(chan_list, GPIO.LOW)
		rospy.loginfo("Complete")

def shutdown():
	# Clean up our ROS subscriber if they were set, avoids error messages in logs
	if sub_a is not None:
		sub_a.unregister()

	# Close down our GPIO
	GPIO.cleanup()

if __name__ == '__main__':
    # Setup the ROS backend for this node
    rospy.init_node('actuator_controller', anonymous=True)

    # Setup the GPIO
    GPIO.setmode(GPIO.BOARD)# Use physical pin numbering
    GPIO.setup(chan_list, GPIO.OUT)

    # Setup the publisher for a single actuator (use additional subscribers for extra actuators)
    sub_a = rospy.Subscriber('/actuator_control/actuator_a', Bool, callback_a)

    # Make sure we clean up all our code before exiting
    rospy.on_shutdown(shutdown)

    # Loop forever
    rospy.spin()
