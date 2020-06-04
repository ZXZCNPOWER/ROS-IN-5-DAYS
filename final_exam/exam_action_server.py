#! /usr/bin/env python
import rospy
import time
import actionlib

from record_odom.msg import EXAMActionMsgFeedback, EXAMActionMsgResult, EXAMActionMsgAction
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

class EXAMActionMsgClass(object):
    
  # create messages that are used to publish feedback/result
  _result   = EXAMActionMsgResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("rec_odom_as", EXAMActionMsgAction, self.goal_callback, False)
    self._as.start()

    
  def goal_callback(self, goal):
    # this callback is called when the action server is called.
    
    # helper variables
    success = True
    r = rospy.Rate(1)
    
    
    i = 0
    for i in xrange(0, 4):
    
      # check that preempt (cancelation) has not been requested by the action client
      if self._as.is_preempt_requested():
        rospy.loginfo('The goal has been cancelled/preempted')
        # the following line, sets the client in preempted state (goal cancelled)
        self._as.set_preempted()
        success = False
        break
    

      # the sequence is computed at 1 Hz frequency
      r.sleep()
    
    # at this point, either the goal has been achieved (success==true)
    # or the client preempted the goal (success==false)
    # If success, then we publish the final result
    # If not success, we do not publish anything in the result
    if success:
      self._result = EXAMActionMsgResult
      self._as.set_succeeded(self._result)
      
      
if __name__ == '__main__':
  rospy.init_node('action_custom_msg')
  CustomActionMsgClass()
  rospy.spin()
