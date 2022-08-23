#!/usr/bin/env python
#-*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import rospy,sys
from mq import *
#gpio 번호
from geometry_msgs.msg import PoseWithCovarianceStamped
#gpio 번호 그대로 사용
GPIO.setmode(GPIO.BCM)

#gpio, 입력 출력 결정

#화염 감지하면 출력 함수
from gas_py.msg import gas_msg


def publish_only_gas():
        msg.detect="gas detected"
        msg.CO_data=perc["CO"]
        msg.gas_data=perc["GAS_LPG"]
        msg.smoke=perc["SMOKE"]
        pub_gas.publish(msg)

def publish_both():
        msg.detect="both flame gas detected"
        msg.CO_data=perc["CO"]
        msg.gas_data=perc["GAS_LPG"]
        msg.smoke=perc["SMOKE"]
        pub_gas.publish(msg)

def input_x_y(msg):
        x=msg.pose.pose.position.x
        y=msg.pose.pose.position.y
        msg.x=x
        msg.y=y

def readAD1():
        analog=bus.read_byte(add)
        return analog
def main():
        #initializing node
        rospy.init_node('topic_pub', anonymous=True)
        global msg
        msg=gas_msg()
        rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, input_x_y)
        global pub_both
        global pub_gas
        #publisher for gas, flame and both
        pub_gas = rospy.Publisher('gas_detect', gas_msg, queue_size=10)
        rate = rospy.Rate(1)


        print("Press CTRL+C to abort.")
        mq=MQ()
        global perc
        pub_both = rospy.Publisher('gas_flame_detect', gas_msg, queue_size=10)

        while True:
                an1=readAD1()

                perc = mq.MQPercentage()
                sys.stdout.write("\r")
                sys.stdout.write("\033[K")
                #both light gas
                if(an1>700 and (perc["GAS_LPG"] > 0.095 or perc["CO"]>0.015 or perc["SMOKE"]>0.032)):
                        publish_both()
                #only gas
                elif(not (an1 >700) and (perc["GAS_LPG"] > 0.095 or perc["CO"]>0.015 or perc["SMOKE"]>0.032)):
                        publish_only_gas()
        while (True):
                rate.sleep()


if __name__ == '__main__':
        try:
                print("check")
                main()
        except rospy.ROSInterruptException:
                pass

