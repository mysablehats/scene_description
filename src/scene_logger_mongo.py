#!/usr/bin/env python

# instantiates listeners for the current topics we thought of.
# get latest value of everything. see if it change. if it did, update latest
# value and write results in a log file
import rospy
import pymongo
import os

def actlogger():
    rospy.init_node('actlogger', anonymous=True)
    logfile_path = os.path.expanduser(rospy.get_param('~logfile_path','human_act.log'))
    topic_name = rospy.get_param('~diff',True)
    rate_value = rospy.get_param('~rate')
    rate = rospy.Rate(rate_value)

    from pymongo import MongoClient
    client = MongoClient()
    db = client.pymongo_test
    posts = db.posts
    post_data = {
        'title': 'Python and MongoDB',
        'content': 'PyMongo is fun, you guys',
        'author': 'Scott'
    }
    result = posts.insert_one(post_data)
    print('One post: {0}'.format(result.inserted_id))
    post_1 = {
        'title': 'Python and MongoDB',
        'content': 'PyMongo is fun, you guys',
        'author': 'Scott'
    }
    post_2 = {
        'title': 'Virtual Environments',
        'content': 'Use virtual environments, you guys',
        'author': 'Scott'
    }
    post_3 = {
        'title': 'Learning Python',
        'content': 'Learn Python, it is easy',
        'author': 'Bill'
    }
    new_result = posts.insert_many([post_1, post_2, post_3])
    print('Multiple posts: {0}'.format(new_result.inserted_ids))
    bills_post = posts.find_one({'author': 'Bill'})
    print(bills_post)
    
    #logger = setup_logger('activity_logger', logfile_path)
    #logging.basicConfig(filename=logfile_path, format='%(asctime)s %(message)s', level=logging.DEBUG)
    #rospy.loginfo('saving file in:'+logfile_path)
    #logger.info("Started logging human activity.")


    while not rospy.is_shutdown():
        #logging.info('alive')
        ### here we go through all of the topics, see if they changed - I am going to store the last bit of info of each to do the comparison
        rate.sleep()
if __name__ == '__main__':
    try:
        actlogger()
    except rospy.ROSInterruptException:
        pass
