#!/usr/bin/env python
import rospy
import time
from scene_description.srv import *
from std_srvs.srv import Empty
from std_msgs.msg import String

global done 
done = False

def donecallback(data):
    global done
    if data.data == "1":
	done = True
    pass

def statemachine():
    ### things are launched
    #now I need to send a service call to load split 1
    rospy.wait_for_service('/readpathnode/read_split')
    rospy.wait_for_service('/videofiles/videofiles_stream/play')
    rospy.Subscriber("/readpathnode/done", String, donecallback)
    try:
        s_h = rospy.ServiceProxy('/readpathnode/read_split', split)
        play_h = rospy.ServiceProxy('/videofiles/videofiles_stream/play', Empty)
        stop_h = rospy.ServiceProxy('/videofiles/videofiles_stream/stop', Empty)
        init_cfer_h = rospy.ServiceProxy('/init_cfer', Empty)
        show_cfer_h = rospy.ServiceProxy('/show_cf', Empty)

        stop_h()
        rospy.loginfo('stopped everything')
        time.sleep(1)
        rospy.loginfo('choosing 1 split')
        s_h(1)
        time.sleep(3)
        rospy.loginfo('playing')
        play_h()
        rospy.loginfo('waiting for tsn_caffe to be alive')
        rospy.wait_for_message('/action', String)
        rospy.loginfo('tsn_caffe is alive. restarting')
        stop_h()
	for i in range(1,5):
	    rospy.loginfo('choosing '+str(i) +' split')
	    s_h(i)
	    time.sleep(3)
	    rospy.loginfo('initialing cfer')
	    init_cfer_h()
	    rospy.loginfo('playing until done')
	    play_h()
	    while not done:
		time.sleep(1)
	    if done:
		global done
		done = False
	    rospy.loginfo('showing cf')
	    show_cfer_h()

    except rospy.ServiceException, e:
        print "service failed: %s"%e
if __name__ == '__main__':
    try:
        rospy.init_node('mystatemachine_node', log_level=rospy.INFO)
        statemachine()
    except rospy.ROSInterruptException:
        pass
