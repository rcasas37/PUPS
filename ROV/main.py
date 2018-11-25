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
import control
import pigpio

# Global variables
# global my_var = 100 


"""
The main loop will control all of the operations of the ROV
Parameters:
        None
Return:	
        None
Notes:
	Initialized all sensor address data before main while loop and within
        other class object init() functions
"""
def main():
        # Define some variables used within main
        end_expedition = False 	# Variable to end program's main
        depth = 10               # Program terminates if depth is less than 0.867psi
        cmd_id = "0" 	            # Command ID stored as decimal number in python
        cmd_input = "n"
        cmd_message = "p,0,0,0,0,0,0,0"            # Init to none 
        cmd_list = [0,0,0,0,0,0,0]  # Init cmd_list
        temp_list =[0,0,0]

        # Initialize class objects and instances. (Also inits 2 xml files with default vals)
        rov = rov_skeleton.rov()		            # Init rov class/module instance
        ###pi = pigpio.pi()                                    # Init Raspberry Pi class instance
        ###rov_control = control.control(pi=pi)                # Init control class instance
        atlas_sensor = rov_skeleton.sensors.atlas_sensors() # Initialize atlas sensor class/module instance
        ###rov_control.arm()                                   # Init motor pwm signals

        # Create atlas sensor thread
        atlas_sensor_thread = Thread(target=atlas_sensor.run)
        atlas_sensor_thread.daemon = True       # Used to stop the thread once main finishes
        atlas_sensor_thread.start()

        # Open serial port communication
        ser = serial.Serial(port='/dev/ttyS0', baudrate=38400, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.010)

        cmd_id = "0" 
        lt_xaxis = 0 
        lt_yaxis = 0 
        rt_xaxis = 0 
        rt_yaxis = 0 
        collector_button = 0 
        sensor_button = "0" 
        headlights = 0 
        kval = "0" 
        water_type = "0" 
        count = 0

        ser.flushInput() # Flush serial port

        """
        Description While Loop:
        Reads and writes to the tether.
        Operates the ROV: controls the thrusters and takes sensor measurements.
        Logic to control the ROV's different states obtained from command center packets.
        """
        while end_expedition != True:
                # Everything goes here

                #print("inWaiting() bytes: ", ser.inWaiting())
                #if ser.inWaiting():
                        # Get control data from serial port
                cmd_message = rov.read_serial_port(ser)         # Read from serial port
                #ser.flushInput() # Flush serial port
                #else:
                #if count == 3:
                #        ser.flushInput() # Flush serial port
                #        count = 0
                        
                #        continue

                # CRC Check here before we use the message

                cmd_message = cmd_message.replace(";", "")      # Remove the terminating ; from the message to use the data

                # Write sensor data to serial port 
                rov.write_serial_port(ser, rov.send_sensor_data())

                # Alternative to writing the cmd message string to xml (IDK why I am trying to do that)
                cmd_list = cmd_message.split(",")               # Save each individual srting cmd into list cmd_list 
                msg_len = len(cmd_list)

                #testing:
                depth = rov.get_essential_meas(water_type)        # Get pressure and temp. 1st input = salt/fresh water (1/0)
                print("depth: " , depth)
                #print('x={0:0.3F} y={1:0.3F} z={2:0.3F} w={3}'.format(x, y, z, w))

                if msg_len != 8 and msg_len != 3 and msg_len != 1:
                        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$: ", msg_len)
                        #maybe stabalize rov here? cause no data recieved?
                        ser.flushInput() # Flush serial port
                        #print("This is the control_message: ", cmd_message)
                        continue
                else:
                        if cmd_list[0] != '':
                                print("*************************************************************************************************************************: ", msg_len)

                                # Print read results
                                print("This is the control_message: ", cmd_message)
                
                # Save Command Center data into variables
                if msg_len == 8:
                        cmd_id = cmd_list[0]
                        lt_xaxis = int(cmd_list[1])
                        lt_yaxis = int(cmd_list[2])
                        rt_xaxis = int(cmd_list[3])
                        rt_yaxis = int(cmd_list[4])
                        collector_button = cmd_list[5]
                        sensor_button = cmd_list[6]
                        headlights = int(cmd_list[7])

                elif msg_len == 3:
                        cmd_id = cmd_list[0]
                        kval = cmd_list[1]
                        water_type = cmd_list[2]

                elif msg_len == 1:
                        cmd_id = cmd_list[0]
                        if cmd_id == '':        # If no data is recieved
                                continue

                else:
                        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH", msg_len)
                        continue

                #ser.flushInput() # Flush serial port

                '''
                # Control ROV Command Data
                if cmd_id == "C":
                        # Drive ROV 
                        rov_control.left_stick_control(lt_xaxis, lt_yaxis)
                        rov_control.right_stick_control(rt_xaxis, rt_yaxis)
                        rov_control.set_motor_speed()

                        # Set LEDs
                        rov_control.light_control(headlights)

                        # Water Collection Control set at 40% speed
                        rov_control.water_pump_control(40, collector_button)
                        
                        pass
                # Shutdown ROV motors
                elif cmd_id == "p":
                        # Write normalized 0's (4001) to each motor axis to shut down the motors
                        rov_control.left_stick_control(4001, 4001)
                        rov_control.right_stick_control(4001, 4001)
                        rov_control.set_motor_speed()

                        # Water Collection Control set to off (0)
                        rov_control.water_pump_control(40, 0)
                        pass

                # Initalize ROV Data
                elif cmd_id == "z":
                        # Set k value for salinity probe. Water type is sent to pressure sensor each time after it is set
                        atlas_sensor.set_kval(kval) 
                        pass

                # End Expedition operation, quit loop and program when depth is approx 2ft or 0.867 psi
                elif cmd_id == "f":
                        # Drive ROV 
                        rov_control.left_stick_control(lt_xaxis, lt_yaxis)
                        rov_control.right_stick_control(rt_xaxis, rt_yaxis)
                        rov_control.set_motor_speed()

                        # Set LEDs
                        rov_control.light_control(headlights)

                        # Terminate when pressure is less than 2ft or 0.867 psi
                        if depth <= 0.867:
                                end_expedition = True
                        pass
                else:
                        print("Error, invalid command ID value: ", cmd_id)
                '''

                #ser.flushInput() # Flush serial port


                # Get Sensor Measurements
                if sensor_button == "1":
                        print("WATER TYPE: ", water_type)
                        depth,x,y,z,w = rov.get_essential_meas(water_type)        # Get pressure and temp. 1st input = salt/fresh water (1/0)
                        atlas_sensor.set_stop_flag(0) # 0 =go get atlas sensor meas
                        
                else: 
                        depth,x,y,z,w = rov.get_essential_meas(water_type)        # Get pressure and temp. 1st input = salt/fresh water (1/0)

                #count += 1


                """End While Loop"""
        # Write sensor data to serial port for last time before quit 
        rov.write_serial_port(ser, rov.send_sensor_data())

        # Shut down sensor thread before terminating the program
        atlas_sensor.terminate_thread()
        print("GOODBYE!")

        return 0 # End main() Definition # 


# Runs the main just defined above
main()

