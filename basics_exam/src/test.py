#! /usr/bin/env python
import rospy
import time
import math
from geometry_msgs.msg import Twist 
#from std_srvs.srv import Trigger, TriggerRequest
rospy.init_node('test_node')
rate = rospy.Rate(1)

for i in range(60):
    print(i)
    rate.sleep()
