#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests
from datetime import datetime
import rospy
from gas_py.msg import gas_msg
#패키지의 msg파일 불러오기. msg파일 내부에 있는 변수들의 집합이라고 생각하면 될듯

#메시지를 받으면 실행되는 콜백 함수
def callback_gas(data):
	
	tempDate=datetime.now()
	tmp=tempDate.strftime('%Y-%m-%d %H:%M:%S')	
	print(tempDate.strftime('%Y-%m-%d %H:%M:%S'))
	CO_tmp=data.CO_data
	gas_tmp=data.gas_data
	sm_tmp=data.smoke
	rospy.loginfo("%s", data.detect)
	rospy.loginfo("%f",data.gas_data)
	rospy.loginfo("%f",data.CO_data)
	rospy.loginfo("%f",data.smoke)
	rospy.loginfo("%f",data.x)
	rospy.loginfo("%f",data.y)
	x=data.x
	y=data.y
	ID=0
	res = requests.post("http://163.152.223.21:3000/fire", json={'detectionTime': tmp, 'patrolID' : ID, 'positionX' : x, 'positionY': y, 'smokeDensity' : sm_tmp, 'fireDensity' : gas_tmp})
	print(res.content)

#메인 함수
def main():
	print("start")
	rospy.init_node('topic_sub', anonymous=True)#노드 초기화
	rospy.Subscriber('gas_detect', gas_msg, callback_gas)
	rospy.Subscriber('gas_flame_detect', gas_msg, callback_gas)

#토픽 메시지 받으면 콜백 함수 실행
#flame_detect라는 토픽, flame_msg라는 메시지 수신하면 콜백함수 실헹
	rospy.spin()

if __name__ == '__main__':
	main()
