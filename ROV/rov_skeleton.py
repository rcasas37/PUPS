"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: Landon Ledbetter
File: rov_skeleton.py
--------
Contains the rov class and functions that run SEAL's rov. Including 
sensor readings and communication to SEAL's cmd center.
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


"""
The rov class handles initalizing xml files, setting up and managing essential sensor objects and takes measurements
such as temperature, pressure, and IMU orientation data. Class contains functions that reads and writes data
to and from xmls and it also has functions that reads and writes the appropriate messages to and from the
serial port. 
"""
class rov:
        # rov class member variables
        default_sensor_xml = "xml_sensors.xml"   
        default_atlas_xml = "xml_atlas.xml"   
        default_command_xml = "xml_commands.xml"   
        cmd_xml_elem = ["id_char", "lt_xaxis", "lt_yaxis", "rt_xaxis", "rt_yaxis", "a_button", "x_button", "k_value", "water_type"]


        """
        Initilizes the .xml files with values of zeros since this is only called 
        upon once at startup of the ROV, initalizes sensor objects for continued use within
        the rov class.
        Parameters:
                sensor_xml_file - Programmer can change the file to open and use if wanted
                command_xml_file - Programmer can change the file to open and use if wanted
                atlas_xml_file - Programmer can change the file to open and use if wanted
        Return:
                None 
        Notes:
                ROV class initilization function called upon when ROV object is created in main
        """
        def __init__(self, sensor_xml_file=default_sensor_xml, command_xml_file=default_command_xml, atlas_xml_file=default_atlas_xml):
                # Init imu sensor object
                self.bno = BNO055.BNO055(i2c=3, rst=18)         # Create bno object that uses bitbanged i2c line (3)
                try:
                        # Must initialize imu sensor before reading it checking each time in imu function takes approx 0.5 sec 
                        # and is thus impractical
                        if not self.bno.begin():
                                print("IMU sensor not initalized - rov_skeleton")
                except:
                        print("IMU sensor not initalized1 - rov_skeleton")

                # Init temperature sensor object
                self.temp_sensor = tsys01.TSYS01()              # Create temperature object that uses standard i2c line (1) 

                # Init pressure sensor object
                self.pres_sensor = ms5837.MS5837_30BA()         # Create pressure object that uses standard i2c line (1) 

                # Initilize all values in commands.xml to defaults (0)
                self.base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                self.xml_file = os.path.join(self.base_path, command_xml_file)    # Join base_path with actual .xml file name
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
                self.root1.find("Temperature").text = "Temp"
                self.root1.find("Pressure").text = "Pres"
                self.root1.find("N").text = "0" 
                self.root1.find("S").text = "0" 
                self.root1.find("E").text = "0" 
                self.root1.find("W").text = "0" 
                self.tree1.write(self.xml_file1)    # Saves all changes to the sensors.xml on the SD card

                # Initilize all values in atlas.xml to defaults (0)
                self.base_path2 = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                self.xml_file2 = os.path.join(self.base_path2, atlas_xml_file)      # Join base_path with actual .xml file name
                self.tree2 = et.parse(self.xml_file2)                               # Save file into memory to work with its children/elements
                self.root2 = self.tree2.getroot()                                   # Returns root of the xml file to get access to all elements 

                self.root2.find("id_char").text = "S"         # S=sensor packet 
                self.root2.find("pH").text = "pH"
                self.root2.find("Salinity").text = "Cond"
                self.root2.find("Dissolved_Oxygen").text = "DOxy"
                self.tree2.write(self.xml_file2)    # Saves all changes to the sensors.xml on the SD card
                return


        """
        Sends sensor data. Opens atlas.xml and checks if it is in use by atlas thread, if not it
        combines all data into a comma delineated string and returns the string 
        Parameters:
               None 
        Return:
               sensor_str - the concatinated sensor string e.g.: "S,pH,DO,Sal,Temp,Presure,N,E,S,W;" 
        Notes:
                Only used in conjunction with write_serial_port(), this function returns the string
                we want to write to the serial port
        """
        def send_sensor_data(self):
                # Set default sensor packet if atlas sensors fail via try and except below, send sensor read value of -1 (error)
                sensor_str= (self.root1.find("id_char").text + ",-1,-1,-1," +
                            self.root1.find("Temperature").text + "," + self.root1.find("Pressure").text + "," +
                            self.root1.find("N").text + "," +  self.root1.find("E").text + "," + self.root1.find("S").text + "," +
                            self.root1.find("W").text + ";") 
                try:
                        # Initalize access to the sensors.xml file
                        base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                        xml_file = os.path.join(base_path, "xml_atlas.xml")   # Join base_path with actual .xml file name
                        tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                        root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                        # create sensor string from sensors.xml 
                        sensor_str= (self.root1.find("id_char").text + "," + root.find("pH").text + "," + root.find("Dissolved_Oxygen").text + "," +
                                    root.find("Salinity").text + "," + self.root1.find("Temperature").text + "," + self.root1.find("Pressure").text + "," +
                                    self.root1.find("N").text + "," +  self.root1.find("E").text + "," + self.root1.find("S").text + "," +
                                    self.root1.find("W").text + ";") 
                except:
                        print("XMLXMLXML parse error.")     # Debug print shows when atlas.xml is already open in atlas thread
                        pass

                return sensor_str


        """
        Obtains temp, pressure, and IMU (Euler angles tilt measurements (N,E,S,W)
        Parameters:
                water_choice - chosen by the user at startup
        Return:
                orientation - Binary orientation tuple of size 4. Where 1 denotes tilted past 45 degrees
                depth - Depth of rov in PSI
        Notes:
        """
        def get_essential_meas(self, water_choice):
                # Get Pressure measurement and write it to sensors.xml
                depth = self.get_pressure(water_choice)
                self.root1.find("Pressure").text = str(depth)

                # Get Temperature measurement and write it to sensors.xml
                c_temp = self.get_temperature()
                self.root1.find("Temperature").text = str(c_temp)

                # Get IMU measurement and write it to sensors.xml
                roll,pitch = self.get_imu()
                
                # Use function here to determine "warning tilted at least +45deg n/s/e/w"
                orientation = self.check_orientation(roll,pitch)
                self.root1.find("N").text = orientation[0]
                self.root1.find("S").text = orientation[1]
                self.root1.find("E").text = orientation[2]
                self.root1.find("W").text = orientation[3]

                # Saves all changes to the sensors.xml on the SD card
                self.tree1.write(self.xml_file1)                    

                return orientation,depth 


        """
        Checks the orientation of the ROV and returns a binary tuple of 4 values that represent north,
        south, east, and west. A "1" for any of the 4 values means that the rov is tilted past 45 degrees
        in that direction. This also writes that direction to the command center so the user can correct.
        Parameters:
                Roll - The angle tilted off of the x-axis
                Pitch - The angle tilted off of the y-axis
        Return:
                Return binary tuple (size 4) of horizontal coordinate plane where 1 means it is tilted past threshold of 45 degrees 
        Notes:
                At most only 2 of the 4 variables can be a 1 at any given time i.e. North east or southwest etc
        """
        def check_orientation(self, roll, pitch):
                # Check to make sure IMU sensor is working
                if roll == 500 and pitch == 500:
                        return "1","1","1","1"

                # Default the orientations to OKAY or zero (not tilted off of any axis by more than 45 degrees
                n = "0"
                s = "0"
                e = "0"
                w = "0"
                
                # Check if roll or pitch exceeds 45 degree threshold
                if roll < -45: e = "1"
                elif roll > 45: w = "1"

                if pitch < 45: s = "1"
                elif pitch > 135: n = "1"

                return n,s,e,w


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
                        char = ser.read(1)          # Read 1 byte/character
                        if char:
                                line_str += char    # Append a single char string to the line_str 
                                if line_str[-len_eol:] == eol:                  # Check if char is terminating character
                                        break
                                if size is not None and len(line_str) >= size:  # Check if message exists in the buffer
                                        break

                        else:   # No bytes to read
                                break
                return bytes(line_str) 


        """
        Physically writes sensor string data to the tether to the command center terminated by a ';'  
        Parameters:
                ser - The serial port object to read bytes of data
                sensor_str - The sensor string we have to write to the tether
        Return:
                None
        Notes:
                Only used in conjunction with send_sensor_data() as the sensor_str input parameter.
                This is only ever called from main.py
        """
        def write_serial_port(self, ser, sensor_str):
                # Open and write sensor_str to serial port
                sensor_encoded = sensor_str.encode()
                ser.write(sensor_encoded)
                return



        """
        Obtains a Euler angle orientation heading, pitch, and roll measurement from BNO055 sensor
        Called only by get_essential_meas() part of the rov class.
        Parameters:
                None 
        Return:
                Returns tuple (size 2) of roll and pitch data 
        Notes:
                If BNO055 is not read try to restart and return invalide roll and pitch values
        """
        def get_imu(self):
                try:
                        # Read the Euler angles for heading, roll, pitch (all in degrees).
                        heading, roll, pitch = self.bno.read_euler()
                        #print('H={0:0.2F} R={1:0.2F} P={2:0.2F}'.format(heading, roll, pitch))
                except:
                        self.bno.begin()    # Try to restart BNO055
                        return 500,500      # Return values that will NEVER be read for Roll and Pitch

                #return x,y,z,w
                return roll, pitch


        """
        Obtains a single pressure measurement from pressure sensor
        Called only by get_essential_meas() part of rov class.
        Parameters:
                water_choice - Water density chioce (salt/fresh watter) as string,
        Return:
                depth - Depth as float in meters, Prints Temp. as float in Celsius
        Notes:
                Returns "-1" if sensor is not connected
        """
        def get_pressure(self, water_choice):
                # Check if pressure sensor is still there by initalizing it before each reading
                try:
                        # Must initialize pressure sensor before reading it
                        if not self.pres_sensor.init():
                                print("Error initializing pressure sensor.")# Print debug 
                except:
                        return "-1"

                # Freshwater vs Saltwater depth measurements set via user input form cmd center
                # default is freshwater if initalization packet is missed
                if water_choice == "1":     # Saltwater
                        self.pres_sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
                        freshwaterDepth = self.pres_sensor.depth() 
                        water_choice = "0"

                elif water_choice == "0":   # Freshwater
                        self.pres_sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)
                        freshwaterDepth = self.pres_sensor.depth() 
                        water_choice = "1"

                else:
                        print("Error on water density choice.")             # Print debug 

                if self.pres_sensor.read():
                        depth = self.pres_sensor.pressure(ms5837.UNITS_psi) # Get presure in psi
                else:
                        print ("Error reading pressure sensor.")            # Print debug 
                return depth



        """
        Obtains a single temperature measurement from termperature sensor
        Called only by get_essential_meas() part of rov class.
        Parameters:
                None 
        Return:
                c_temp - temperature as float in Celcius 
        Notes:
                Returns "-1" if sensor is not connected
        """
        def get_temperature(self):
                # Check if temperature sensor is still there by initalizing it before each reading
                try:
                        # Must initilize temp sensor object
                        if not self.temp_sensor.init():
                            print("Error initializing temperature sensor.")     # Print debug 
                except:
                        return "-1"

                # Read temp sensor once and save in c_temp variable
                if not self.temp_sensor.read():
                    print("Error reading temperature sensor.")                  # Print debug 
                
                c_temp = self.temp_sensor.temperature()                         # Get celcius temp
                
                return c_temp 


        """
        Checks a passed string to determine if it is an int. It also accounts for '-'
        and '+' signs just in case; as well as the empty string "". E.g. returns true
        for vals such as: "10", "-10" and "+10" false for any other char that is not an int.
        Parameters:
                s - String that will be checked if an integer value is present 
        Return:
                True/False - depending on if passed string is an integer. 
        Notes:
        """
        def check_int(self, s):
                if s == "":
                        return False
                if s[0] in ('-', '+'):
                        return s[1:].isdigit()
                return s.isdigit()


# End rov class functions

