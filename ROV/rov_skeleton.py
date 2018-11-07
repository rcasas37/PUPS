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

import serial
import os   # Module used to find the file directory path for reading and writing to .xml
import xml.etree.ElementTree as et  # Module provides .xml file manipulation and functions

# Global variables
#global my_var                """Example if absolutely needed ONLY"""
#my_var = 34 

class rov:
        default_sensor_xml = "xml_sensors.xml"   
        default_command_xml = "xml_commands.xml"   
        cmd_xml_elem = ["id_char", "lt_xaxis", "lt_yaxis", "rt_xaxis", "rt_yaxis", "a_button", "x_button", "headlights", "crc", "k_value", "water_type"]
        error_byte = 0

        
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
        def __init__(self, sensor_xml_file=default_sensor_xml, command_xml_file=default_command_xml):
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
                root.find("headlights").text = "0"      # Init headlights to off 
                root.find("crc").text = "0"             # CRC value 
                root.find("k_value").text = "10"        # Our probe is 10
                root.find("water_type").text = "salt"   # fresh or salt 

                tree.write(xml_file)    # Saves all changes to the commands.xml on the SD card

                # Initilize all values in sensors.xml to defaults (0)
                base_path1 = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                self.xml_file1 = os.path.join(base_path1, sensor_xml_file)     # Join base_path with actual .xml file name
                self.tree1 = et.parse(self.xml_file1)                               # Save file into memory to work with its children/elements
                self.root1 = self.tree1.getroot()                                   # Returns root of the xml file to get access to all elements 

                """
                self.root1.find("id_char").text = "S"         # S=sensor packet 
                self.root1.find("Temperature").text = "Temperature"
                self.root1.find("Pressure").text = "Pressure"
                self.root1.find("pH").text = "pHval"
                self.root1.find("Salinity").text = "Salinity"
                self.root1.find("Dissolved_Oxygen").text = "DOxy"
                self.root1.find("Errored_Sensor").text = "0"
                self.root1.find("Gyroscope1").text = "1"
                self.root1.find("Gyroscope2").text = "2"
                self.root1.find("Gyroscope3").text = "3"
                self.root1.find("Accelerometer1").text = "999"
                self.root1.find("Accelerometer2").text = "99"
                self.root1.find("Accelerometer3").text = "9"
                self.tree1.write(self.xml_file1)    # Saves all changes to the sensors.xml on the SD card
                """

                return



        """
        Reads a specific element from the commands.xml file for motor/ROV control
        Parameters:
                Select a specific command center element to read 
        Return:
                Returns string to use for ROV control 
        Notes:
        """
        def read_command_xml(self, cmd_element):
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
        and returns string ready to send over serial port 
        Parameters:
               None 
        Return:
               Returns the sensor string in format: "S,pH,DO,Sal,Temp,Presure,Gyro1,Accel1,Error_byte;" 
        Notes:
        """
        def send_sensor_data(self):
                # Open sensor.xml read from and concatenate all sensor data into string close sensor.xml
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_sensors.xml")   # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                # create sensor string from sensors.xml 
                sensor_str= (root.find("id_char").text + "," + root.find("pH").text + "," + root.find("Dissolved_Oxygen").text + "," +
                            root.find("Salinity").text + "," + root.find("Temperature").text + "," + root.find("Pressure").text + "," +
                            root.find("Gyroscope1").text + "," + root.find("Accelerometer1").text + "," + root.find("Errored_Sensor").text + ";") 

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
                # Open sensor.xml read from and concatenate all sensor data into string close sensor.xml
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_sensors.xml")   # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                # Create sensor string from sensor.xml 
                sensor_str= (root.find("Temperature").text + root.find("Pressure").text + root.find("pH").text + 
                        root.find("Salinity").text + root.find("Dissolved_Oxygen").text + root.find("Errored_Sensor").text + ";") 
                return



        """
        Parses data received from serial port and writes each element it to command.xml for motor use.
        Parameters:
                Command center string cmd_str
        Return:
                None 
        Notes:
        """
        def parse_control_message(self, cmd_str):
                cmd_list = cmd_str.split(",")           # Get list of each individual cmd from cmd center
                i = 0
                length = len(cmd_list)
                print("Length of cmd_list: %d" % len(cmd_list))

                # If the cmd msg is a normal control packet 'C'
                if (length != 0 and length <= 9):   
                        for cmd in cmd_list:            # Write each individual element to the command.xml
                                write_xml("1", self.cmd_xml_elem[i], cmd)
                                i += 1
                # If the cmd msg is an initilization packet 'z'
                elif (length == 2):     
                        # Set the k value and water type of the sensors
                        write_xml("1", "k_value", cmd_list[0])
                        write_xml("1", "water_type", cmd_list[1])
                        write_xml("1", "crc", cmd_list[2])
                else:
                        print("command message is not greater than 1 or larger than 8")
                return



        """
        Uses control.xml values to calculate PWM (dir & spd) of selected motor
        Parameters:
                list of parameters
        Return:
                Do we return any value?
        Notes:
        """
        def calc_motor_spd(self):
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
        def set_motor_spd(self):
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
        def get_essential_meas(self, water_choice):
                # Get Pressure measurement and write it to sensors.xml
                depth = get_pressure(water_choice, self.root1)
                write_xml("0", "Pressure", str(depth))

                # Get Temperature measurement and write it to sensors.xml
                c_temp = get_temperature(self.root1)
                write_xml("0", "Temperature", str(c_temp))
                
                # Create the errored sensor string and save in xml
                current_error = self.error_byte
                new_error = 0x00
                print("Previous error in rov_skeleton: ", current_error)

                if depth == -1 and c_temp == -1:
                        new_error = 0x03 
                        self.error_byte = current_error | new_error 
                elif c_temp == -1:
                        new_error = 0x01 
                        self.error_byte = current_error | new_error 
                elif depth == -1:
                        new_error = 0x02 
                        self.error_byte = current_error | new_error 
                else:
                        no_error_mask = 0x1C        # Mask the byte to clear the temp and pressure bits 
                        self.error_byte = current_error & no_error_mask
                        print("rov_skeleton no error: ", self.error_byte)


                write_xml("0", "Errored_Sensor", str(self.error_byte))


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
        def get_all_meas(self):
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
        def stabilize_rov(self):
                # This one is gonna be a beach

                return


        """
        Obtain string commands from cmd center.
        Parameters:
                None
        Return:
                Returns full message from cmd center as a string with a terminating ';' 
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
                                if size is not None and len(line_str) >= size:  # Check if message is even in the buffer
                                        break
                        else:
                                break
                return bytes(line_str) 


        """
        Sends sensor array data to the command center terminated by a ';' 
        Called only by send_sensor_string() a part of the rov class. 
        Parameters:
                Sensor array string terminated by ';'  
        Return:
                None
        Notes:
        """
        def write_serial_port(self, ser, sensor_str):
                # Open and write sensor_str to serial port
                sensor_encoded = sensor_str.encode()
                #ser.flushInput()        # Flush serial port
                ser.write(sensor_encoded)

                # This is the sensor string I am getting
                print("This is the sensor string I have to send: ", sensor_str)

                return


        """
        DELETE - MARKED FOR DELETION SINCE MOVED THIS FUNCTION TO parse_control_message()
        Writes each command data element to the command.xml for motor use.
        Parameters:
                
        Return:
                None
        Notes:
        """
        def write_cmd_xml(self, cmd_str):
                cmd_list = cmd_str.split(",")           # Get list of each individual cmd from cmd center
                i = 0
                length = len(cmd_list)
                print("Length of cmd_list: %d" % len(cmd_list))

                # If the cmd msg is a normal control packet 'C'
                if (length != 0 and length <= 9):   
                        for cmd in cmd_list:            # Write each individual element to the command.xml
                                write_xml("1", self.cmd_xml_elem[i], cmd)
                                i += 1
                # If the cmd msg is an initilization packet 'z'
                elif (length == 2):     
                        # Set the k value and water type of the sensors
                        write_xml("1", "k_value", cmd_list[0])
                        write_xml("1", "water_type", cmd_list[1])
                        write_xml("1", "crc", cmd_list[2])
                else:
                        print("command message is not greater than 1 or larger than 8")
                return


        """
        Sets the current error byte for use within essential measuremnts()
        Parameters:
                Sensor Error Byte 
        Return:
                None
        Notes:
        """
        def set_error_byte(self, error):
                self.error_byte = error
                return

        """
        Gets the current error byte for use within essential measuremnts()
        Parameters:
                None 
        Return:
                Sensor Error Byte
        Notes:
        """
        def get_error_byte(self):
                return self.error_byte




