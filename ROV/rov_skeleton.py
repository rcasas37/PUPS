"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: SEAL
File: rov_skeleton.py
--------
Will contain the rov class and functions that run SEAL's rov. Including movement, 
sensor readings, and communication to SEAL's cmd center.
"""

#Import python/sensor modules
import sys	#Module provides access to fns maintained by the interpreter
import os	#Module provides fns allowing one to use OS dependent functionality
#from threading import Thread 	#Module provides multiple thread functionality
import time	#Module provides SW delay functionality
#import test #NOT real import. DELETE after use!!!!
import sensors	#Module provides all of the sensor classes 


#Global variables
#global my_var		"""Example if absolutely needed ONLY"""
#my_var = 34 

class rov:
	#########################################################################3
	"""
	The main loop will control all of the operations of the ROV
	Parameters:

	Return:
		0 on success, error code on failure
	Notes:
		Initialized all sensor address data before main while loop 
	def main():
		#Define some variables used within main
		end_expedition = 0

		#Or here both work

		#Initialize I2C bus slave addresses explicitly to default values
		###Set parameters that hold the slave addresses in Hex

		Description While Loop:
		The while loop does what?? Oh that is right, EVERYTHING!
		""
		while end_expedition != 1:
			#Everything goes here


			#end_expedition = 1 #Exits the while loop when we get specific cmd from user
			#break; #This also exits the while loop if some condition is met

			###End While Loop###


		return #End main() Definition#
	"""
	#########################################################################3

	"""TEST function"""
	def test_function(default_arg):
		print("You are inside the test function available through the rov class.")
		return





	"""
	Obtain string commands from cmd center.
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def read_serial_port(default_arg):

		return



	"""
	Obtain string commands from cmd center.
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def write_serial_port(default_arg):

		return


	"""
	Opens .xml and reads from it
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def read_xml(default_arg):
		#open .xml read what i want and close .xml
		return



	"""
	Opens .xml and writes to it
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def write_xml(default_arg):
		#open.xml write to it and close .xml
		return



	"""
	Parses data received from serial port and writes it to .xml
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def parse_control_data(default_arg):
		#parse the data string from buffer then write each piece to .xml

		#write_xml()	#writes to control.xml values of each control data pt.
		return



	"""
	Sends sensor data. Opens sensor.xml and combines into a string packet and sends through serial port
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def send_sensor_data(default_arg):
		#Open sensor.xml concatenate all sensor data into string close sensor.xml

		#write_serial_port() #Write the string we just created to serial port
		return



	"""
	Uses control.xml values to calculate PWM (dir & spd) of selected motor
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def calc_motor_spd(default_arg):
		#Open control.xml read selected value, calc PWM write it into .xml and close xml

		return



	"""
	Uses control.xml values to send PWM value to motor for driving
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def set_motor_spd(default_arg):
		#Open control.xml read selected vals & write to ESC channel(s) via I2C bus close .xml

		return



	"""
	Obtains temp, pressure, accelerometer, and gyroscope measurements
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def get_essential_meas(default_arg):
		#Open sensor.xml, obtain sensor measurements, write to sensor.xml and close

		#write_xml()	#writes to sensor.xml value of obtained sensor meas
		return



	"""
	Obtains essential measurements(temp, pres., and accel/gyro) and
	Dissolved Oxy, pH, and Salinity
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def get_all_meas(default_arg):
		#Open sensor.xml, obtain all sensor meas, write to sensor.xml and close 
		#get_essential_meas()

		#write_xml()	#writes to sensor.xml value of obtained sensor meas
		return



	"""
	Attempts to stabilize rov via accelerometer and gyro if user sends to mvmt cmds
	Parameters:
		list of parameters
	Return:
		Do we return any value?
	Notes:
	"""
	def stabilize_rov(default_arg):
		#This one is gonna be a beach

		return


	#get each sensor data
	#parse input cmd or is this write_xml??
