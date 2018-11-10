"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: SEAL
File: main.py
--------
Contains the main loop and uses classes and functions that run SEAL's rov. Including
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
        cmd_message = "0"           # Most current command message 
        control_ints = [0,0,0,0,0]  # Integer values of the motor elements [lt_xaxis, lt_yaxis, rt_xaxis, rt_yaxis, headlights] 
        control_elems = ["lt_xaxis","lt_yaxis","rt_xaxis","rt_yaxis","headlights"]  # Control elements for xml access
        error_byte = 0x00


        cmd_test = "C,0,0,0,0,0,0"           #  
        cmd_input = "y"
        cmd_list = [0,0,0,0,0,0,0]  # Init cmd_list
        

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

        # Initalize use of sensors.xml
        base_path1 = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
        xml_file1 = os.path.join(base_path1, "xml_sensors.xml")  # Join base_path with actual .xml file name
        tree1 = et.parse(xml_file1)                               # Save file into memory to work with its children/elements
        root1 = tree1.getroot()                                   # Returns root of the xml file to get access to all elements 
        root1.find("Errored_Sensor").text = "0"
        tree1.write(xml_file1) 

        # Open serial port communication
        ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
        ser.flushInput() # Flush serial port

        """
        Description While Loop:
        This while loop Rx/Tx to/from the tether and controls the operation
        of the ROV by calling on motor movement functions and sensor reading functions.
        """
        while end_expedition != True:
                
                # Get control data from serial port
                cmd_message = rov.read_serial_port(ser)         # Read from serial port

                # CRC Check here before we use the message
                        ####Fill this in here
                        ###If CRC is bad 
                                # Stabilize ROV and use "continue" keyword to start next loop of the while loop
                                    #### rov.stabilize_function 

                # Save the cmd data to the cmd.xml
                rov.parse_control_message(cmd_message)              # Write the cmd data to the cmd.xml
                cmd_id = root.find("id_char").text              # Save the ID char for program flow
               
                # Convert the str values to integers we can use for control.py
                for i, elem in enumerate(control_ints):
                        control_ints[i] = int(root.find(control_elems[i]).text)
                        
                # Print read results
                print("This is the control_message: ", cmd_message)


                # int(root.find("lt_xaxis").text)   # converts lt analog X axis to an integer for use in the motors class
                
                ##########
                # Control ROV command data
                if (cmd_id == "C"):
                        pass

                # Shutdown the ROV motors
                elif (cmd_id == "p"):
                        # Write 0 to all pts in the cmd_xml and then set motor speed
                        pass

                # End Expedition operation 
                elif (cmd_id == "f"):
                        pass
                else:
                        print("Error: Invalid command ID value")
                ##########



                # Write sensor data to serial port 
                rov.write_serial_port(ser, rov.send_sensor_data())

                # Controls if all meas or essential measurments are taken this is the user input from the cmd center
                cmd_input = input("Would you like to get all measurements? (y,n) ")

                # Set the sensor error byte to the rov class for error detection
                rov.set_error_byte(int(root1.find("Errored_Sensor").text))

                """ 
                # Alternative to writing the cmd message string to xml (IDK why I am trying to do that)
                cmd_list = cmd_test.split(",")               # Save each individual srting cmd into list cmd_list 

                # Check if data is recieved
                if len(cmd_list) != 1:
                # No data was received stabalize ROV and get essential measurements
                if len(cmd_list) == 1:
                        rov.get_essential_meas("1")     # Get pressure and temp. 1st input = salt/fresh water (1/0)
                                    #The '1' in the function parameter above should be changed based on what the user selects

                # Control Data is recieved
                else:
                """ 
                # End of expedition user input (need to change it to an interupt kind of function)
                if cmd_list[0] == "b" or cmd_input == "q":  # End Mission 
                        end_expedition = True
                else:
                        #####"""
                        if cmd_input == "y":
                                get_all_meas = True
                                print("get_all_meas pressed")
                                cmd_input = "y"
                        else:
                                get_all_meas = False
                                #####cmd_input = "y"

                        if cmd_input == "y":    # Get all measurments?
                                # Get essential meas here
                                rov.get_essential_meas("1")     # get pressure and temp. 1st input = salt/fresh water (1/0)

                                # Get pH, DO, and salinity measurments
                                atlas_sensor.set_stop_flag(0)           # 0 =go get atlas sensor meas
                                atlas_sensor.set_error_byte(error_byte) # Pass the sensor errors to the sensor class

                        else:   # Get essential measurements only 
                                #### atlas_sensor.set_stop_flag(1) # 1 = do NOT get atlas sensor meas
                                                    #### May not need to tell it explicitely to not go get atlas sensor measurements
                                rov.get_essential_meas("1")     # Get pressure and temp. 1st input = salt/fresh water (1/0)

                                """

                                #####print("This is the x Button value: ", cmd_list[6])
                                # Take Sensor Measurements
                                if cmd_list[6] == "1":    # Get all measurments?
                                        # Get essential meas here
                                        rov.get_essential_meas("1")     # get pressure and temp. 1st input = salt/fresh water (1/0)

                                        # Get pH, DO, and salinity measurments
                                        atlas_sensor.set_stop_flag(0) # 0 =go get atlas sensor meas

                                else:   # Get essential measurements only 
                                        ######atlas_sensor.set_stop_flag(1) # 1 = do NOT get atlas sensor meas
                                                    #### May not need to tell it explicitely to not go get atlas sensor measurements
                                        rov.get_essential_meas("1")     # Get pressure and temp. 1st input = salt/fresh water (1/0)

                                """


                """End While Loop"""
        # Shut down sensor thread before terminating the program
        atlas_sensor.terminate_thread()
        print("GOODBYE!")

        return 0 # End main() Definition # 


# Runs the main just defined above
main()


