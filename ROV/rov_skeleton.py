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

import os   # Module used to find the file directory path for reading and writing to .xml
import xml.etree.ElementTree as et  # Module provides .xml file manipulation and functions

# Global variables
#global my_var                """Example if absolutely needed ONLY"""
#my_var = 34 

class rov:
        default_sensor_xml = "xml_sensors.xml"   
        default_command_xml = "xml_commands.xml"   

        
        """
        Initilizes the .xml files with values of zeros since this is only called 
        upon once at startup of the ROV.
        Parameters:
                sensors.xml file name as string, commands.xml file name as string
        Return:
                None 
        Notes:
                ROV class initilization function called upon when ROV object is created.
        """
        def __init__(default_arg, sensor_xml_file=default_sensor_xml, command_xml_file=default_command_xml):
                # Initilize all values in commands.xml to defaults (0)
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, command_xml_file)     # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 
                
                root.find("id_char").text = "0"         # C=control, p=stop motors, f=end mission, z=initialize probes
                root.find("lt_xaxis").text = "0"        # -32000-32000
                root.find("lt_yaxis").text = "0"        # -32000-32000
                root.find("rt_xaxis").text = "0"        # -32000-32000
                root.find("rt_yaxis").text = "0"        # -32000-32000
                root.find("a_button").text = "0"        # Pressed("1") or not pressed("0")
                root.find("x_button").text = "0"        # Pressed("1") or not pressed("0")
                root.find("k_value").text = "10"        # Our probe is 10
                root.find("water_type").text = "salt"   # fresh or salt 

                tree.write(xml_file)    # Saves all changes to the commands.xml on the SD card

                # Initilize all values in sensors.xml to defaults (0)
                base_path1 = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file1 = os.path.join(base_path1, sensor_xml_file)     # Join base_path with actual .xml file name
                tree1 = et.parse(xml_file1)                               # Save file into memory to work with its children/elements
                root1 = tree1.getroot()                                   # Returns root of the xml file to get access to all elements 

                root1.find("id_char").text = "S"         # S=sensor packet 
                root1.find("Temperature").text = "Temperature"
                root1.find("Pressure").text = "Pressure"
                root1.find("pH").text = "pHval"
                root1.find("Salinity").text = "Salinity"
                root1.find("Dissolved_Oxygen").text = "DOxy"
                root1.find("Errored_Sensor").text = " "
                root1.find("Gyroscope1").text = "1"
                root1.find("Gyroscope2").text = "2"
                root1.find("Gyroscope3").text = "3"
                root1.find("Accelerometer1").text = "999"
                root1.find("Accelerometer2").text = "99"
                root1.find("Accelerometer3").text = "9"

                tree1.write(xml_file1)    # Saves all changes to the sensors.xml on the SD card
                return



        """
        Reads a specific element from the commands.xml file for motor/ROV control
        Parameters:
                Select a specific command center element to read 
        Return:
                Returns string to use for ROV control 
        Notes:
        """
        def read_command_xml(default_arg, cmd_element):
                # Read from command xml at specific point so I
                #may need more function input parameters

                # Open command.xml for reading
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_commands.xml")  # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                # Use cmd_element parameter to grab specific element inside command.xml for motor control 
                #SEE above comment 
                command_str = root.find(cmd_element).text

                return command_str


        """
        Sends sensor data. Opens sensor.xml and combines all data into a comma delineated string 
        and sends through serial port by calling write_serial_port()
        Parameters:
               None 
        Return:
               None 
        Notes:
        """
        def send_sensor_data(default_arg):
                # Open sensor.xml read from and concatenate all sensor data into string close sensor.xml
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_sensors.xml")   # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                # create sensor string from sensors.xml 
                sensor_str= (root.find("id_char").text + "," + root.find("pH").text + "," + root.find("Dissolved_Oxygen").text + "," +
                            root.find("Salinity").text + "," + root.find("Temperature").text + "," + root.find("Pressure").text + "," +
                            root.find("Gyroscope1").text + "," + root.find("Accelerometer1").text + "," + root.find("Errored_Sensor").text + ":") 

                # Write the string we just created to serial port
                write_serial_port(sensor_str) 
                return



        """
        Limits the number of significant figures (chars) that each sensor data string can take
        up in the sensor data string.
        Parameters:
                What parameters do I need? 
        Return:
                Do i return anything at all or just re-write to sensor.xml???
        Notes:
        """
        def sig_fig_sensor_data(default_arg):
                # Open sensor.xml read from and concatenate all sensor data into string close sensor.xml
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_sensors.xml")   # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                # Create sensor string from sensor.xml 
                sensor_str= (root.find("Temperature").text + root.find("Pressure").text + root.find("pH").text + 
                        root.find("Salinity").text + root.find("Dissolved_Oxygen").text + root.find("Errored_Sensor").text + ":") 
                # Write the string we just created to serial port
                write_serial_port(sensor_str) 
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
                # Get Pressure measurement and write it to sensors.xml
                depth = get_pressure(water_choice)
                write_xml("0", "Pressure", str(depth))

                # Get Temperature measurement and write it to sensors.xml
                c_temp = get_temperature()
                write_xml("0", "Temperature", str(c_temp))

                # Get Gyroscope measurement and write it to sensors.xml
                #write_xml("0", "Gyroscope1", gyro1)
                #write_xml("0", "Gyroscope2", gyro2)
                #write_xml("0", "Gyroscope3", gyro3)

                # Get Accelerometer measurement and write it to sensors.xml
                #write_xml("0", "Accelerometer1", accel1)
                #write_xml("0", "Accelerometer2", accel2)
                #write_xml("0", "Accelerometer3", accel3)
                return 



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



############################################################
################ ROV Class Helper functions#################
############################################################


"""
Obtain string commands from cmd center.
Parameters:
        None
Return:
        Returns full message from cmd center as a string with a terminating ':' 
Notes:
"""
def read_serial_port():
        # Open and read from serial port and save in cmd_message variable
        #cmd_message = readUART_LINE_SOMETHING_like_this()
        
        return cmd_message



"""
Sends sensor array data to the command center terminated by a ':' 
Called only by send_sensor_string() a part of the rov class. 
Parameters:
        Sensor array string terminated by ':'  
Return:
        None
Notes:
"""
def write_serial_port(sensor_str):
        # Open and write sensor_str to serial port

        # This is the sensor string I am getting
        print("This is the sensor string I am getting: ", sensor_str)

        return



"""
Writes individual string data to a single element in the chosen xml file.
Parameters:
        Select the xml to open, the element in the xml to overwrite, string to write to xml 
Return:
        None 
Notes:
"""
def write_xml(xml_choice, xml_element, string_data):
        # Write to command.xml
        if xml_choice == "1":
                # Open command.xml for reading
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_commands.xml")  # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 
                
                # Write the new data to the element chosen
                root.find(xml_element).text = string_data
                tree.write(xml_file)    # Saves all changes to the command.xml

        # Write to sensor.xml
        elif xml_choice == "0":
                # Open command.xml for reading
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_sensors.xml")   # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                # Write the new data to the element chosen
                root.find(xml_element).text = string_data
                tree.write(xml_file)    # Saves all changes to the sensor.xml
        else:
                print("Error in write_xml() function of rov_skelton no xml was written to.")

        return



"""
Obtains a single pressure measurement from sensor
Called only by get_essential_meas() part of rov class.
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
                depth = sensor.pressure(ms5837.UNITS_psi)           # Get presure in psi
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
Called only by get_essential_meas() part of rov class.
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

        num_sensors = 0                #Must get one reading for each sensor

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
# """






