#!/usr/bin/env python

"""
    work.py 
    
"""

import rospy, os, sys
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient

class Work:
    def __init__(self, script_path):
        rospy.init_node('work')
        rospy.on_shutdown(self.cleanup)
        self.soundhandle = SoundClient()
        
        # Wait a moment to let the client connect to the sound_play server
        rospy.sleep(1)
        
        # Make sure any lingering sound_play processes are stopped.
        self.soundhandle.stopAll()
        
        # Announce that we are ready for input
        rospy.loginfo("Ready, waiting for commands...")
	self.soundhandle.say('Hello, I am Robort. What can I do for you?')
	#rospy.sleep(5)

        # Subscribe to the recognizer output and set the callback function
        rospy.Subscriber('/lm_data', String, self.talkback)
        
        #self.turn_on_camera = rospy.Publisher("turn_on_camera", String, queue_size=10)

    def talkback(self, msg):
        # Print the recognized words on the screen
        rospy.loginfo(msg.data)

	if msg.data.find('WHAT CAN YOU DO')>-1:
                self.soundhandle.say(' I have a magic that makes you beautiful.')
                rospy.loginfo('I have a magic that makes you beautiful.')
		#rospy.sleep(10) 
        elif msg.data.find('WOW WHAT IS IT')>-1:
                self.soundhandle.say('I can whiten your skin.')
                self.soundhandle.say('Besides, I can bring you a beautiful Christmas hat.')
                rospy.loginfo('I can whiten your skin.Besides, I can bring you a beautiful Christmas hat.')
	elif msg.data.find('LET ME TRY')>-1:
        	#rospy.sleep(1)
                self.soundhandle.say('Ok, get ready. please press the keyboard "s".')
                rospy.loginfo('You want to take a photo? Ok, get ready. please press the keyboard "s".')
                os.system("/home/dong/catkin_ws/src/rc-home-edu-learn-ros/rchomeedu_speech/scripts/turn_on_camera.py")
                rospy.loginfo('save photos.')
		#rospy.sleep(5)
        elif msg.data.find('THAT IS GREAT THANK YOU')>-1:
                self.soundhandle.say('You are welcome.It is my pleasure to make you happy.')
                rospy.loginfo('You are welcome.It is my pleasure to make you happy.')
	else:rospy.sleep(3)

    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down talkback node...")


if __name__=="__main__":
    try:
        Work(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Work node terminated.")