############################################################
################ ROV Class Helper functions#################
############################################################

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
Gets individual string data to a single element in the chosen xml file.
Parameters:
        Select the xml to open, the element in the xml to overwrite, string to write to xml 
Return:
        None 
Notes:
"""
def read_xml(xml_choice, xml_element):
        # Read from command.xml
        if xml_choice == "1":
                # Open command.xml for reading
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_commands.xml")  # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 
                
                # Read data from the element chosen
                string_data = root.find(xml_element).text

        # Read from sensor.xml
        elif xml_choice == "0":
                # Open command.xml for reading
                base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
                xml_file = os.path.join(base_path, "xml_sensors.xml")   # Join base_path with actual .xml file name
                tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
                root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 

                # Read data from the element chosen
                string_data = root.find(xml_element).text
        else:
                print("Error in write_xml() function of rov_skelton no xml was written to.")

        return string_data



"""
Obtains a single pressure measurement from sensor
Called only by get_essential_meas() part of rov class.
Parameters:
        Water density chioce (salt/fresh watter) as string,
Return:
        Returns Depth as float in meters, Prints Temp. as float in Celsius
Notes:
"""
def get_pressure(water_choice, root1) :
        try:
                # Create sensor object
                sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)
                sensor.init()

        except:
                #root1.find("Pressure").text = "Not Connected"    # Set the xml feild
                return -1 

        # Must initialize pressure sensor before reading it
        #if not sensor.init():
        #        print("Error initializing pressure sensor.")            # Print not needed in final version
                ### exit(1)

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
                #####print("P: %0.4f m \t T: %0.2f C  %0.2f F\n" % (         # Print not needed in final version
                ###depth,      # Sensor depth, either fresh or salf water depending on above
                ###sensor.temperature(), # Default is degrees C (no arguments)
                ###sensor.temperature(ms5837.UNITS_Farenheit))) # Request Farenheit
        else:
                print ("Error reading pressure sensor.")            # Print not needed in final version
                ### exit(1)
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
def get_temperature(root1):
        base_path = os.path.dirname(os.path.realpath(__file__)) # Returns the directory name as str of current dir and pass it the curruent dir being run 
        xml_file = os.path.join(base_path, "xml_sensors.xml")  # Join base_path with actual .xml file name
        tree = et.parse(xml_file)                               # Save file into memory to work with its children/elements
        root = tree.getroot()                                   # Returns root of the xml file to get access to all elements 
        c_temp = 0.0
        try:
                # Create sensor object
                sensor = tsys01.TSYS01()

                # Must initilize temp sensor object
                if not sensor.init():
                    print("Error initializing temperature sensor.")         # Print not needed in final version
                    ### exit(1)

                # Read temp sensor once and save in c_temp variable
                if not sensor.read():
                    print("Error reading temperature sensor.")          # Print not needed in final version
                    ### exit(1)
                c_temp = sensor.temperature()                           # Get celcius temp
                #####f_temp = sensor.temperature(tsys01.UNITS_Farenheit)     # Get farenheit temp
                ######print("T: %.2f C\t%.2f F" % (c_temp, f_temp))           # Print not needed in final version
        except:
                #root1.find("Temperature").text = "Not Connected"      # Set the xml feild
                return -1 
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






