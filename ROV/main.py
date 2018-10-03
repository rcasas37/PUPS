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
#import sensors	# Module provides all of the sensor classes 
#import test  # NOT A real import. Delete after done


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
        usr_input = 0


        # Initialize I2C bus slave addresses explicitly to default values ### Set parameters that hold the slave addresses in Hex or decimal??

        # Initialize class objects and instances 
        rov = rov_skeleton.rov()		# Init rov class/module instance
        atlas_sensor = rov_skeleton.sensors.atlas_sensors()     # Initialize atlas sensor class/module instance

        # Create atlas sensor thread
        atlas_sensor_thread = Thread(target=atlas_sensor.run)
        atlas_sensor_thread.daemon = True       # Used to stop the thread once main finishes

        # Start Sensor thread
        atlas_sensor_thread.start()

        # Buttons that can be set via command center
        stop_motors = False
        get_all_meas = False

        # Other Essential variables
        cmd_id = 0x00 	# Command ID stored as decimal number in python
        get_essential_meas = True # This guy should always be true might not even need var for him	


        # Open serial port communication


        # Create sensor and command .xml files for data storage

        user_input = "y"

        """
        Description While Loop:
        The while loop does what?? Oh that is right, EVERYTHING!
        """
        while end_expedition != True:
                # Everything goes here

                # Get control data from serial port
                        # get control data here 


                # Controls if all meas or essential measurments are taken this is the user input from the cmd center
                user_input = input("Would you like to get all measurements? (y,n) ")
                
                # End of expedition user input (need to change it to an interupt kind of function)
                if user_input == "quit": 
                        end_expedition = True
                else:
                        if user_input == "y":
                                get_all_meas = True
                                print("get_all_meas pressed")
                                user_input = "n"
                        else:
                                get_all_meas = False
                                print("get_all_meas NOT pressed")


                        # Take Sensor Measurements
                        if get_all_meas == True:
                                # Get essential meas here
                                rov.get_essential_meas("1")     # Get pressure and temp. tuple 1st input = salt/fresh water (1/0)
                                #####depth, c_temp = rov.get_essential_meas("1")     # Get pressure and temp. 1st input = salt/fresh water (1/0)

                                # Get pH, DO, and salinity measurments
                                atlas_sensor.set_stop_flag(0) # 0 =go get sensor meas

                        else:   # Get only temp, pressure, accel, and gyro meas
                                # Get essential meas here
                                atlas_sensor.set_stop_flag(1) # 1 = do NOT get sensor meas
                                ####depth, c_temp = rov.get_essential_meas("1")     # Get pressure and temp. 1st input = salt/fresh water (1/0)
                                rov.get_essential_meas("1")     # Get pressure and temp. tuple 1st input = salt/fresh water (1/0)

                        # Always get essential meas 
                        #essential_meas = rov.get_essential_meas("1")     # Get pressure and temp. tuple 1st input = salt/fresh water (1/0)
                        #rov.get_essential_meas("1")     # Get pressure and temp. tuple 1st input = salt/fresh water (1/0)
                        #depth, c_temp = essential_meas      # Unpack tuple 
                        #print("These are the tuples: %.4f m and %.2f C" % (depth, c_temp))      # Print tuple to verify we get it


                        #end_expedition = input("End expedition(y=1, n=0)? ")
                        #end_expedition = 1 # Exits the while loop when we get specific cmd from user
                        #break; # This also exits the while loop if some condition is met

                                
                        """End While Loop"""
        # Shut down sensor thread before terminating the program
        atlas_sensor.terminate_thread()
        print("GOODBYE!")

        # return 0 # End main() Definition # 


# Runs the main just defined above
main()
