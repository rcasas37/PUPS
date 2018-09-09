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

import sys	#Module provides access to fns maintained by the interpreter
import os	#Module provides fns allowing one to use OS dependent functionality


#Initialize I2C bus slave addresses explicitly to default values
###Set parameters that hold the slave addresses in Hex



"""
The main loop will control all of the operations of the ROV
Parameters:

Return:
	0 on success, error code on failure
Notes:
	Initialized all sensor 
"""
def main():

	"""write my comments here for a
	multiple line comment"""
	#Or here both work
	"""This is the main python program for the ROV"""

if __name__ == '__main__':
	sys.exit(main())



"""
Obtain string commands from cmd center.
"""
def read_serial_port():

	return;