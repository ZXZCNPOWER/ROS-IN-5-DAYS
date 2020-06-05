#! /usr/bin/env python

import rospy
import time
from std_srvs.srv import Trigger, TriggerResponse
from sensor_msgs.msg import LaserScan

def service_callback(request):  
    _response.success = True
    return  _response

def topic_callback(msg):
    #print(msg.ranges[360])
    '''
    if msg.ranges[360] < 0.1:
        _response.message = 'right'
    elif msg.ranges[0] < 0.1:
        _response.message = 'left'
    elif msg.ranges[719] < 0.1:
        _response.message = 'right'
    else:
        _response.message = 'front'
    '''
    if msg.ranges[360] > 1:
        _response.message = 'front'

#If the distance to an obstacle in front of the robot is smaller than 1 meter, the robot will turn left
    elif msg.ranges[360] < 1: 
         _response.message = 'right'        
#If the distance to an obstacle at the left side of the robot is smaller than 0.3 meters, the robot will turn right
    elif msg.ranges[719] < 0.3:
         _response.message = 'right'
        
#If the distance to an obstacle at the right side of the robot is smaller than 0.3 meters, the robot will turn left
    elif msg.ranges[0] < 0.3:
         _response.message = 'left'

    
    print(_response.message)

rospy.init_node('service_server') 
sub = rospy.Subscriber('/scan', LaserScan, topic_callback)
my_service = rospy.Service('/crash_direction_service', Trigger, service_callback) 
_response = TriggerResponse()
rospy.spin() 