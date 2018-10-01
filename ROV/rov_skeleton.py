"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: SEAL
File: rov_skeleton.py
--------
Will contain the rov class and functions that run SEAL's rov. Including movement, 
sensor readings, and communication to SEAL's cmd center.
"""

# Import python/sensor modules
import sys        # Module provides access to fns maintained by the interpreter
import os        # Module provides fns allowing one to use OS dependent functionality
import time        # Module provides SW delay functionality

import sensors        # Module provides all functions for the atlas sensor
import ms5837   # Module provides all functions for the pressure sensor
import tsys01   # Module provides all functions for the temperature sensor

# Global variables
#global my_var                """Example if absolutely needed ONLY"""
#my_var = 34 

class rov:
        #########################################################################3
        """
        The main loop will control all of the operations of the ROV
        Parameters:

        Return:
                0 on success, error code on failure
        Notes:
                Initialized all sensor address data before main while loop 
        def main():
                # Define some variables used within main
                end_expedition = 0

                #Or here both work

                #Initialize I2C bus slave addresses explicitly to default values
                ###Set parameters that hold the slave addresses in Hex

                Description While Loop:
                The while loop does what?? Oh that is right, EVERYTHING!
                ""
                while end_expedition != 1:
                        #Everything goes here


                        #end_expedition = 1 #Exits the while loop when we get specific cmd from user
                        #break; #This also exits the while loop if some condition is met

                        ###End While Loop###


                return #End main() Definition#
        """
        #########################################################################3

        """TEST function"""
        def test_function(default_arg):
                print("You are inside the test function available through the rov class.")
                return





        """
        Obtain string commands from cmd center.
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def read_serial_port(default_arg):

                return



        """
        Obtain string commands from cmd center.
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def write_serial_port(default_arg):

                return


        """
        Opens .xml and reads from it
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def read_xml(default_arg):
                # open .xml read what i want and close .xml
                return



        """
        Opens .xml and writes to it
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def write_xml(default_arg):
                # open.xml write to it and close .xml
                return



        """
        Parses data received from serial port and writes it to .xml
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def parse_control_data(default_arg):
                # parse the data string from buffer then write each piece to .xml

                # write_xml()        # writes to control.xml values of each control data pt.
                return



        """
        Sends sensor data. Opens sensor.xml and combines into a string packet and sends through serial port
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def send_sensor_data(default_arg):
                # Open sensor.xml concatenate all sensor data into string close sensor.xml

                # write_serial_port() # Write the string we just created to serial port
                return



        """
        Uses control.xml values to calculate PWM (dir & spd) of selected motor
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def calc_motor_spd(default_arg):
                # Open control.xml read selected value, calc PWM write it into .xml and close xml
                return



        """
        Uses control.xml values to send PWM value to motor for driving
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def set_motor_spd(default_arg):
                # Open control.xml read selected vals & write to ESC channel(s) via I2C bus close .xml

                return



        """
        Obtains temp, pressure, accelerometer, and gyroscope measurements
        Parameters:
                Water density chioce (salt/fresh watter) as string,
        Return:
                Do we return any value?
        Notes:
        """
        def get_essential_meas(default_arg, water_choice):
                # Open sensor.xml, obtain sensor measurements, write to sensor.xml and close

                
                # Get Pressure measurement
                depth = get_pressure(water_choice)

                # Get Temperature measurement
                c_temp = get_temperature()

                # Create tuple to hold all the values that will be passed back to main
                essential_meas = (depth, c_temp)


                # write_xml()        # writes to sensor.xml value of obtained sensor meas
                return essential_meas



        """
        Obtains essential measurements(temp, pres., and accel/gyro) and
        Dissolved Oxy, pH, and Salinity
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def get_all_meas(default_arg):
                # Open sensor.xml, obtain all sensor meas, write to sensor.xml and close 
                # get_essential_meas()
                
                # Get pH, DO and Salinity measurments with the compensation values
                #       get_ph_do_sal()

                # write_xml()        # writes to sensor.xml value of obtained sensor meas
                return



        """
        Attempts to stabilize rov via accelerometer and gyro if user sends to mvmt cmds
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def stabilize_rov(default_arg):
                # This one is gonna be a beach

                return


        # get each sensor data
        # parse input cmd or is this write_xml??

################ ROV Class Helper functions#################


"""
Obtains a single pH, DO and Salinity measurement from each sensor
and uses their respective compensation values such as temp and pressure
Parameters:
       Pressure (m), Temperature (C), and K value for salinity probe (0.1, 1.0, or 10) 
Return:
        Returns pH, DO, and Salinity as 
