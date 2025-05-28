#!/usr/bin/env python

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError

class ImageProcessor():
	def __init__(self):
		# Set up the CV Bridge
		self.bridge = CvBridge()

		# Set up the subscriber (input) and publisher (output)
		self.sub_img = rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, self.callback_img)
		self.pub_img = rospy.Publisher('~image_raw/compressed', CompressedImage, queue_size=1)

		# Make sure we clean up all our code before exitting
		rospy.on_shutdown(self.shutdown)

	def shutdown(self):
		# Unregister anything that needs it here
		self.sub_img.unregister()

	def callback_img(self, msg_in):
		# Convert ROS image to CV image
		try:
			cv_image = self.bridge.compressed_imgmsg_to_cv2( msg_in, "bgr8" )
		except CvBridgeError as e:
			rospy.logerr(e)

		# ===================
		# Do processing here!
		# ===================
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

		cv2.circle(gray, (200, 200), 20, (0,255,0), thickness=2)
		# ===================

		# Convert CV image to ROS image and publish
		try:
			self.pub_img.publish( self.bridge.cv2_to_compressed_imgmsg( gray ) )
		except CvBridgeError as e:
			rospy.logerr(e)

if __name__ == '__main__':
	# Initialize
	rospy.init_node('egh450_image_processor', anonymous=True)

	ip = ImageProcessor()
	rospy.loginfo("[IMG] Processing images...")

	# Loop here until quit
	rospy.spin()