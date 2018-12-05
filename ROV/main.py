"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: Landon Ledbetter
File: main.py
--------
Contains the main loop and uses functions that run SEAL's rov. Including
movement from the control class, sensor readings from the rov and sensor classes,
and communication to SEAL's cmd center via the raspberry pi's UART serial port.
"""

# Import code modules and classes 
import rov_skeleton 
from threading import Thread
import time
import serial
import os 
import xml.etree.ElementTree as et
import control
import pigpio


"""
The main loop will control all of the operations of the ROV and will be run
on Raspberry Pi on power on.
Parameters:
        None
Return:	
        None
Notes:
	Initialized all sensor address data before main while loop and within
        other class object init() functions. For example with the atlas sensors
        the address data is initalized internally within that class.
"""
def main():
        # Define some variables used within main
        end_expedition = False 	    # Variable to end program's main
        depth = 20                  # Program terminates if depth is less than 16.867psi
        cmd_id = "0" 	            # Command ID stored as decimal number in python
        cmd_message = "p,0,0,0,0,0,0,0"     # Init command message list to store data recieved 
        cmd_list = [0,0,0,0,0,0,0]  # Init cmd_list to store data recieved minus the eol ";" into a list variable
        lt_xaxis = 0                # Variables to store cmd center data (below) 
        lt_yaxis = 0                # - 
        rt_xaxis = 0                # - 
        rt_yaxis = 0                # - 
        collector_button = 0        # - 
        sensor_button = "0"         # - 
        headlights = 0              # - 
        kval = "1"                  # - 
        water_type = "0"            # Variables to store cmd center data (above) 
        error_count = 0             # Init error count for empty command packets
        orient = ["0","0","0","0"]  # Init tilt orientation data
        os.system("cp xml_sen_backup.xml xml_sensors.xml")
        os.system("cp xml_at_backup.xml xml_atlas.xml")
        time.sleep(.1)              # Ensure that the xml files are formated correctly on each boot
        
        # Initialize class objects and instances. (Also inits 2 xml files with default vals)
        rov = rov_skeleton.rov()		            # Init rov class/module instance
        pi = pigpio.pi()                                    # Init Raspberry Pi class instance
        rov_control = control.control(pi=pi)                # Init control class instance
        atlas_sensor = rov_skeleton.sensors.atlas_sensors() # Initialize atlas sensor class/module instance
        rov_control.arm()                                   # Init motor pwm signals
        time.sleep(1)                                       # Wait for thrusters to arm

        # Create atlas sensor thread
        atlas_sensor_thread = Thread(target=atlas_sensor.run)
        atlas_sensor_thread.daemon = True       # Used to stop the thread once main finishes
        atlas_sensor_thread.start()

        # Open serial port communication
        ser = serial.Serial(port='/dev/ttyS0', baudrate=19200, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.010)
        ser.flushInput() # Flush serial port

        """
        Description While Loop:
        Reads and writes to the tether/RPi serial port.
        Operates the ROV: controls the thrusters and takes sensor measurements.
        Logic to control the ROV's different states obtained from command center packets.
        """
        while end_expedition != True:
                try:
                        # Get control data from serial port
                        cmd_message = rov.read_serial_port(ser)         # Read from serial port
                        cmd_message = cmd_message.replace(";", "")      # Remove the eol ";" from the message to use the data

                        # Write sensor data to serial port 
                        rov.write_serial_port(ser, rov.send_sensor_data())

                        # Save each individual command data string into list
                        cmd_list = cmd_message.split(",")
                        msg_len = len(cmd_list)

                        # Check to ensure that the received message legth is of the correct size 8, 3 or 1 depending on the packet
                        if msg_len != 8 and msg_len != 3 and msg_len != 1:
                                # Command message was in error so flush port and restart the while loop
                                ser.flushInput() # Flush serial port
                                continue
                        else:
                                # If message is of length 8, 3, or 1 and not empty, pass onto normal ROV operation
                                if cmd_list[0] != '':
                                        # Print read results as debug
                                        print("*************************************************************************************************************************: ", msg_len)
                                        print("This is the control_message: ", cmd_message)
                                pass

                        # Save Command Center data into main.py variables
                        if msg_len == 8:            # Data is normal ROV control packet 
                                cmd_id = cmd_list[0]
                                if cmd_id == "C":
                                        # Check to ensure that the data is an integer before trying to convert string data to integer
                                        if rov.check_int(cmd_list[1]):      
                                                lt_xaxis = int(cmd_list[1])
                                        if rov.check_int(cmd_list[2]):
                                                lt_yaxis = int(cmd_list[2])
                                        if rov.check_int(cmd_list[3]):
                                                rt_xaxis = int(cmd_list[3])
                                        if rov.check_int(cmd_list[4]):
                                                rt_yaxis = int(cmd_list[4])
                                        collector_button = cmd_list[5]
                                        sensor_button = cmd_list[6]
                                        if rov.check_int(cmd_list[7]):
                                                headlights = int(cmd_list[7])
                                error_count = 0     # Got good data, reset error count

                        elif msg_len == 3:          # Data is initalization packet
                                cmd_id = cmd_list[0]
                                if cmd_id == "z":
                                        kval = cmd_list[1]
                                        water_type = cmd_list[2]
                                error_count = 0     # Got good data, reset error count

                        elif msg_len == 1:          # Data is pause packet or no data received 
                                cmd_id = cmd_list[0]
                                if cmd_id == '':        # If no data is received
                                        #Shut off motors if count of bad messages > 10
                                        error_count += 1
                                        if error_count > 10:
                                                # No data received, turn off thrusters, write normalized 0's (5000) to each motor axis to shut down 
                                                print("10 bad messages")    # Print debug
                                                rov_control.left_stick_control(5000, 5000)
                                                rov_control.right_stick_control(5000, 5000)
                                                rov_control.set_motor_speed()
                                                rov_control.water_pump_control(40, 0)
                                                error_count = 0             # Reset error count to avoid int overflow given long no connect
                                        continue
                        else:           # Unexpected packet, go get next
                                error_count = 0     # Reset error count
                                continue
                        
                        # ROV Control based on packet received and parsed above into main.py variables
                        if cmd_id == "C":
                                # Drive ROV 
                                rov_control.left_stick_control(lt_xaxis, lt_yaxis, orient)
                                rov_control.right_stick_control(rt_xaxis, rt_yaxis, orient)
                                rov_control.set_motor_speed()

                                # Set LEDs
                                rov_control.light_control(headlights)

                                # Water Collection Control set at 40% speed
                                rov_control.water_pump_control(40, collector_button)
                                pass

                        # Shutdown ROV motors
                        elif cmd_id == "p":
                                # Write normalized 0's (5000) to each motor axis to shut down the motors
                                rov_control.left_stick_control(5000, 5000)
                                rov_control.right_stick_control(5000, 5000)
                                rov_control.set_motor_speed()

                                # Water Collection Control set to off (0)
                                rov_control.water_pump_control(40, 0)
                                pass

                        # Initalize ROV Data
                        elif cmd_id == "z":
                                # Set k value for salinity probe. Water type is sent to pressure sensor each time after it is set initially
                                atlas_sensor.set_kval(kval) 
                                pass

                        # End Expedition operation, quit loop and program when depth is approx 2ft or 0.867 psi
                        elif cmd_id == "f":
                                # Drive ROV 
                                rov_control.left_stick_control(lt_xaxis, lt_yaxis, orient)
                                rov_control.right_stick_control(rt_xaxis, rt_yaxis, orient)
                                rov_control.set_motor_speed()

                                # Set LEDs
                                rov_control.light_control(headlights)

                                # Terminate program when pressure is less than 2ft or 16.867 psi
                                if depth <= 16.867:
                                        print("Quit")
                                        end_expedition = True
                                pass

                        else:
                                print("Error, invalid command ID value: ", cmd_id)  # Debug print the errored cmd_id

                        # Get sensor measurements
                        if sensor_button == "1":    # Get all measurements
                                print("water type: ", water_type)
                                orient,depth = rov.get_essential_meas(water_type)        # get pressure, temp., and IMU input = salt/fresh water (1/0)
                                atlas_sensor.set_stop_flag(0)       # 0=go get atlas sensor meas

                        else:                       # Get essential measurements only 
                                orient,depth = rov.get_essential_meas(water_type)        # get pressure, temp., and IMU input = salt/fresh water (1/0)

                        """End While Loop"""

                # Must ensure that Raspberry Pi cannot get stuck into infinite while loop, if pressure sensor malfunctions
                except KeyboardInterrupt:
                        # Shut down thrusters and sensor thread
                        atlas_sensor.terminate_thread()
                        rov_control.disarm()

                        # If rov does not exit correctly it could corrupt xml files which will cause it to crash on
                        # next boot. Thus, added this to fix xmls after erroneous quit of main.py it just copies xml structure
                        # to the xmls the main.py file utilizes
                        os.system("cp xml_sen_backup.xml xml_sensors.xml")
                        os.system("cp xml_at_backup.xml xml_atlas.xml")
                        raise

        # Write sensor data to serial port for last time before quit 
        rov.write_serial_port(ser, rov.send_sensor_data())

        # Shut down sensor thread before terminating the program
        atlas_sensor.terminate_thread()

        # Shut down thrusters
        rov_control.disarm()

        # For terminal debugging 
        print("GOODBYE!") 

        return 0 # End main() Definition 

# Runs the main just defined above
main()

