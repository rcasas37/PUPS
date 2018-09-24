#!/usr/bin/python
"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: SEAL
File: sensor.py
--------
Contains all the sensor classes and functions that are use to 
take sensor readings within the ROV
"""

import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps
import string     # helps parse strings

import threading

stop_flag = 1 

class atlas_sensors(threading.Thread):
	long_timeout = 1.5         	# the timeout needed to query readings and calibrations
	short_timeout = .5         	# timeout for regular commands
	default_bus = 1         	# the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
	default_address = 97     	# the default address for the sensor
	current_addr = default_address
	#stop_flag = 1			#stop=1, run=0

	def __init__(self, address=default_address, bus=default_bus):
		# open two file streams, one for reading and one for writing
		# the specific I2C channel is selected with bus
		# it is usually 1, except for older revisions where its 0
		# wb and rb indicate binary read and write
		self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
		self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

		# initializes I2C to either a user specified or default address
		self.set_i2c_address(address)

		self.running = True 
                global stop_flag
                stop_flag = 1
                super(atlas_sensors, self).__init__()
                self._stop_event = threading.Event()

	def terminate_thread(self):
                self._stop_event.set()

	def terminated(self):
                return self._stop_event.is_set()

	def run(self):
                print("Thread self.running parameter: ", self.running)
		while self.running:
                    program()
                    self.running = False

	def set_i2c_address(self, addr):
		# set the I2C communications to the slave specified by the address
		# The commands for I2C dev using the ioctl functions are specified in
		# the i2c-dev.h file from i2c-tools
		I2C_SLAVE = 0x703
		fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
		fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
		self.current_addr = addr

	def write(self, cmd):
		# appends the null character and sends the string over I2C
		cmd += "\00"
		self.file_write.write(cmd)

	def read(self, num_of_bytes=31):
		# reads a specified number of bytes from I2C, then parses and displays the result
		res = self.file_read.read(num_of_bytes)         # read from the board
		response = filter(lambda x: x != '\x00', res)     # remove the null characters to get the response
		if ord(response[0]) == 1:             # if the response isn't an error
			# change MSB to 0 for all received characters except the first and get a list of characters
			char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
			# NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
			return "Command succeeded " + ''.join(char_list)     # convert the char list to a string and returns it
		else:
			return "Error " + str(ord(response[0]))

	def query(self, string):
		# write a command to the board, wait the correct timeout, and read the response
		self.write(string)

		# the read and calibration commands require a longer timeout
		if((string.upper().startswith("R")) or
			(string.upper().startswith("CAL"))):
			time.sleep(self.long_timeout)
		elif string.upper().startswith("SLEEP"):
			return "sleep mode"
		else:
			time.sleep(self.short_timeout)

		return self.read()

	def close(self):
		self.file_read.close()
		self.file_write.close()

	def list_i2c_devices(self):
		prev_addr = self.current_addr # save the current address so we can restore it after
		i2c_devices = []
		for i in range (0,128):
			try:
				self.set_i2c_address(i)
				self.read()
				i2c_devices.append(i)
			except IOError:
				pass
		self.set_i2c_address(prev_addr) # restore the address we were using
		return i2c_devices

	def get_address(self):
		return self.default_address

	def get_stop_flag(self):
		global stop_flag
                return stop_flag

	def set_stop_flag(self, flag):
            global stop_flag 
            stop_flag = flag 
            print("stop flag just set to........",  flag)

def program():
	device = atlas_sensors() 	# creates the I2C port object, specify the address or bus if necessary

        """	
	print(">> Atlas Scientific sample code")
	print(">> Any commands entered are passed to the board via I2C except:")
	print(">>   List_addr lists the available I2C addresses.")
	print(">>   Address,xx changes the I2C address the Raspberry Pi communicates with.")
	print(">>   Poll,xx.x command continuously polls the board every xx.x seconds")
	print(" where xx.x is longer than the %0.2f second timeout." % atlas_sensors.long_timeout)
	print(">> Pressing ctrl-c will stop the polling")
	"""	


	# main loop
	#while True:
	#usr_input = input("Enter command: ")
	usr_input = "R"
	num_sensors = 0		#Must do it once for each sensor
	while num_sensors != 3:
                while device.get_stop_flag() == 1:
                    # do nothing
                    #print("stop flag issss: )", device.get_stop_flag())
                    # If stop flag is 0 = go then do the below
                    dummyinput = "dummy variable"

		#Set i2c address to poll each sensor once: EC=100, DO=97, pH=99	
		if num_sensors == 0:
			device.set_i2c_address(100)
			num_sensors += 1
			print("Testing EC probe...")
		elif num_sensors == 1:
			device.set_i2c_address(97)
			num_sensors += 1
			print("Testing DO probe...")
		else:
			device.set_i2c_address(99)
			num_sensors += 1
			print("Testing pH probe...")

		print("Number of sensors: ", num_sensors)


		if usr_input.upper().startswith("LIST_ADDR"):
			devices = device.list_i2c_devices()
			for i in range(len (devices)):
				print (devices[i])

		# address command lets you change which address the Raspberry Pi will poll
		elif usr_input.upper().startswith("ADDRESS"):
			addr = int(string.split(usr_input, ',')[1])
			device.set_i2c_address(addr)
			print("I2C address set to " + str(addr))

		# continuous polling command automatically polls the board
		elif usr_input.upper().startswith("POLL"):
			delaytime = float(string.split(usr_input, ',')[1])

			# check for polling time being too short, change it to the minimum timeout if too short
			if delaytime < atlas_sensors.long_timeout:
				print("Polling time is shorter than timeout, setting polling time to %0.2f" % atlas_sensors.long_timeout)
				delaytime = atlas_sensors.long_timeout

			# get the information of the board you're polling
			info = string.split(device.query("I"), ",")[1]
			print("Polling %s sensor every %0.2f seconds, press ctrl-c to stop polling" % (info, delaytime))

			try:
				while True:
					print(device.query("R"))
					time.sleep(delaytime - atlas_sensors.long_timeout)
			except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
				print("Continuous polling stopped")
		# if not a special keyword, pass commands straight to board
		else:
			if len(usr_input) == 0:
				print ("Please input valid command.")
			else:
				try:
					print(device.query(usr_input))
				except IOError:
					print("Query failed \n - Address may be invalid, use List_addr command to see available addresses")
		if num_sensors == 3:
                        num_sensors = 0     #reset to restart
			device.set_stop_flag(1) 		#Thread should stop now now since stop_flag = 1 
			print("Set stop flag to 1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! boi", device.get_stop_flag())

#This code (ie main loop) will only execute if we run this file as a program and it
#will not execute when someone wants to just import it as a module and call
#the functions available within the class atlas_sensors

#if __name__ == '__main__':
#	main()

