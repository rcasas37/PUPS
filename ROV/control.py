"""
Texas A&M University
Electronic Systems Engineering Technology
ESET-420 Capstone II
Author: Rogelio Casas Jr. 
File: control.py
--------------------------------------------------------------------------------------
Contains the classes needed to control movement for the ROV. This is done by
sending various PWM signals to either the T200 thrusters, water pump, or light.
It uses the PWM class that was created by PIGPIO for the PCA9685 module. 
"""

import time
import pigpio
#import motors
import control

"""
This class provides an interface to the I2C PCA9685 PWM chip. The chip provides 16 PWM 
channels. All channels use the same frequency which may be set in the range 24 to 
1526 Hz. If used to drive servos the frequency should normally be set in the range 50 
to 60 Hz. The duty cycle for each channel may be independently set between 0 and 100%.

It is also possible to specify the desired pulse width in microseconds rather than the 
duty cycle.  This may be more convenient when the chip is used to drive servos. The 
chip has 12 bit resolution, i.e. there are 4096 steps between off and full on.
"""
class PWM:

   _MODE1         = 0x00
   _MODE2         = 0x01
   _SUBADR1       = 0x02
   _SUBADR2       = 0x03
   _SUBADR3       = 0x04
   _PRESCALE      = 0xFE
   _LED0_ON_L     = 0x06
   _LED0_ON_H     = 0x07
   _LED0_OFF_L    = 0x08
   _LED0_OFF_H    = 0x09
   _ALL_LED_ON_L  = 0xFA
   _ALL_LED_ON_H  = 0xFB
   _ALL_LED_OFF_L = 0xFC
   _ALL_LED_OFF_H = 0xFD

   _RESTART = 1<<7
   _AI      = 1<<5
   _SLEEP   = 1<<4
   _ALLCALL = 1<<0

   _OCH    = 1<<3
   _OUTDRV = 1<<2

   def __init__(self, pi, bus=1, address=0x40):

      self.pi = pi
      self.bus = bus
      self.address = address

      self.h = pi.i2c_open(bus, address)

      self._write_reg(self._MODE1, self._AI | self._ALLCALL)
      self._write_reg(self._MODE2, self._OCH | self._OUTDRV)

      time.sleep(0.0005)

      mode = self._read_reg(self._MODE1)
      self._write_reg(self._MODE1, mode & ~self._SLEEP)

      time.sleep(0.0005)

      self.set_duty_cycle(-1, 0)
      self.set_frequency(200)

   """
   Returns the PWM frequency
   Parameters:
      self - Needed for all functions in class
   Return:
      N/A
   """
   def get_frequency(self):
      return self._frequency

   """
   Sets the PWM frequency
   Parameters:
      self - Needed for all functions in class
      frequency - What frequency to set it to
   Return:
      N/A
   """
   def set_frequency(self, frequency):
      prescale = int(round(25000000.0 / (4096.0 * frequency)) - 1)

      if prescale < 3:
         prescale = 3
      elif prescale > 255:
         prescale = 255

      mode = self._read_reg(self._MODE1);
      self._write_reg(self._MODE1, (mode & ~self._SLEEP) | self._SLEEP)
      self._write_reg(self._PRESCALE, prescale)
      self._write_reg(self._MODE1, mode)

      time.sleep(0.0005)

      self._write_reg(self._MODE1, mode | self._RESTART)

      self._frequency = (25000000.0 / 4096.0) / (prescale + 1)
      self._pulse_width = (1000000.0 / self._frequency)

   """
   Sets the duty cycle for a channel.  Use -1 for all channels.
   Parameters:
      self - Needed for all functions in class
      channel - Channels on PCA9685 chip (0-15)
      percent - Percentage for duty cycle (0-100)
   Return:
      N/A
   """
   def set_duty_cycle(self, channel, percent):
      steps = int(round(percent * (4096.0 / 100.0)))

      if steps < 0:
         on = 0
         off = 4096
      elif steps > 4095:
         on = 4096
         off = 0
      else:
         on = 0
         off = steps

      if (channel >= 0) and (channel <= 15):
         self.pi.i2c_write_i2c_block_data(self.h, self._LED0_ON_L+4*channel,
            [on & 0xFF, on >> 8, off & 0xFF, off >> 8])

      else:
         self.pi.i2c_write_i2c_block_data(self.h, self._ALL_LED_ON_L,
            [on & 0xFF, on >> 8, off & 0xFF, off >> 8])

   """
   Sets the pulse width for a channel.  Use -1 for all channels.
   Parameters:
      self - Needed for all functions in class
      channel - Channels on PCA9685 chip (0-15)
      width - The width of the square wave in milliseconds
   Return:
      N/A
   """
   def set_pulse_width(self, channel, width):
      self.set_duty_cycle(channel, (float(width) / self._pulse_width) * 100.0)

   """
   Switches all PWM channels off and releases resources.
   Parameters:
      self - Needed for all functions in class
   Return:
      N/A
   """
   def cancel(self):
      self.set_duty_cycle(-1, 0)
      self.pi.i2c_close(self.h)

   def _write_reg(self, reg, byte):
      self.pi.i2c_write_byte_data(self.h, reg, byte)

   def _read_reg(self, reg):
      return self.pi.i2c_read_byte_data(self.h, reg)


