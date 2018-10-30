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


# Import code modules
import rov_skeleton # Module provides access to all of the fns with our class 'rov'
from threading import Thread
import time
import serial
import os 
import xml.etree.ElementTree as et
#import sensors	# Module provides all of the sensor classes 

# Global variables
# global my_var = 100 


"""
The main loop will control all of the operations of the ROV
Parameters:

Return:
	0 on success, error code on failure
Notes:
	Initialized all sensor address data before main while loop 
"""
def main():
        # Define some variables used within main
        end_expedition = False 	# Variable to end program's main
        cmd_id = "0" 	            # Command ID stored as decimal number in python
        cmd_input = "y"
        test_init_input = "z,kval10,H2oSalt;"                        # Sample init input from cmd center
        cmd_message = ""            # Init to zero 

        # Initialize class objects and instances. (Also inits 2 xml files with default vals)
        rov = rov_skeleton.rov()		            # init rov class/module instance
        atlas_sensor = rov_skeleton.sensors.atlas_sensors() # Initialize atlas sensor class/module instance

        # Create atlas sensor thread
        atlas_sensor_thread = Thread(target=atlas_sensor.run)
        atlas_sensor_thread.daemon = True       # Used to stop the thread once main finishes

        # Start Sensor thread
        atlas_sensor_thread.start()

        # Buttons that can be set via command center
        stop_motors = False
        get_all_meas = False

        # Initalize use of commands.xml
        base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
        xml_file = os.path.join(base_path, "xml_commands.xml")  # Join base_path with actual .xml file name
        tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
        root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

        # Open serial port communication
        ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)        # (physical port, baudrate, timeout interval)


        """
        Description While Loop:
        The while loop does what?? Oh that is right, EVERYTHING!
        """
        while end_expedition != True:
                # Everything goes here

                # Get control data from serial port
                rov.write_serial_port(ser, test_init_input)     # Write to serial port
                cmd_message = rov.read_serial_port(ser)         # Read from serial port
                rov.write_cmd_xml(cmd_message)                  # Write the cmd data to the cmd.xml

                # Print read results
                print("This is the control_message: ", cmd_message)

                # Write sensor data to serial port 
                ########    write_serial_port()
                rov.write_serial_port(ser, rov.send_sensor_data())

                # Controls if all meas or essential measurments are taken this is the user input from the cmd center
                cmd_input = input("Would you like to get all measurements? (y,n) ")

                
                # End of expedition user input (need to change it to an interupt kind of function)
                if cmd_input == "quit" or cmd_input == "q": 
                        end_expedition = True
                else:
                        if cmd_input == "y":
                                get_all_meas = True
                                print("get_all_meas pressed")
                                cmd_input = "n"
                        else:
                                get_all_meas = False
                                print("get_all_meas NOT pressed")


                        # Take Sensor Measurements
                        if get_all_meas == True:
                                # Get essential meas here
                                rov.get_essential_meas("1")     # Get pressure and temp. tuple 1st input = salt/fresh water (1/0)

                                # Get pH, DO, and salinity measurments
                                atlas_sensor.set_stop_flag(0) # 0 =go get atlas sensor meas

                        else:   # Get only temp, pressure, accel, and gyro meas
                                # Get essential meas here
                                atlas_sensor.set_stop_flag(1) # 1 = do NOT get atlas sensor meas
                                rov.get_essential_meas("1")     # Get pressure and temp. tuple 1st input = salt/fresh water (1/0)

                        #end_expedition = input("End expedition(y=1, n=0)? ")
                        #end_expedition = 1 # Exits the while loop when we get specific cmd from user
                        #break; # This also exits the while loop if some condition is met
                                
                """End While Loop"""
        # Shut down sensor thread before terminating the program
        atlas_sensor.terminate_thread()
        print("GOODBYE!")

        return 0 # End main() Definition # 


# Runs the main just defined above
main()
