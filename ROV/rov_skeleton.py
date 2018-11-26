"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: SEAL
File: rov_skeleton.py
--------
Contains the rov class and functions that run SEAL's rov. Including movement, 
sensor readings, and communication to SEAL's cmd center.
"""

# Import python/sensor modules
import sys          # Module provides access to fns maintained by the interpreter
import os           # Module provides fns allowing one to use OS dependent functionality
import time         # Module provides SW delay functionality

import sensors      # Module provides all functions for the atlas sensor
import ms5837       # Module provides all functions for the pressure sensor
import tsys01       # Module provides all functions for the temperature sensor
import logging      # Module provides logging functions for BNO055
from Adafruit_BNO055 import BNO055  # Module provides all functions used to interface with the IMU

import serial
import os           # Module used to find the file directory path for reading and writing to .xml
import xml.etree.ElementTree as et  # Module provides .xml file manipulation and functions


class rov:
        default_sensor_xml = "xml_sensors.xml"   
        default_command_xml = "xml_commands.xml"   
        cmd_xml_elem = ["id_char", "lt_xaxis", "lt_yaxis", "rt_xaxis", "rt_yaxis", "a_button", "x_button", "k_value", "water_type"]

        """
        Initilizes the .xml files with values of zeros since this is only called 
        upon once at startup of the ROV, initalizes sensor objects for continues use with the rov class.
        Parameters:
                sensor_xml - Programmer can change the file to open and use if wanted
                command_xml - Programmer can change the file to open and use if wanted
        Return:
                None 
        Notes:
                ROV class initilization function called upon when ROV object is created.
        """
        def __init__(self, sensor_xml_file=default_sensor_xml, command_xml_file=default_command_xml):
                # Init imu, temp and pressure sensor objects
                self.bno = BNO055.BNO055(i2c=3, rst=18)         # Create bno object that uses bitbanged i2c line (3)

                # Initialize the BNO055 and stop if something went wrong.
                if not self.bno.begin():
                        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

                self.temp_sensor = tsys01.TSYS01()              # Create temperature object that uses standard i2c line (1) 
                self.pres_sensor = ms5837.MS5837_30BA()         # Create pressure object that uses standard i2c line (1) 

                # Initilize all values in commands.xml to defaults (0)
                self.base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                self.xml_file = os.path.join(self.base_path, command_xml_file)     # Join base_path with actual .xml file name
                self.tree = et.parse(self.xml_file)                               # Save file into memory to work with its children/elements
                self.root = self.tree.getroot()                                   # Returns root of the xml file to get access to all elements 
                
                self.root.find("id_char").text = "0"         # C=control, p=stop motors, f=end mission, z=initialize probes
                self.root.find("lt_xaxis").text = "0"        # -32000-32000
                self.root.find("lt_yaxis").text = "0"        # -32000-32000
                self.root.find("rt_xaxis").text = "0"        # -32000-32000
                self.root.find("rt_yaxis").text = "0"        # -32000-32000
                self.root.find("a_button").text = "0"        # Pressed("1") or not pressed("0")
                self.root.find("x_button").text = "0"        # Pressed("1") or not pressed("0")
                self.root.find("k_value").text = "10"        # Our probe is 10
                self.root.find("water_type").text = "salt"   # fresh or salt 

                self.tree.write(self.xml_file)    # Saves all changes to the commands.xml on the SD card

                # Initilize all values in sensors.xml to defaults (0)
                self.base_path1 = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                self.xml_file1 = os.path.join(self.base_path1, sensor_xml_file)     # Join base_path with actual .xml file name
                self.tree1 = et.parse(self.xml_file1)                               # Save file into memory to work with its children/elements
                self.root1 = self.tree1.getroot()                                   # Returns root of the xml file to get access to all elements 

                self.root1.find("id_char").text = "S"         # S=sensor packet 
                self.root1.find("Temperature").text = "Temperature"
                self.root1.find("Pressure").text = "Pressure"
                self.root1.find("pH").text = "pHval"
                self.root1.find("Salinity").text = "Salinity"
                self.root1.find("Dissolved_Oxygen").text = "DOxy"
                self.root1.find("Orientation").text = " " 
                self.root1.find("Errored_Sensor").text = " "

                self.tree1.write(self.xml_file1)    # Saves all changes to the sensors.xml on the SD card
                return



        """
        Reads a specific element from the commands.xml file for motor/ROV control
        Parameters:
                cmd_element - The element of interest within the xml 
        Return:
                command_str - The value from the xml of the element selected through cmd_element 
        Notes:
        """
        def read_command_xml(self, cmd_element):
                '''
                # Read from command xml at specific point so I
                #may need more function input parameters

                # Open command.xml for reading
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_commands.xml")  # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                # Use cmd_element parameter to grab specific element inside command.xml for motor control 
                #SEE above comment 
                '''
                command_str = root.find(cmd_element).text

                return command_str


        """
        Sends sensor data. Opens sensor.xml and combines all data into a comma delineated string 
        and returns the string ready to send over the serial port 
        Parameters:
               None 
        Return:
               sensor_str - the concatinated sensor string e.g.: "S,pH,DO,Sal,Temp,Presure,Gyro1,Accel1,Error_addr;" 
        Notes:
                Only used in conjunction with write_serial_port(), this function returns the string
                we want to write to the serial port
        """
        def send_sensor_data(self):
                '''
                # Open sensor.xml read from and concatenate all sensor data into string close sensor.xml
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_sensors.xml")   # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 
                '''
                # create sensor string from sensors.xml 
                sensor_str= (self.root1.find("id_char").text + "," + self.root1.find("pH").text + "," + self.root1.find("Dissolved_Oxygen").text + "," +
                            self.root1.find("Salinity").text + "," + self.root1.find("Temperature").text + "," + self.root1.find("Pressure").text + "," +
                            self.root1.find("Orientation").text + "," + self.root1.find("Errored_Sensor").text + ";") 

                return sensor_str



        """
        Limits the number of significant figures (chars) that each sensor data string can take
        up in the sensor data string.
        Parameters:
                What parameters do I need? 
        Return:
                Do i return anything at all or just re-write to sensor.xml???
        Notes:
        """
        def sig_fig_sensor_data(self):
                # Create sensor string from sensor.xml 
                sensor_str= (self.root1.find("Temperature").text + self.root1.find("Pressure").text + self.root1.find("pH").text + 
                        self.root1.find("Salinity").text + self.root1.find("Dissolved_Oxygen").text + self.root1.find("Errored_Sensor").text + ";") 
                return



        """
        Parses data received from serial port and writes it to .xml
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def parse_control_data(self):
                # parse the data string from buffer then write each piece to .xml

                # write_xml()        # writes to control.xml values of each control data pt.
                return



        """
        Obtains temp, pressure, and IMU (quaternions: x,y,z,w) measurements
        Parameters:
                water_choice - chosen by the user at startup
        Return:
                depth and orientation tuple 
        Notes:
        """
        def get_essential_meas(self, water_choice):
                # Get Pressure measurement and write it to sensors.xml
                #depth = self.get_pressure(water_choice)
                #write_xml("0", "Pressure", str(depth))
                #self.root1.find("Pressure").text = depth

                # Get Temperature measurement and write it to sensors.xml
                #c_temp = self.get_temperature()
                #write_xml("0", "Temperature", str(c_temp))
                #self.root1.find("Temperature").text = c_temp

                # Get IMU measurement and write it to sensors.xml
                roll,pitch = self.get_imu()
                
                # Use function here to determine "warning tilted at least +45deg n/s/e/w"
                orientation = self.check_orientation(roll,pitch)
                self.root1.find("Orientation").text = orientation[4]

                # Saves all changes to the sensors.xml on the SD card
                self.tree1.write(self.xml_file1)                    

                return orientation 


        """
        Checks the orientation of the ROV and returns a binary tuple of 4 values that represent north,
        south, east, and west. A 1 for any of the 4 values means that the rov is tilted past 45 degrees
        in that direction. This means that at most there should only ever be at most 2 values that are 1.
        This also writes the direction in which the ROV is tilting if any.
        Parameters:
                Roll - The angle tilted off of the x-axis
                Pitch - The angle tilted off of the y-axis
        Return:
                Return binary tuple of horizontal coordinate plane where 1 means it is tilted past threshold 
        Notes:
        """
        def check_orientation(self, roll, pitch):
                tilt_data = "" 
                # Default the orientations to OKAY (not tilted off of any axis by more than 45 degrees
                n = 0
                s = 0
                e = 0
                w = 0
                
                # Check if roll or pitch exceeds 45 degree threshold
                if roll < -45: e = 1
                elif roll > 45: w = 1

                if pitch < 45: s = 1
                elif pitch > 135: n = 1

                # Write the error string to the sensor xml
                if n == 1: tilt_data = "North"
                elif s == 1: tilt_data = "South"
                elif e == 1: tilt_data = "East"
                elif w == 1: tilt_data = "West"
                if n == 1 and e == 1: tilt_data = "Northeast"
                elif s == 1 and e == 1: tilt_data = "Southeast"
                elif n == 1 and w == 1: tilt_data = "Northwest"
                elif s == 1 and w == 1: tilt_data = "Northwest"
                
                print("Tilted past 45 degrees: ", tilt_data)

                return n,s,e,w,tilt_data



        """
        Attempts to stabilize rov via accelerometer and gyro if user sends to mvmt cmds
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def stabilize_rov(self):
                # This one is gonna be a beach

                return


        """
        Obtain string command packet from cmd center.
        Parameters:
                ser - The serial port object to read bytes of data
                size - Programmer can specify number of bytes to read
                eol - The end of the line character, read bytes terminator
        Return:
                line_str - A complete command center control packet terminated with ';' 
        Notes:
        """
        def read_serial_port(self, ser, size=None, eol=';'):
                # Open and read from serial port and save in cmd_message variable
                len_eol = len(eol)
                line_str = bytearray() 
                while True:
                        #ser.flushInput()        # Flush serial port
                        char = ser.read(1)      # Read 1 byte or 1 char
                        if char:
                                #print("charrrr::::::::::: ", char)
                                #if char.decode() != ";":    # Is the current char the terminating char? No then append it.
                                line_str += char    # Append a single char string to the line_str 
                                if line_str[-len_eol:] == eol:                  # Check if char is terminating character
                                        break
                                if size is not None and len(line_str) >= size:  # Check if message is exists in the buffer
                                        break
                        else:
                                #print("NO CHARACTER TO READ")
                                break
                return bytes(line_str) 


        """
        Pysically writes sensor array data to the tether to the command center terminated by a ';'  
        Parameters:
                ser - The serial port object to read bytes of data
                sensor_str - The sensor string we have to write to the tether
        Return:
                None
        Notes:
                Only used in conjunction with send_sensor_data() as the sensor_str input parameter
        """
        def write_serial_port(self, ser, sensor_str):
                # Open and write sensor_str to serial port
                sensor_encoded = sensor_str.encode()
                ser.write(sensor_encoded)

                # This is the sensor string I have
                ############print("This is the sensor string I have to send: ", sensor_str)

                return


        """
        Writes each command data to the command.xml for motor use
        Parameters:
                cmd_str - A single rov command that will be writen to the commands.xml
        Return:
                None
        Notes:
        """
        def write_cmd_xml(self, cmd_str):
                cmd_list = cmd_str.split(",")           # Get list of each individual cmd from cmd center
                i = 0
                length = len(cmd_list)
                print("Length of cmd_list: %d" % len(cmd_list))
                if (length != 0 and length <= 9):
                        for cmd in cmd_list:                    # Write each individual element at a time to the command.xml
                                #self.write_xml("1", self.cmd_xml_elem[i], cmd)
                                self.root.find(self.cmd_xml_elem[i]).text = cmd
                                i += 1
                else:
                        print("command message is not greater than 1 or larger than 9")
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
                try:
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
                except:
                        print("Error writing temp or press to XML.")

                return



        """
        Obtains a quaternion orientation packet "x,y,z,w" measurement from BNO055 sensor
        Called only by get_essential_meas() part of rov class.
        Parameters:
                None 
        Return:
                Returns tuple of quaternion data, 3 vectors and the rotation about the vector
        Notes:
        """
        def get_imu(self):
                try:
                        # Read the Euler angles for heading, roll, pitch (all in degrees).
                        heading, roll, pitch = self.bno.read_euler()

                        # Print everything out.
                        #print('H={0:0.2F} R={1:0.2F} P={2:0.2F}'.format(heading, roll, pitch))

                        # Orientation as a quaternion:
                        #x,y,z,w = self.bno.read_quaternion()
                        #print('x={0:0.3F} y={1:0.3F} z={2:0.3F} w={3}'.format(x, y, z, w))
                        
                except:
                        print("IMU sensor not read")
                        #return 0,0,0,0
                        return 0,0

                #return x,y,z,w
                return roll, pitch


        """
        Obtains a single pressure measurement from pressure sensor
        Called only by get_essential_meas() part of rov class.
        Parameters:
                Water density chioce (salt/fresh watter) as string,
        Return:
                Returns Depth as float in meters, Prints Temp. as float in Celsius
        Notes:
        """
        def get_pressure(self, water_choice):

                # Create sensor object
                #self.pres_sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

                # Must initialize pressure sensor before reading it
                if not self.pres_sensor.init():
                        print("Error initializing pressure sensor.")            # Print not needed in final version
                        exit(1)

                # Freshwater vs Saltwater depth measurements set via user input form cmd center
                if water_choice == "1":
                        # Saltwater
                        self.pres_sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
                        freshwaterDepth = self.pres_sensor.depth() # default is freshwater
                        water_choice = "0"
                elif water_choice == "0":
                        # Freshwater
                        self.pres_sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
                        freshwaterDepth = self.pres_sensor.depth() # default is freshwater
                        water_choice = "1"
                else:
                        print("Error on water density choice.")         # Print not needed in final version

                if self.pres_sensor.read():
                        depth = self.pres_sensor.pressure(ms5837.UNITS_psi)           # Get presure in psi
                        #####print("P: %0.4f m \t T: %0.2f C  %0.2f F\n" % (         # Print not needed in final version
                        ###depth,      # Sensor depth, either fresh or salf water depending on above
                        ###sensor.temperature(), # Default is degrees C (no arguments)
                        ###sensor.temperature(ms5837.UNITS_Farenheit))) # Request Farenheit
                else:
                        print ("Error reading pressure sensor.")            # Print not needed in final version
                        exit(1)
                return depth



        """
        Obtains a single temperature measurement from termperature sensor
        Called only by get_essential_meas() part of rov class.
        Parameters:
                None 
        Return:
                Returns temperature as float in Celcius 
        Notes:
        """
        def get_temperature(self):
                # Create sensor object
                #self.temp_sensor = tsys01.TSYS01()

                # Must initilize temp sensor object
                if not self.temp_sensor.init():
                    print("Error initializing temperature sensor.")         # Print not needed in final version
                    exit(1)

                # Read temp sensor once and save in c_temp variable
                if not self.temp_sensor.read():
                    print("Error reading temperature sensor.")          # Print not needed in final version
                    exit(1)
                
                c_temp = self.temp_sensor.temperature()                           # Get celcius temp
                #####f_temp = sensor.temperature(tsys01.UNITS_Farenheit)     # Get farenheit temp
                ######print("T: %.2f C\t%.2f F" % (c_temp, f_temp))           # Print not needed in final version
                
                return c_temp 




############################################################
################ ROV Class Helper functions#################
############################################################


"""
Obtains a single pressure measurement from pressure sensor
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
        if water_choice == "1":
                # Saltwater
                sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
                freshwaterDepth = sensor.depth() # default is freshwater
                water_choice = "0"
        elif water_choice == "0":
                # Freshwater
                sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
                freshwaterDepth = sensor.depth() # default is freshwater
                water_choice = "1"
        else:
                print("Error on water density choice.")         # Print not needed in final version

        if sensor.read():
                depth = sensor.pressure(ms5837.UNITS_psi)           # Get presure in psi
                #####print("P: %0.4f m \t T: %0.2f C  %0.2f F\n" % (         # Print not needed in final version
                ###depth,      # Sensor depth, either fresh or salf water depending on above
                ###sensor.temperature(), # Default is degrees C (no arguments)
                ###sensor.temperature(ms5837.UNITS_Farenheit))) # Request Farenheit
        else:
                print ("Error reading pressure sensor.")            # Print not needed in final version
                exit(1)
        return depth



"""
Obtains a single temperature measurement from termperature sensor
Called only by get_essential_meas() part of rov class.
Parameters:
        None 
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
        #####f_temp = sensor.temperature(tsys01.UNITS_Farenheit)     # Get farenheit temp
        ######print("T: %.2f C\t%.2f F" % (c_temp, f_temp))           # Print not needed in final version
        
        return c_temp 

