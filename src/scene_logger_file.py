#!/usr/bin/env python

# instantiates listeners for the current topics we thought of.
# get latest value of everything. see if it change. if it did, update latest
# value and write results in a log file
import rospy
import os
import time
from std_msgs.msg import String

class ActLogger():
    def __init__(self):
        rospy.init_node('actlogger', anonymous=True)
        logfile_path = os.path.expanduser(rospy.get_param('~logfile_path','human_act.log'))
        self.logger = open(logfile_path, "a")
        #logger = setup_logger('activity_logger', logfile_path)
        #logging.basicConfig(filename=logfile_path, format='%(asctime)s %(message)s', level=logging.DEBUG)
        #rospy.loginfo('saving file in:'+logfile_path)
        self.logger.write("Started logging human activity.\n")
        self.difflog = rospy.get_param('~diff',True)
        rate_value = rospy.get_param('~rate')
        rate = rospy.Rate(rate_value)
        rospy.Subscriber("/subject/action", String, self.callback)
        self.lastdata = ''
        rospy.spin()
        #while not rospy.is_shutdown():
        #    logger.write('alive\n')
            ### here we go through all of the topics, see if they changed - I am going to store the last bit of info of each to do the comparison
        #    rate.sleep()
    def callback(self, data):
        rospy.logdebug(rospy.get_caller_id() + ": I heard %s lastadata is %s", data.data ,self.lastdata)
        if self.difflog and (data.data in self.lastdata):
            rospy.loginfo_throttle(20,"Got same result as last time. Logging nothing.")

            pass
        else:
            now = rospy.get_rostime()
            #timestr = "[%i %i] " % (now.secs, now.nsecs)
            #timestr = time.strftime('%l:%M%p %Z on %b %d, %Y', time.gmtime(now.secs))
            timestr = time.strftime('[%Y-%b-%d (%Z) %H:%M:%S]', time.gmtime(now.secs))
            actloggerstring = timestr+ data.data+"\n"
            self.logger.write(actloggerstring)
            rospy.logdebug(actloggerstring)

        self.lastdata = data.data
if __name__ == '__main__':
    try:
        mylogger = ActLogger()

    except rospy.ROSInterruptException:
        pass
