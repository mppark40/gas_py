import rospy
import time
from std_msgs.msg import Empty


def main():
	#initializing node
	rospy.init_node('journey', anonymous=True)
	global msg
	msg=Empty()

	global pub_journey
	#publisher for gas, flame and both
	pub_journey = rospy.Publisher('start_journey', Empty, queue_size=10)
	cnt=0
	while True:
		
		pub_journey.publish(Empty)
		cnt=cnt+1
		if cnt>1:
			break
		time.sleep(180)



if __name__ == '__main__':
	main()