Notes:
"""
def get_ph_do_sal(pressure, temp, k_val="10"):

        device = sensors.atlas_sensors()         # creates the I2C port object, specify the address or bus if necessary

        # Initilize values used on atlas sensor measurements
        salinity = 0                        # Holds salinity measurement for DO sensor
        pressure_in_kpa = pressure * 10     # 1 meter of water = 10 kPa
        p_str = "P, " + pressure_in_kpa     # Default Pressure compensation value as string
        t_str = "T, 25.0"                   # Default temp compensation value as string

        num_sensors = 0                #Must do it once for each sensor

        #Get one DO, EC and pH sensor reading
        while num_sensors != 3:
                while device.get_stop_flag() == 1:
                        # do nothing
                        # If stop flag is 0 = go then do the below
                        time.sleep(1)
                        dummyinput = "dummy variable"

                try:
                        #Set i2c address to poll each sensor once: EC=100, DO=97, pH=99        
                        if num_sensors == 0:
                                device.set_i2c_address(100)
                                print("Testing EC probe...")
                                
                                k_str = "K," + k_val            # Create K value as a string
                                print(device.query(k_str))      # Set K value of Salinity measurement default 10
                                t_str = "T," + str(temp)        # Create temperature as a string
                                print(device.query(t_str))      # Set Temperature compensation value
                                print(device.query("R"))        # Get Salinity measurement
                                ######Must save salinity temp value for use below save in "salinity" variable

                        elif num_sensors == 1:
                                device.set_i2c_address(97)
                                print("Testing DO probe...")
                                print(device.query(p_str))      # Set Pressure compensation value 
                                print(device.query(t_str))      # Set Temperature compensation value 
                                ####print(device.query(salinity))   # Set salinity compensation value 
                                print(device.query("R"))        # Get DO measurement

                        else:
                                device.set_i2c_address(99)
                                print("Testing pH probe...")
                                print(device.query(t_str))      # Set Temperature compensation value
                                print(device.query("R"))        # Get pH measurement
                        
                except IOError:
                        print("Query failed \n - Address may be invalid, use List_addr command to see available addresses")
                
                #Increment to test the next sensor
                num_sensors += 1

                if num_sensors == 3:
                        num_sensors = 0             #Reset this variable to restart upon new user input
                        device.set_stop_flag(1)     #Thread should stop now now since stop_flag = 1 


"""
Obtains a single pressure measurement from sensor
Parameters:
        Water density chioce (salt/fresh watter) as string,
Return:
        Returns Depth as float in meters, Prints Temp. as float in Celsius
Notes:
"""
def get_pressure(water_choice):

        # Create sensor object
        sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

        # Must initialize pressure sensor before reading it
        if not sensor.init():
                print("Error initializing pressure sensor.")            # Print not needed in final version
                exit(1)

        # Poll readings
        #while True:
        #water_choice = '0'
        #water_choice = input("Fresh/Saltwater (0/1)? ")

        # Freshwater vs Saltwater depth measurements set via user input form cmd center
        if water_choice == '0':
                # Freshwater
                sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
                freshwaterDepth = sensor.depth() # default is freshwater
                water_choice = '1'
        elif water_choice == '1':
                # Saltwater
                sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
                freshwaterDepth = sensor.depth() # default is freshwater
                water_choice = '0'
        else:
                print("Error on water density choice.")         # Print not needed in final version

        if sensor.read():
                depth = sensor.depth()
                print("P: %0.4f m \t T: %0.2f C  %0.2f F\n" % (         # Print not needed in final version
                depth,      # Sensor depth, either fresh or salf water depending on above
                sensor.temperature(), # Default is degrees C (no arguments)
                sensor.temperature(ms5837.UNITS_Farenheit))) # Request Farenheit
        else:
                print ("Error reading pressure sensor.")            # Print not needed in final version
                exit(1)
        return depth


"""
Obtains a single temperature measurement from sensor
Parameters:
       none 
Return:
        Returns temperature as float in Celcius 
Notes:
"""
def get_temperature():

        # Create sensor object
        sensor = tsys01.TSYS01()

        # Must initilize temp sensor object
        if not sensor.init():
            print("Error initializing temperature sensor.")         # Print not needed in final version
            exit(1)

        # Read temp sensor once and save in c_temp variable
        if not sensor.read():
            print("Error reading temperature sensor.")          # Print not needed in final version
            exit(1)
        c_temp = sensor.temperature()                           # Get celcius temp
        f_temp = sensor.temperature(tsys01.UNITS_Farenheit)     # Get farenheit temp
        print("T: %.2f C\t%.2f F" % (c_temp, f_temp))           # Print not needed in final version
        
        return c_temp 





