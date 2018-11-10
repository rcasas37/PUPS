"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: SEAL
File: main.py
--------
Contains the main loop and uses class instances and functions that run SEAL's rov. Including
movement, sensor readings, and communication to SEAL's cmd center.
"""

# Import code modules
import rov_skeleton             # Module provides access to all of the fns with our class 'rov'
from threading import Thread
import time
import serial
import os 
import xml.etree.ElementTree as et
import control
import pigpio

"""
The main program will control all of the operations of the ROV
Parameters:

Return:
	0 on success, error code on failure
Notes:
	Initialized all classes, variables, and files before main while loop execution 
"""
def main():
        # Define some variables used within main
        end_expedition = False 	    # Variable to end program's main
        cmd_id = "0" 	            # Command ID stored as decimal number in python
        cmd_message = "0"           # Most current command message 
        control_ints = [0,0,0,0,0]  # Integer values of the motor elements [lt_xaxis, lt_yaxis, rt_xaxis, rt_yaxis, headlights] 
        control_elems = ["lt_xaxis","lt_yaxis","rt_xaxis","rt_yaxis","headlights"]  # Control elements for xml access
        error_byte = 0x00           # Current error sensor data byte
        lt_xaxis = 0
        lt_yaxis = 1
        rt_xaxis = 2
        rt_yaxis = 3
        headlights = 4


        # Test variables
        cmd_test = "C,0,0,0,0,0,0"
        cmd_input = "y"
        cmd_list = [0,0,0,0,0,0,0]  # Init cmd_list
        

        # Initialize class objects and instances. (Also inits 2 xml files with default vals)
        rov = rov_skeleton.rov()		            # Init rov class instance
        pi = pigpio.pi()                                    # Init Raspberry Pi class instance
        rov_control = control.control(pi=pi)                # Init control class instance 
        atlas_sensor = rov_skeleton.sensors.atlas_sensors() # Init atlas sensor class instance

        # Create atlas sensor thread
        atlas_sensor_thread = Thread(target=atlas_sensor.run)
        atlas_sensor_thread.daemon = True       # Used to stop the thread once main finishes
        atlas_sensor_thread.start()

        # Initalize use of rov control instance by arming and initilizing motors and LEDs to defaults
        rov_control.arm()

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
                control_ints[lt_xaxis] = int(root.find(control_elems[lt_xaxis]).text)
                control_ints[lt_yaxis] = int(root.find(control_elems[lt_yaxis]).text)
                control_ints[rt_xaxis] = int(root.find(control_elems[rt_xaxis]).text)
                control_ints[rt_yaxis] = int(root.find(control_elems[rt_yaxis]).text)
                control_ints[headlights] = int(root.find(control_elems[headlights]).text)
                        
                # Print read results
                print("This is the control_message: ", cmd_message)


                # int(root.find("lt_xaxis").text)   # converts lt analog X axis to an integer for use in the motors class
                
                #######################################################
                # Control ROV command data
                if (cmd_id == "C"):
                        # Drive ROV 
                        rov_control.left_stick_control(control_ints[lt_xaxis, lt_yaxis])
                        rov_control.right_stick_control(control_ints[rt_xaxis, rt_yaxis])

                        # Set LEDs
                        rov_control.light_control(control_ints[headlights])

                        # Water Collection Control set at 40% speed 
                        rov_control.water_pump_control(40, int(root.find("a_button").txt))

                # Initalize ROV data
                if (cmd_id == "z"):
                        ##### Set water type and K value
                        pass

                # Shutdown the ROV motors
                elif (cmd_id == "p"):
                        # Write normalized 0's (4001) to each motor axis to shut down the motors
                        rov_control.left_stick_control(control_ints[lt_xaxis, lt_yaxis])
                        rov_control.right_stick_control(control_ints[rt_xaxis, rt_yaxis])

                        # Water Collection Control Off (0)  
                        rov_control.water_pump_control(40, 0)

                # End Expedition operation 
                elif (cmd_id == "f"):
                        # Drive ROV 
                        rov_control.left_stick_control(control_ints[lt_xaxis, lt_yaxis])
                        rov_control.right_stick_control(control_ints[rt_xaxis, rt_yaxis])

                        # Set LEDs
                        rov_control.light_control(control_ints[headlights])
                        
                        ### If pressure == 2ft ish then set end expedition to true to quit while loop
                                ####end_expedition = True 
                else:
                        print("Error: Invalid command ID value")


                # Set the sensor error byte to the rov class for error detection
                rov.set_error_byte(int(root1.find("Errored_Sensor").text))

                # Get Sensor Measurements
                if ((root.find("x_button").text) == "1"): # Get all measurements pressed
                        # Get essential meas 
                        rov.get_essential_meas("1")     # get pressure and temp. input = salt/fresh water (1/0)

                        # Get pH, DO, and salinity measurments
                        atlas_sensor.set_stop_flag(0)           # 0 =go get atlas sensor meas
                        atlas_sensor.set_error_byte(error_byte) # Pass the sensor errors to the sensor class

                else:                                   # Get essential measurements
                        rov.get_essential_meas("1")     # Get pressure and temp. input = salt/fresh water (1/0)
                        ####atlas_sensor.set_error_byte(error_byte) # Pass the sensor errors to the sensor class

                #######################################################


                # Write sensor data to serial port 
                rov.write_serial_port(ser, rov.send_sensor_data())

                # Controls if all meas or essential measurments are taken this is the user input from the cmd center
                #######cmd_input = input("Would you like to get all measurements? (y,n) ")


                """
                # End of expedition user input (need to change it to an interupt kind of function)
                if cmd_list[0] == "f" or cmd_input == "q":  # End Mission 
                        end_expedition = True
                else:
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


                """End While Loop"""

        # Turns off all motors and LEDs 
        rov_control.disarm()

        # Shut down sensor thread before terminating the program
        atlas_sensor.terminate_thread()
        print("GOODBYE!")

        return 0 # End main() Definition 


# Runs the main defined above
main()


