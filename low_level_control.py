#!/usr/bin/python

"""
Class for low level control of our car. It assumes ros-12cpwmboard has been
installed
"""
import rospy
from i2cpwm_board.msg import Servo, ServoArray
from std_msgs.msg import Int16MultiArray #for the DC HAT
from geometry_msgs.msg import Twist
import time
import csv

class ServoConvert():
    def __init__(self, id=1, direction=1):
   	self.Servor_Min = 6
    	self.Servo_Center = 333
    	self.Servo_Max = 660
	self.id         = id


        self.read_servo_calib_file()
        self.value      = 0.0
        self.value_out  = self.Servo_Center
	self._center	= self.Servo_Center
        self._dir       = direction

    def read_servo_calib_file(self):
	print "read file"
        with open('/home/pirob/catkin_ws/src/donkey_llc/src/Steering_Angles_Correction.csv') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                        print(', '.join(row))
			print(row)
			if row and unicode(row[0], 'utf-8').isnumeric():
				print(self.id)
				if int(row[0]) == self.id:
					self.Servo_Min 		= int(row[1])
					self.Servo_Center 	= int(row[2])
					self.Servo_Max 		= int(row[3])
				print "This was ID: ", self.id

    def get_value_out(self, value_in):
        #--- value is in [-1, 1]
        self.value      = value_in
	if value_in == 0:
		self.value_out = self._center
	elif value_in < 0:
		self.value_out = int(value_in * (self._center-self.Servo_Min) + self._center)+1
	else:
		self.value_out = int(self._center + value_in * (self.Servo_Max - self._center))
        print "self.id, value_in, self.value_out ", self.id, value_in, self.value_out
        return(self.value_out)

class DkLowLevelCtrl():
    def __init__(self):
        rospy.loginfo("Setting Up the Node...")

        rospy.init_node('dk_llc')

        self.actuators = {}
        self.actuators['throttle']  = ServoConvert(id=61) #this is a dc motor
        self.actuators['steering_1']  = ServoConvert(id=1, direction=-1) #-- positive left
	self.actuators['steering_2']  = ServoConvert(id=2, direction=-1) #-- positiv$
	self.actuators['steering_3']  = ServoConvert(id=3, direction=-1) #-- positiv$
	self.actuators['steering_4']  = ServoConvert(id=4, direction=-1) #-- positiv$
        rospy.loginfo("> Actuators corrrectly initialized")

        self._servo_msg       = ServoArray()
        for i in range(4): self._servo_msg.servos.append(Servo())

	self._dc_msg 	      = Int16MultiArray()
        #--- Create the servo array publisher
        self.ros_pub_servo_array    = rospy.Publisher("/servos_absolute", ServoArray, queue_size=1)
        rospy.loginfo("> Servo Publisher corrrectly initialized")

        #--- Create the DC HAT array publisher
        self.ros_pub_dc_array    = rospy.Publisher("/cmd", Int16MultiArray, queue_size=1)
        rospy.loginfo("> DC Publisher corrrectly initialized")

        #--- Create the Subscriber to Twist commands
        self.ros_sub_twist          = rospy.Subscriber("/cmd_vel", Twist, self.set_actuators_from_cmdvel)
        rospy.loginfo("> Subscriber corrrectly initialized")

        #--- Get the last time e got a commands
        self._last_time_cmd_rcv     = time.time()
        self._timeout_s             = 5

        rospy.loginfo("Initialization complete")

    def set_actuators_from_cmdvel(self, message):
        """
        Get a message from cmd_vel, assuming a maximum input of 1
        """
        #-- Save the time
        self._last_time_cmd_rcv = time.time()

        #-- Convert vel into servo values
        self.actuators['throttle'].get_value_out(message.linear.x)
        self.actuators['steering_1'].get_value_out(message.angular.z)
        self.actuators['steering_2'].get_value_out(message.angular.z)
        self.actuators['steering_3'].get_value_out(message.angular.z)
        self.actuators['steering_4'].get_value_out(message.angular.z) 
        rospy.loginfo("Got a command v = %2.1f  s = %2.1f"%(message.linear.x, message.angular.z))
        self.send_servo_msg()

    def set_actuators_idle(self):
        #-- Convert vel into servo values
        self.actuators['throttle'].get_value_out(0)
        self.actuators['steering_1'].get_value_out(0)
	self.actuators['steering_2'].get_value_out(0)
	self.actuators['steering_3'].get_value_out(0)
	self.actuators['steering_4'].get_value_out(0)

        rospy.loginfo("Setting actutors to idle")
        self.send_servo_msg()

    def send_servo_msg(self):
        for actuator_name, servo_obj in self.actuators.iteritems():
	    if 'steering' in actuator_name:
            	self._servo_msg.servos[servo_obj.id-1].servo = servo_obj.id
            	self._servo_msg.servos[servo_obj.id-1].value = servo_obj.value_out
	    elif 'throttle' in actuator_name:
	 	self._dc_msg.data = [-servo_obj.value_out,-servo_obj.value_out,-servo_obj.value_out,servo_obj.value_out]
            rospy.loginfo("Sending to %s command %d"%(actuator_name, servo_obj.value_out))

        self.ros_pub_servo_array.publish(self._servo_msg)
	self.ros_pub_dc_array.publish(self._dc_msg)

    @property
    def is_controller_connected(self):
        print time.time() - self._last_time_cmd_rcv
        return(time.time() - self._last_time_cmd_rcv < self._timeout_s)

    def run(self):

        #--- Set the control rate
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            print self._last_time_cmd_rcv, self.is_controller_connected
            if not self.is_controller_connected:
                self.set_actuators_idle()

            rate.sleep()

if __name__ == "__main__":
   # set_active_board()
    dk_llc     = DkLowLevelCtrl()
    dk_llc.run()
