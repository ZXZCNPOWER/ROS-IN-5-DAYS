#! /usr/bin/env python
import rospy
import time
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback
from basics_exam.msg import record_odomFeedback, record_odomResult, record_odomAction
from nav_msgs.msg import Odometry
from std_msgs.msg import Empty
from std_srvs.srv import Trigger, TriggerRequest
from geometry_msgs.msg import Twist 
import math
from geometry_msgs.msg import Vector3

rospy.init_node('main_client_node')
rate = rospy.Rate(1)
timer_60 = False
goal = Empty()
request = TriggerRequest()
client_as = actionlib.SimpleActionClient('/rec_odom_as', record_odomAction)
client_as.wait_for_server()
client_service = rospy.ServiceProxy('crash_direction_service', Trigger)
client_pub_move = rospy.Publisher('cmd_vel', Twist, queue_size=1)
move = Twist()
result_as = TriggerRequest()
state_result = client_as.get_state()

def calculate_dist_between(p1, p2):
        
        distance_vector = Vector3()
        distance_vector.x = p2.x - p1.x
        distance_vector.y = p2.y - p1.y
        
        length = math.sqrt(math.pow(distance_vector.x,2)+math.pow(distance_vector.y,2))
        return length

def get_dist_moved(odmetry_data_list):
    distance = None
        
    if len(odmetry_data_list) >= 2 :
        start_odom = odmetry_data_list[0]
        end_odom = odmetry_data_list[len(odmetry_data_list)-1]
            
        start_position = start_odom.pose.pose.position
        end_position = end_odom.pose.pose.position

        distance = calculate_dist_between(distance_vector)        
    else:
        rospy.logerr("Odom array doesnt have the minimum number of elements = "+str(len(odmetry_data_list)))
        
    return distance     

while not timer_60:    
    success = True
    #if client_as.is_preempt_requested():
            #rospy.loginfo('The goal has been cancelled/preempted')
            # the following line, sets the client in preempted state (goal cancelled)
            #client_as.set_preempted()
            #success = False
            
    client_as.send_goal(goal, feedback_cb=None) #start timer 60
    result = client_service(request) #ask for direction

    if result == 'front': #move
        move.linear.x = 0.1
        move.angular.z = 0.0
    elif result == 'right':
        move.linear.x = 0.0
        move.angular.z = -0.2
    else: # result == 'left':
        move.linear.x = 0.0
        move.angular.z = 0.2
    
    if state_result == 2: #wait for timer
        result_as = client_as.get_result()
        total_dist_moved = get_dist_moved(result_as.Result)
        timer_60 = True
        if total_dist_moved >= 2.0:
            print('I am outside')
        else:
            print('I am still inside')
    
    client_pub_move.publish(move)
    rate.sleep()