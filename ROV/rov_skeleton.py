"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: SEAL
File: rov_skeleton.py
--------
Will contain the main loop and functions that run SEAL's rov. Including movement, 
sensor readings, and communication to SEAL's cmd center.
"""

#Import python modules
import sys	#Module provides access to fns maintained by the interpreter
import os	#Module provides fns allowing one to use OS dependent functionality
from threading import Thread 	#Module provides multiple thread functionality
import time	#Module provides SW delay functionality



#Global variables
#global my_var		"""Example if absolutely needed ONLY"""
#my_var = 34 



"""
The main loop will control all of the operations of the ROV
Parameters:

Return:
	0 on success, error code on failure
Notes:
	Initialized all sensor address data before main while loop 
"""
def main():
	#Define some variables used within main
	end_expedition = 0

	"""write my comments here for a
	multiple line comment"""
	#Or here both work
	"""This is the main python program for the ROV"""

	#Initialize I2C bus slave addresses explicitly to default values
	###Set parameters that hold the slave addresses in Hex

	"""
	Description While Loop:
	The while loop does what?? Oh that is right, EVERYTHING!
	"""
	while end_expedition != 1:
		#Everything goes here


		#end_expedition = 1 #Exits the while loop when we get specific cmd from user
		#break; #This also exits the while loop if some condition is met

		"""End While Loop"""


	return #End main() Definition#



"""
Obtain string commands from cmd center.
Parameters:
	list of parameters
Return:
	Do we return any value?
Notes:
"""
def read_serial_port():

	return



"""
Obtain string commands from cmd center.
Parameters:
	list of parameters
Return:
	Do we return any value?
Notes:
"""
def write_serial_port():

	return


"""
Opens .xml and reads from it
Parameters:
	list of parameters
Return:
	Do we return any value?
Notes:
"""
def read_xml():
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
def write_xml():
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
def parse_control_data():
	#parse the data string from buffer then write each piece to .xml

	#write_xml()
	return



"""
Sends sensor data. Opens sensor.xml and combines into a string packet and sends through serial port
Parameters:
	list of parameters
Return:
	Do we return any value?
Notes:
"""
def send_sensor_data():
	#Open sensor.xml concatenate all sensor data into string close sensor.xml

	#write_seral_port() the string we just created
	return





#get each sensor data
#calculate motor spd
#set motor spd choose based on selected ESC channel
#get all meas
#get essential meas
#stabilize ROV???

#parse input cmd or is this write_xml??
