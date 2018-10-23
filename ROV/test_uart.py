
# Import code modules
import time
import serial
import os 
import test_uart

#def main():
# Open serial port communication
ser = serial.Serial(port='/dev/ttyS0', baudrate=57600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)        # (physical port, baudrate, timeout interval)

ser.flushInput()

def write_ser(user):
        strr = user.encode() 
        ser.write(strr)

def read_ser():
        line = ser.read(1)
        return line

def read_ser_port(size=None, eol=';'):
        # Open and read from serial port and save in cmd_message variable
        len_eol = len(eol)
        line_str = bytearray() 
        while True:
                #ser.flushInput()        # Flush serial port
                char = ser.read(1)      # Read 1 byte or 1 char
                if char:
                        if char != "1":    # Is the current char the terminating char? No then append it.
                                line_str += char    # Append a single char string to the line_str 
                        if line_str[-len_eol:] == eol:                  # Check if char is terminating character
                                break
                        if size is not None and len(line_str) >= size:  # Check if message is even in the buffer
                                break
                else:
                        break
        return bytes(line_str) 

while 1:
        str_input = "Hey man;"
        line = read_ser_port()
        write_ser(str_input)
        time.sleep(.15)

        print("This is the received char: ", line)

        
        

#main()