"""
Class that handles controlling the motors, lights, and water pump. It also
passes the PWM and pi object to the class to be used later.
When creating the object, initialize the motors using the parameters
where m# is motors, l# is lights, and w# is water pump with it having two enables
defaulted to GPIO25 and GPIO8.
"""
class control:
   """
   Initializes the class for use
   Parameters:
      self - Needed for all functions in class
      pi - Reference to pigpio pi object. Defaulted to 0 
      pwm - Creating PWM object using reference to pi object. Defaulted to 0
      m1 - Channel that the first motor is connected to. Defaulted to 0
      m2 - Channel that the second motor is connected to. Defaulted to 1
      m3 - Channel that the third motor is connected to. Defaulted to 2
      m4 - Channel that the fourth motor is connected to. Defaulted to 3
      m5 - Channel that the fifth motor is connected to. Defaulted to 4
      m6 - Channel that the sixth motor is connected to. Defaulted to 5
      l1 - Channel that the lights are connected to. Defaulted to 6
      w1 - Channel that the water pump is connected to. Defaulted to 12
      w1_en1 - GPIOs needed to control direction of water pump. Defaulted to 25
      w1_en2 - GPIOs needed to control direction of water pump. Defaulted to 8
   Return:
      N/A
   """
   def __init__(self, pi=0, pwm=0, m1=0, m2=1, m3=2, m4=3, m5=4, m6=5, l1=6, w1=12, w1_en1=25, w1_en2=8):
      self.pi = pi #pigpio.pi()
      self.pwm = control.PWM(self.pi)
      self.m1 = m1
      self.m2 = m2
      self.m3 = m3
      self.m4 = m4
      self.m5 = m5
      self.m6 = m6
      self.l1 = l1
      self.w1 = w1
      self.w1_en1 = w1_en1
      self.w1_en2 = w1_en2

   """
   Sends the initialization signal to all motors, sets the light off, water pump
   off, and writes 0 to the two GPIOs to 0 (which is the command for stopped)
   Parameters:
      self - Needed for all functions in class
   Return:
      N/A
   """
   def arm(self):
      self.pwm.set_pulse_width(self.m1, 1530)
      self.pwm.set_pulse_width(self.m2, 1530)
      self.pwm.set_pulse_width(self.m3, 1530)
      self.pwm.set_pulse_width(self.m4, 1530)
      self.pwm.set_pulse_width(self.m5, 1530)
      self.pwm.set_pulse_width(self.m6, 1530)
      self.pwm.set_pulse_width(self.l1, 1100)
      self.pwm.set_duty_cycle(self.w1, 0)
      self.pi.write(self.w1_en1, 0)
      self.pi.write(self.w1_en2, 0)
      time.sleep(1)

   """
   Stops the motors, water pump and light
   Parameters:
      self - Needed for all functions in class
   Return:
      N/A
   """
   def disarm(self):
      self.pwm.set_pulse_width(self.m1, 0)
      self.pwm.set_pulse_width(self.m2, 0)
      self.pwm.set_pulse_width(self.m3, 0)
      self.pwm.set_pulse_width(self.m4, 0)
      self.pwm.set_pulse_width(self.m5, 0)
      self.pwm.set_pulse_width(self.m6, 0)
      self.pwm.set_pulse_width(self.l1, 1100)
      self.pwm.set_duty_cycle(self.w1, 0)
      self.pi.write(self.w1_en1, 0)
      self.pi.write(self.w1_en2, 0)

   """
   Stops the motors, water pump and light
   Parameters:
      self - Needed for all functions in class
      analog_value - Values from remote control that are converted to useable
      values to be able to dynamically adjust speed of control
   Return:
      Normalized values
   """
   def norm_values(self, analog_value):
      return (analog_value // 137)

   """
   Main function calls sub functions that handle what is done depending on the incoming
   x and y axis values from the left stick. Created a software deadband of +/- 4000 to 
   prevent jittering when the controller sticks are not touched.
   Parameters:
      self - Needed for all functions in class
      left_x - Controller value from x-axis on left stick 
      left_y - Controller value from y-axis on left stick
   Return:
      N/A
   """
   def left_stick_control(self, left_x, left_y):
      #Check to see what direction it is going in the y axis
      if left_y > 4000:
          self.tilt_n(self.norm_values(left_y-3999))
      elif left_y < -4000:
          self.tilt_s(self.norm_values(left_y+3999))

      #Check to see what direction it is going in the x axis
      if left_x > 4000:
          self.tilt_e(self.norm_values(left_x-3999))
      elif left_x < -4000:
          self.tilt_w(self.norm_values(left_x+3999))

   """
   Tilting the ROV to the north direction
   Parameters:
      self - Needed for all functions in class
      norm_left_y - normalized left y-axis value used to modify pulse width
   Return:
      N/A
   """
   def tilt_n(self, norm_left_y):
      self.pwm.set_pulse_width(self.m1, 1525 + left_y + 30)
      self.pwm.set_pulse_width(self.m3, 1530)
      #self.pwm.set_pulse_width(self.m3, -left_y)

   """
   Tilting the ROV to the south direction
   Parameters:
      self - Needed for all functions in class
      norm_left_y - normalized left y-axis value used to modify pulse width
   Return:
      N/A
   """
   def tilt_s(self, norm_left_y):
      self.pwm.set_pulse_width(self.m3, 1475 + left_y + 30)
      self.pwm.set_pulse_width(self.m1, 1530)
      #self.pwm.set_pulse_width(self.m1, -left_y)

   """
   Tilting the ROV to the east direction
   Parameters:
      self - Needed for all functions in class
      norm_left_x - normalized left x-axis value used to modify pulse width
   Return:
      N/A
   """
   def tilt_e(self, norm_left_x):
      self.pwm.set_pulse_width(self.m2, 1525 + left_x + 30)
      self.pwm.set_pulse_width(self.m4, 1530)
      #self.pwm.set_pulse_width(self.m4, -left_x)

   """
   Tilting the ROV to the west direction
   Parameters:
      self - Needed for all functions in class
      norm_left_x - normalized left x-axis value used to modify pulse width
   Return:
      N/A
   """
   def tilt_w(self, norm_left_x):
      self.pwm.set_pulse_width(self.m4, 1475 + left_x + 30)
      self.pwm.set_pulse_width(self.m2, 1530)
      #self.pwm.set_pulse_width(self.m2, -left_x)

   """
   Main function calls sub functions that handle what is done depending on the incoming
   x and y axis values from the right stick. Created a software deadband of +/- 4000 to 
   prevent jittering when the controller sticks are not touched.
   Parameters:
      self - Needed for all functions in class
      right_x - Controller value from x-axis on left stick 
      right_y - Controller value from y-axis on left stick
   Return:
      N/A
   """
   def right_stick_control(self, right_x, right_y):
      #Check to see what direction it is going in the y axis
      if right_y > 4000:
          self.tilt_n(self.norm_values(right_y-3999))
      elif right_y < -4000:
          self.tilt_s(self.norm_values(right_y+3999))

      #Check to see what direction it is going in the x axis
      if right_x > 4000:
          self.tilt_e(self.norm_values(right_x-3999))
      elif right_x < -4000:
          self.tilt_w(self.norm_values(right_x+3999))

   """
   Rises up to the surface by having motors 1-4 straight up
   Parameters:
      self - Needed for all functions in class
      norm_right_y - normalized right y-axis value used to modify pulse width
   Return:
      N/A
   """
   def rise(self, norm_right_y):
      self.pwm.set_pulse_width(self.m1, 1525 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m2, 1525 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m3, 1525 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m4, 1525 + norm_right_y + 30)

   """
   Dives down to the surface by having motors 1-4 straight up
   Parameters:
      self - Needed for all functions in class
      norm_right_y - normalized right y-axis value used to modify pulse width
   Return:
      N/A
   """
   def dive(self, norm_right_y):
      self.pwm.set_pulse_width(self.m1, 1475 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m2, 1475 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m3, 1475 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m4, 1475 + norm_right_y + 30)

   """
   Rotates counter-clockwise by having motors 5 and 6 go forward
   Parameters:
      self - Needed for all functions in class
      norm_right_x - normalized right y-axis value used to modify pulse width
   Return:
      N/A
   """
   def rotate_cw(self, norm_right_x):
      self.pwm.set_pulse_width(self.m5, 1525 + norm_right_x + 30)
      self.pwm.set_pulse_width(self.m6, 1525 + norm_right_x + 30)

   """
   Rotates clockwise by having motors 5 and 6 go backwards
   Parameters:
      self - Needed for all functions in class
      norm_right_x - normalized right y-axis value used to modify pulse width
   Return:
      N/A
   """
   def rotate_ccw(self, norm_right_x):
      self.pwm.set_pulse_width(self.m5, 1475 + norm_right_x + 30)
      self.pwm.set_pulse_width(self.m6, 1475 + norm_right_x + 30)

   """
   Controls the light intensity. Needs power which is a variable from 0 to 100
   and will adjust the pwm (1100-1900) as needed
   Parameters:
      self - Needed for all functions in class
      power - The intensity of the light with 0 being off
   Return:
      N/A
   """
   def light_control(self, power):
      if power == 0:
         self.pwm.set_pulse_width(self.l1, 1100)
      else:
         self.pwm.set_pulse_width(self.l1, 1100 + power*8)

   """
   Control for water pump. Needs speed (pwm variable) and enable variable since
   we are just turning it on or off
   """

   """
   Control for water pump. Needs speed (pwm variable) and enable variable since
   we are just turning it on or off
   Parameters:
      self - Needed for all functions in class
      pwm - Speed of the water pump
      en - Value that tells if the pump is on or off (0-1 respectively)
   Return:
      N/A
   """
   def water_pump_control(self, pwm, en):
      if en == 0:
         self.pwm.set_duty_cycle(self.w1, pwm)
         self.pi.write(self.w1_en1, 0)
         self.pi.write(self.w1_en2, 0)
      elif en == 1:
         self.pwm.set_duty_cycle(self.w1, pwm)
         self.pi.write(self.w1_en1, 0)
         self.pi.write(self.w1_en2, 1)


if __name__ == "__main__":

   import time

   import control
   import pigpio

   rov_cont = motors.control()

   try:
      '''
      #Test program for left motors
      print("Test program for Tilt")
      print("Sending initialization signal...")
      rov_cont.arm()
      while(1):
         x_axis_left = int(input("X-axis of left stick? "))
         y_axis_left = int(input("Y-axis of left stick? "))
         rov_cont.left_stick_control(x_axis_left, y_axis_left)
         time.sleep(2)
      '''

      '''
      #Test program for lights
      print("Test program for Light")
      rov_cont.arm()
      while(1):
         power_check = int(input("Light intensity? (0 - 100): "))
         rov_cont.light_control(power_check)
         time.sleep(2)
      '''

      
      #Test program for water pump
      print("Test program for water pump")

      rov_cont.arm()

      while(1):
         pwm_check = int(input("Speed?: "))
         en_check = int(input("Is the pump on or off? (0-1): "))

         rov_cont.water_pump_control(pwm_check, en_check)
         time.sleep(2)
      
   except KeyboardInterrupt:
      rov_cont.disarm()
