Python program and files used to control the ROV and poll environmental sensors.

The main.py is the file that is run by the Raspberry Pi and it utilizes 
classes contained in the files present within this directory.

Adafruit_BNO055 - Directory that contains the necessary files for the IMU sensor.
control.py - File that contains the movement and control of LEDs, thrusters and pump
ms5837.py - Class file for the pressure sensor and its functions
tsys01.py - Class file for the temperature sensor and its functions
sensors.py- Class file for the three atlas scientific sensors this class is run on a separate thread and polls each atlas sensor one at a time.
rov_skeleton.py - Class file that contains functions for reading and writing to the serial port of the Rpi. It also controls when essential measurements are taken etc.
xml_sensors.xml - Stores the essential sensor measurements such as temp, press, and IMU data
xml_sen_backup.xml - Default xml structure used as a backup by main.py in case the original xml gets corrupted by power failure.
xml_atlas.xml - Stores the Atlas Scientific sensor measurements such as pH, DO, and Salinity
xml_at_backup.xml - Same as the other backup file but for the atlas xml

