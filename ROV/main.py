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

#Global variables
#global my_var = 100 """Example if absolutely needed ONLY"""



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

	"""write my comments here for a
	multiple line comment"""
	#Or here both work
	"""This is the main python program for the ROV"""

	#Initialize I2C bus slave addresses explicitly to default values
	###Set parameters that hold the slave addresses in Hex

	#Initialize rov class/module instance
	rov = rov_skeleton.rov()

	"""
	Description While Loop:
	The while loop does what?? Oh that is right, EVERYTHING!
	"""
	while end_expedition != 100:
		#Everything goes here
		rov.test_function()		#Show that a function can be called through the class/module we imported
		#end_expedition = input("End expedition(y=1, n=0)? ")
		#end_expedition = 1 #Exits the while loop when we get specific cmd from user
		#break; #This also exits the while loop if some condition is met
		end_expedition += 10

		"""End While Loop"""


	return #End main() Definition#


#Runs the main just defined above
main()