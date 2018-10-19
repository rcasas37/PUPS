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
import rov_skeleton             # Module provides access to all of the fns with our class 'rov'
from threading import Thread
import time
import serial
import os 
import xml.etree.ElementTree as et

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
        cmd_message = ""            # Init to none 

        # Initialize class objects and instances. (Also inits 2 xml files with default vals)
        rov = rov_skeleton.rov()		            # init rov class/module instance
        atlas_sensor = rov_skeleton.sensors.atlas_sensors() # Initialize atlas sensor class/module instance

        # Create atlas sensor thread
        atlas_sensor_thread = Thread(target=atlas_sensor.run)
        atlas_sensor_thread.daemon = True       # Used to stop the thread once main finishes
        atlas_sensor_thread.start()

        # Initalize use of commands.xml
        base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
        xml_file = os.path.join(base_path, "xml_commands.xml")  # Join base_path with actual .xml file name
        tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
        root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

        # Open serial port communication
        ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

        """
        Description While Loop:
        The while loop does what?? Oh that is right, EVERYTHING!
        """
        while end_expedition != True:
                # Everything goes here
                
                ser.flushInput() # Flush serial port

                # Get control data from serial port
                cmd_message = rov.read_serial_port(ser)         # Read from serial port
                ####rov.write_cmd_xml(cmd_message)              # Write the cmd data to the cmd.xml
                cmd_id = root.find("id_char").text              # Save the ID char for program flow

                # Alternative to writing the cmd message string to xml (IDK why I am trying to do that)
                ##cmd_list = cmd_message.split(",")               # Save each individual srting cmd into list cmd_list 

                # Print read results
                print("This is the control_message: ", cmd_message)

                ######ser.flushInput() # Flush serial port
                #time.sleep(.1)
                # Write sensor data to serial port 
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
                                #####print("get_all_meas NOT pressed")


                        # Take Sensor Measurements
                        if get_all_meas == True:
                                # Get essential meas here
                                rov.get_essential_meas("1")     # get pressure and temp. 1st input = salt/fresh water (1/0)

                                # Get pH, DO, and salinity measurments
                                atlas_sensor.set_stop_flag(0) # 0 =go get atlas sensor meas

                        else:   # Get only temp, pressure, accel, and gyro meas
                                # Get essential meas here
                                atlas_sensor.set_stop_flag(1) # 1 = do NOT get atlas sensor meas
                                rov.get_essential_meas("1")     # Get pressure and temp. 1st input = salt/fresh water (1/0)


                """
                # End of expedition user input (need to change it to an interupt kind of function)
                if cmd_id == "quit" or cmd_id == "f": 
                        end_expedition = True
                        # Go to an End Expedition function

                elif cmd_id == "C":
                        # Motor control here
                        dummy = "dummy"

                elif cmd_id == "p":
                        # Stop motors here
                        dummy = "dummy"

                else:
                        print("Error. Not Recognized cmd_id.")

                # Take Sensor Measurements either all or just essential
                if root.find("x_button").text == "1":
                        print("get_all_meas pressed")

                        # Get pH, DO, and salinity measurments
                        atlas_sensor.set_stop_flag(0) # 0 =go get atlas sensor meas

                else:
                        ####depth, c_temp = rov.get_essential_meas("1")     # Get pressure and temp. 1st input = salt/fresh water (1/0)
                        rov.get_essential_meas("1")     # Get pressure and temp. tuple 1st input = salt/fresh water (1/0)

                # Get essential meas every time
                print("get_essential_meas here: ")
                rov.get_essential_meas("1")     # Get pressure and temp. tuple 1st input = salt/fresh water (1/0)



                """


                """End While Loop"""
        # Shut down sensor thread before terminating the program
        atlas_sensor.terminate_thread()
        print("GOODBYE!")

        return 0 # End main() Definition # 


# Runs the main just defined above
main()

"""
Parameters:
        None
Return:
        None
Notes:
"""
def get_control_data(self):
        cmd_list = cmd_str.split(",")           # Get list of each individual cmd from cmd center
        i = 0
        length = len(cmd_list)
        print("Length of cmd_list: %d" % len(cmd_list))
        if (length != 0 and length <= 9):
                for cmd in cmd_list:                    # Write each individual element at a time to the command.xml
                        write_xml("1", self.cmd_xml_elem[i], cmd)
                        i += 1
        else:
                print("command message is not greater than 1 or larger than 9")
        return
