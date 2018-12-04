#!/usr/bin/python
"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: Atlas Scientific. Edits by: Landon Ledbetter
File: sensor.py
--------
Contains the atlas sensor class and functions that are use to 
take sensor readings within the ROV this is run as a separate thread
since the disolved oxygen, pH, and conductivity probes take approximately 3
seconds to poll once.
"""

import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps
import string     # helps parse strings

import threading  # used for creating atlas_sensor thread

import xml.etree.ElementTree as et # For writing to xml file
import os


# Global Variables
stop_flag = 1           # stop=1 and run=0 controls when atlas sensor thread gets a measurement controlled by main.py
kval = "10"             # Our probe is k10
pres_comp_val = "101"   # Pres. compensation value is in kpa
temp_comp_val = "25"    # Temp. compensation value is in Celsius

class atlas_sensors(threading.Thread):
        long_timeout = 1.5                  # the timeout needed to query readings and calibrations
        short_timeout = .5                  # timeout for regular commands
        default_bus = 1                     # the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
        default_address = 97                # the default address for the sensor
        current_addr = default_address

        def __init__(self, address=default_address, bus=default_bus):
                # open two file streams, one for reading and one for writing
                # the specific I2C channel is selected with bus
                # it is usually 1, except for older revisions where its 0
                # wb and rb indicate binary read and write
                self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
                self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

                # initializes I2C to either a user specified or default address
                self.set_i2c_address(address)
                
                # sets state of thread and inits all global variables
                self.running = True 
                global stop_flag
                stop_flag = 1
                global kval 
                kval = "10"
                global pres_comp_val 
                pres_comp_val = "101"
                global temp_comp_val 
                temp_comp_val = "25"
                super(atlas_sensors, self).__init__()
                self._stop_event = threading.Event()

        def terminate_thread(self):
                self._stop_event.set()

        def terminated(self):
                return self._stop_event.is_set()

        def run(self):
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
                unicode_cmd = cmd.encode()      # Added for python3 since .write does not take a string only a unicode byte
                self.file_write.write(unicode_cmd)

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

        # Set and get functions 
        def get_address(self):
                return self.default_address

        # Stop Flag
        def set_stop_flag(self, flag):
                global stop_flag 
                stop_flag = flag 

        def get_stop_flag(self):
                global stop_flag
                return stop_flag

        # Kval (as string)
        def set_kval(self, usr_kval):
                global kval
                kval = usr_kval

        def get_kval(self):
                global kval
                return kval

        # Pressure value (as float)
        def set_pres_comp(self, new_pres):
                global pres_comp_val
                pres_comp_val = new_pres
                
        def get_pres_comp(self):
                global pres_comp_val
                pres_in_kpa = 10 * pres_comp_val 
                return pres_in_kpa

        # temperature value (as float)
        def set_temp_comp(self, new_temp):
                global temp_comp_val
                temp_comp_val = new_temp

        def get_temp_comp(self):
                global temp_comp_val
                return temp_comp_val


def program():
        device = atlas_sensors()         # Creates the I2C port object, specify the address or bus if necessary
        try:
                # Initalize Conductivity Sensor
                device.set_i2c_address(100)
                device.query("O,EC,0")
                device.query("O,TDS,0")
                device.query("O,S,1")       # Only enable salinity output reading (PSU which is approx ppt)
                device.query("O,SG,0")
                if device.get_kval() == "0":
                        kval = "1"
                else:
                        kval = "10"
                device.query("K," + device.get_kval())        # Set default k parameter as 10
                device.query("T,23")        # Set default temp as 23C 
                
                # Initalize Dissolved Oxygen Sensor
                device.set_i2c_address(97)
                device.query("O,DO,1")      # Only enable mg/L output
                device.query("O,%,0")
                device.query("T,23")        # Set default temp as 23C 
                device.query("P,101")       # Set default pressure as 101kpa 

                # Initalize pH Sensor
                device.set_i2c_address(99)
                device.query("T,23")        # Set default temp as 23C 

        except:
                error = "Atlas Sensor Error: " 

        # Initalize access to the sensors.xml file
        base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
        xml_file = os.path.join(base_path, "xml_atlas.xml")   # Join base_path with actual .xml file name
        tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
        root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

        # For while loop
        usr_input = "R"
        num_sensors = 0     # Must do it once for each sensor
        salinity = 0        # Holds salinity measurement for DO sensor

        # Get one DO, EC and pH sensor reading
        while num_sensors != 3:
                while device.get_stop_flag() == 1:
                        # do nothing. If stop flag is 0 = go then do the below
                        time.sleep(1)
                        pass

                #Set i2c address to poll each sensor once: EC=100, DO=97, pH=99        
                if num_sensors == 0:
                        try:
                                device.set_i2c_address(100)
                                print("Testing EC probe...")

                                print(device.query("K," + str(device.get_kval())))      # Set K value of Salinity measurement default 10
                                print(device.query("T," + str(device.get_temp_comp()))) # Set Temperature compensation value 
                                ec_reading = (device.query("R")).split()                # Get Salinity measurement
                                print(ec_reading[2])
                                ######Must save salinity temp value for use below save in "salinity" variable
                                root.find("Salinity").text = ec_reading[2]
                        except:
                                # Return error value 
                                root.find("Salinity").text = "-1" 

                elif num_sensors == 1:
                        try:
                                device.set_i2c_address(97)
                                print("Testing DO probe...")

                                print(device.query("P," + str(device.get_pres_comp()))) # Set Pressure compensation value 
                                ####print(device.query(salinity))                       # Set salinity compensation value 
                                print(device.query("T," + str(device.get_temp_comp()))) # Set Temperature compensation value 
                                do_reading = (device.query("R")).split()                # Get DO measurement and split the command into a list to get the measurement as a string
                                print(do_reading[2])
                                root.find("Dissolved_Oxygen").text = do_reading[2]
                        except:
                                # Return error value 
                                root.find("Dissolved_Oxygen").text = "-1"
                else:
                        try:
                                device.set_i2c_address(99)
                                print("Testing pH probe...")

                                print(device.query("T," + str(device.get_temp_comp()))) # Set Temperature compensation value 
                                ph_reading = (device.query("R")).split()                # Get pH measurement
                                print(ph_reading[2])
                                root.find("pH").text = ph_reading[2]
                        except:
                                # Return error value 
                                root.find("pH").text = "-1" 
                
                try:
                        tree.write(xml_file)         # Saves all changes to the sensors.xml on the SD card
                except:
                        print("Error writing atlas sensors to xml")
                
                #Increment to test the next sensor
                num_sensors += 1

                if num_sensors == 3:
                        num_sensors = 0             #Reset this variable to restart upon new user input
                        device.set_stop_flag(1)     #Thread should stop now now since stop_flag = 1 

# End sensor.py file

