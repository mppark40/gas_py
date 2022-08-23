from mq import *
import sys, time
import rospy
from flame_msg.msg import flame_msg

def publish_only_gas():
	print("gas detected")
	msg.detect="gas detected"
	msg.CO_data=perc["CO"]
	msg.gas_data=["GAS_LPG"]
	msg.smoke=["SMOKE"]
	pub_gas.publish(msg)

try:
    print("Press CTRL+C to abort.") 
    mq = MQ();
    global perc

    pub_gas = rospy.Publisher('gas_detect', flame_msg, queue_size=10)
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
	
	if(perc["GAS_LPG"] >0.095 or perc["CO"]>0.015 or perc["SMOKE"])
        	sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"])):
		publish_only_gas()
		
        sys.stdout.flush()
        time.sleep(0.1)

except:
    print("\nAbort by user")


