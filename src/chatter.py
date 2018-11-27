#!/usr/bin/env python

# recieves name, value and rate. publishes those.

# adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29
import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('talker', anonymous=True)
    #testtest = rospy.set_param('~testo','uhskjadsha')
    #print(testtest)
    topic_name = rospy.get_param('~topic_name')
    value = rospy.get_param('~value')
    rate_value = rospy.get_param('~rate')
    pub = rospy.Publisher(topic_name, String, queue_size=1)

    rate = rospy.Rate(rate_value)
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        pub.publish(value)
        #print('hello')
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
