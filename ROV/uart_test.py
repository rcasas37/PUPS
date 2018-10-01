import serial
import sys
import time
import string
from serial import SerialException



ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

try:
   print("Test program to connect to F5529 Backchannel UART")

   print("Sending test string")
   str = "Hello David\r"
   ser.write(str)

  # time.sleep(1)

   print("Read from serial")

   while 1:
      serial_line = ser.readline()

      print(serial_line)

      time.sleep(1)

   # Only executes once the loop exits (which it won't)
   ser.close()

except KeyboardInterrupt:
   ser.close()
