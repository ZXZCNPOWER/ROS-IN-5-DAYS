#! /usr/bin/env python
import rospy
import actionlib

#from actionlib_tutorials.msg import FibonacciFeedback, FibonacciResult, FibonacciAction
#from actionlib.msg import TestFeedback, TestResult, TestAction
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from basics_exam.msg import record_odomFeedback, record_odomResult, record_odomAction
from nav_msgs.msg import Odometry

#from actions_quiz.msg import CustomActionMsgFeedback, CustomActionMsgResult, CustomActionMsgAction

import time

class action_class(object):
    
    # create messages that are used to publish feedback/result
    def __init__(self):
        # creates the action server
        self._as = actionlib.SimpleActionServer("rec_odom_as", record_odomAction, self.action_callback, False)
        self._as.start()
        self.ctrl_c = False
        self.r = rospy.Rate(1)
        self._sub = rospy.Subscriber('/odometry/filtered', Odometry, self.topic_callback)
        self._odomdata = Odometry()
        self._result = record_odomResult()
        self.counter = 0

    def topic_callback(self, msg):
        self._odomdata = msg

    def action_callback(self, action):

        success = True
        rospy.loginfo('Executing')


        for i in range(60):
 
            if self._as.is_preempt_requested():

                self._as.set_preempted()
                success = False
                break

            self._result.Result.append(self._odomdata)
            print('sec', i)
            self.r.sleep()

        if success:
            #print('return result')
            self._as.set_succeeded(self._result)

        
  



if __name__ == '__main__':
  rospy.init_node('action_server')
  obj = action_class()
  rospy.spin()