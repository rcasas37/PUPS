import serial
import sys
import time
import string
from serial import SerialException



ser = serial.Serial(
        port = '/dev/ttyS0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout=1
)

def print_to_buoy():
   str = "ROV;".encode()
   ser.write(str)

try:
   print("Test program to connect to F5529 Backchannel UART")

   #print("Sending test string")
   #str = "ROV;".encode()       #This string must be as long as david's launchpad expects
   #ser.write(str)

   #print_to_buoy()
   time.sleep(1)

   #print("Read from serial")

   while 1:
      #print("Sending test string")
      #str = "ROV;".encode
      #ser.write(str)

      print("Sending test string")
      print_to_buoy()
      time.sleep(1)

      print("Read from serial")
      serial_line = ser.readline()

      print(serial_line.decode())

      #time.sleep(1)

   # Only executes once the loop exits (which it won't)
   ser.close()

except KeyboardInterrupt:
   ser.close()
