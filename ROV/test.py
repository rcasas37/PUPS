#C:\Users\lledb\AppData\Local\Programs\Python\Python35-32\%compiles python%this is a test example .py file

# this is a test example .py file
# this file should run on startup based on the bash script I made:
# /etc/init.d/boot_py_script  OR beause of the line I added in:
# /etc/rc.local which runs after everython boots
from decimal import Decimal #Module provides converting a string to decimal
import os
import xml.etree.ElementTree as et      #et == ElementTree

# Returns the directory name as string of current dir and pass it the file __file__ that is being run in python
base_path = os.path.dirname(os.path.realpath(__file__))

#join base_path with ROV folder to actual .xml file name
xml_file = os.path.join(base_path, "xml_sensors.xml")

# Save file above into memory so we can work with it
tree = et.parse(xml_file)

# Returns the root of the .xml file to get access to every other element underneeth that root
root = tree.getroot()

# Gets the sensor childs(child.tag) and their names(child.attrib) printed
#for child in root:
#    print(child.tag, child.attrib)

sensor_array = ["100", "10", "Friends", "99", "7", "1", "2", "3", "10", "9", "8"]

#writes an individual element to the sensor.xml file
temp_reading = "Landon"
root.find("Temperature").text = temp_reading 

#writes an individual element to the sensor.xml file
# prints the element in string form of pH
stringme = (root.find("Temperature").text + root.find("Pressure").text + root.find("pH").text + 
            root.find("Salinity").text + root.find("Dissolved_Oxygen").text) 

print(stringme)
root.find("pH").text = sensor_array[2] 

# Saves all changes to the sensor.xml file
tree.write(xml_file)


print(root.find("pH").text)      # prints the element in string form of pH

# Writes everyhting in the sensor_array above to the sensor.xml
"""
i = 0
for child in root:
#    for element in child:
    child.text = sensor_array[i]
    #print(child.tag, ":", child.text)
    i = i + 1
tree.write(xml_file)
"""

