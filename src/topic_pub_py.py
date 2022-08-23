#!/usr/bin/env python
#-*- coding:utf-8 -*-
#import RPi.GPIO as GPIO
import rospy,sys
from mq import *
import smbus
from geometry_msgs.msg import PoseWithCovarianceStamped
bus=smbus.SMBus(1)
add=0x48


#gpio 번호 그대로 사용
#GPIO.setmode(GPIO.BCM)

#gpio, 입력 출력 결정
#GPIO.setup(gas_channel, GPIO.IN)
#화염 감지하면 출력 함수
from gas_py.msg import gas_msg


def readAD1():
	analog=bus.read_byte(add, 0x01)
	return analog

def publish_only_gas():
	print("gas detected")
	msg.detect="gas detected"
	msg.CO_data=perc["CO"]
	msg.gas_data=perc["GAS_LPG"] 
	msg.smoke=perc["SMOKE"]
	pub_gas.publish(msg)

def input_x_y(msg):
	x=msg.pose.pose.position.x
	y=msg.pose.pose.position.y
	msg.x=x
	msg.y=y

def publish_gas_flame():
	print("gas and flame detected")
	msg.detect="gas flame both detected"
	msg.CO_data=perc["CO"]
	msg.gas_data=perc["GAS_LPG"] 
	msg.smoke=perc["SMOKE"]
	pub_both.publish(msg)


def main():
	#initializing node
	rospy.init_node('topic_pub_gas', anonymous=True)
	global msg
	msg=gas_msg()
	
	global pub_gas
	global pub_both

	#publisher for gas, flame and both
	pub_gas = rospy.Publisher('gas_detect', gas_msg, queue_size=10)
	pub_both=rospy.Publisher('gas_flame_detect', gas_msg, queue_size=10)	
	rate = rospy.Rate(1)

	print("Press CTRL+C to abort.")


    	mq = MQ();
    	global perc
	
   	while True:
        	perc = mq.MQPercentage()
        	sys.stdout.write("\r")
        	sys.stdout.write("\033[K")
		an1=readAD1()
		#flame+gas
		if(an1>700 and (perc["GAS_LPG"] >0.095 or perc["CO"]>0.015 or perc["SMOKE"])):
			publish_gas_flame()
		#only gas
		elif(perc["GAS_LPG"] >0.095 or perc["CO"]>0.015 or perc["SMOKE"] and (not an1>700)):
			publish_only_gas()

	while (True):
		rate.sleep()


if __name__ == '__main__':
	try:
		print("start")
		main()
	except rospy.ROSInterruptException:
		pass
