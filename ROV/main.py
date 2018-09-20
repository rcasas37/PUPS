"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: SEAL
File: main.py
--------
Contains the main loop and uses functions that run SEAL's rov. Including
movement, sensor readings, and communication to SEAL's cmd center.
"""


#Import code modules
import rov_skeleton #Module provides access to all of the fns with our class 'rov'
from threading import Thread
#import sensors	#Module provides all of the sensor classes 
#import test  #NOT A real import. Delete after done

#Global variables
#global my_var = 100 



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
	end_expedition = 0 	#variable to end program's main


	#Initialize I2C bus slave addresses explicitly to default values ###Set parameters that hold the slave addresses in Hex or decimal??

	#Initialize class objects and instances 
	rov = rov_skeleton.rov()		#Init rov class/module instance
	atlas_sensor = rov_skeleton.sensors.atlas_sensors()	 #Initialize atlas sensor class/module instance


	#Buttons that can be set via command center
	stop_motors = False
	get_all_meas = False

	#Other Essential variables
	cmd_id = 0x00 	#Command ID stored as decimal number in python
	get_essential meas = True #This guy should always be true might not even need var for him	


	#Open serial port communication


	#Create sensor and command .xml files for data storage



	"""
	Description While Loop:
	The while loop does what?? Oh that is right, EVERYTHING!
	"""
	while True:
		#Everything goes here






		get_all_meas = input("Would you like to get all measurements? ")


		rov.test_function()		#Show that a function can be called through the class/module we imported

		#Take all Sensor measurements
		if get_all_meas == True:
			#Create atlas sensor thread
			atlas_sensor_thread = Thread(target=atlas_sensor.run)
			#Start Sensor thread
			atlas_sensor_thread.start()

			#get essential meas here
		else: 	#Get only temp, pressure, accel, and gyro meas
			#Get essential meas here


		#end_expedition = input("End expedition(y=1, n=0)? ")
		#end_expedition = 1 #Exits the while loop when we get specific cmd from user
		#break; #This also exits the while loop if some condition is met
		
		

		"""End While Loop"""

	#End Sensor thread
	atlas_sensor_thread.terminate_thread()

	return 1 #End main() Definition#


#Runs the main just defined above
main()