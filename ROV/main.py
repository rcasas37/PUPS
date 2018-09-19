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

	#Initialize I2C bus slave addresses explicitly to default values
	###Set parameters that hold the slave addresses in Hex or decimal??

	#Initialize rov class/module instance
	rov = rov_skeleton.rov()

	#Initialize sensor class/module instance
	atlas_sensor = rov_skeleton.sensors.atlas_sensors() #####This is how you get at attribute within the import list
	#test_parameter = rov_skeleton.test.test_class() #####This is how you get at attribute within the import list

	#Create atlas sensor thread
	atlas_sensor_thread = Thread(target=atlas_sensor.run)

	#Start Sensor thread
	atlas_sensor_thread.start()

	#Set up dissolved Oxygen sensor parameters
		

	"""
	Description While Loop:
	The while loop does what?? Oh that is right, EVERYTHING!
	"""
	while True:
		#Everything goes here
		rov.test_function()		#Show that a function can be called through the class/module we imported
		#print("This is the default_address from the DO sensor: %d" %atlas_sensor.attribute_thing)
		#end_expedition = input("End expedition(y=1, n=0)? ")
		#end_expedition = 1 #Exits the while loop when we get specific cmd from user
		#break; #This also exits the while loop if some condition is met
		
		

		"""End While Loop"""


	return #End main() Definition#


#Runs the main just defined above
main()