#! /usr/bin/env python

import rospy                                      # the main module for ROS-python programs
from std_srvs.srv import Trigger, TriggerResponse # we are creating a 'Trigger service'...
                                                  # ...Other types are available, and you can create
                                                  # custom types
def trigger_response(request):

    return TriggerResponse(
        success=True,
        message="front"
    )
 
rospy.init_node('exam_service')                     # initialize a ROS node
my_service = rospy.Service(                        # create a service, specifying its name,
    '/exam_service', Trigger, trigger_response         # type, and callback
)
rospy.spin()   
