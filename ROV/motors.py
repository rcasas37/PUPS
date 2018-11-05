#!/usr/bin/env python

# PCA9685.py
# 2016-01-31
# Public Domain
# Modification made by Rogelio Casas Jr. for use with T200 Motors

import time
import pigpio
import motors

class PWM:

   """
   This class provides an interface to the I2C PCA9685 PWM chip.
   The chip provides 16 PWM channels.
   All channels use the same frequency which may be set in the
   range 24 to 1526 Hz.
   If used to drive servos the frequency should normally be set
   in the range 50 to 60 Hz.
   The duty cycle for each channel may be independently set
   between 0 and 100%.
   It is also possible to specify the desired pulse width in
   microseconds rather than the duty cycle.  This may be more
   convenient when the chip is used to drive servos.
   The chip has 12 bit resolution, i.e. there are 4096 steps
   between off and full on.
   """

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

   def get_frequency(self):

      "Returns the PWM frequency."

      return self._frequency

   def set_frequency(self, frequency):

      "Sets the PWM frequency."

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

   def set_duty_cycle(self, channel, percent):

      "Sets the duty cycle for a channel.  Use -1 for all channels."

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

   def set_pulse_width(self, channel, width):

      "Sets the pulse width for a channel.  Use -1 for all channels."

      self.set_duty_cycle(channel, (float(width) / self._pulse_width) * 100.0)

   def cancel(self):

      "Switches all PWM channels off and releases resources."

      self.set_duty_cycle(-1, 0)
      self.pi.i2c_close(self.h)

   def _write_reg(self, reg, byte):
      self.pi.i2c_write_byte_data(self.h, reg, byte)

   def _read_reg(self, reg):
      return self.pi.i2c_read_byte_data(self.h, reg)

class control:

   """
   Class that handles controlling the motors, lights, and water pump. It also
   passes the PWM and pi object to the class to be used later.
   When creating the object, initialize the motors using the parameters
   where m# is motors, l# is lights, and w# is water pump with it having two enables
   defaulted to GPIO25 and GPIO8.
   """

   def __init__(self, pi=0, pwm=0, m1=0, m2=1, m3=2, m4=3, m5=4, m6=5, l1=6, w1=12, w1_en1=25, w1_en2=8):
      self.pi = pigpio.pi()
      self.pwm = motors.PWM(self.pi)
      self.pi = pi
      self.m1 = m1
      self.m2 = m2
      self.m3 = m3
      self.m4 = m4
      self.m5 = m5
      self.m6 = m6
      self.l1 = l1
      self.w1 = w1

   """
   Sends the initialization signal to all motors.
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

   def norm_values(self, analog_value):
      return (analog_value // 137)

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


   def tilt_n(self, norm_left_y):
      self.pwm.set_pulse_width(self.m1, 1525 + left_y + 30)
      self.pwm.set_pulse_width(self.m3, 1530)
      #self.pwm.set_pulse_width(self.m3, -left_y)

   def tilt_s(self, norm_left_y):
      self.pwm.set_pulse_width(self.m3, 1475 + left_y + 30)
      self.pwm.set_pulse_width(self.m1, 1530)
      #self.pwm.set_pulse_width(self.m1, -left_y)

   def tilt_e(self, norm_left_x):
      self.pwm.set_pulse_width(self.m2, 1525 + left_x + 30)
      self.pwm.set_pulse_width(self.m4, 1530)
      #self.pwm.set_pulse_width(self.m4, -left_x)

   def tilt_w(self, norm_left_x):
      self.pwm.set_pulse_width(self.m4, 1475 + left_x + 30)
      self.pwm.set_pulse_width(self.m2, 1530)
      #self.pwm.set_pulse_width(self.m2, -left_x)

   '''
   Function used to control right stick values
   '''
   def right_stick_control(self, right_x, right_y):
      #Check to see what direction it is going in the y axis
      if left_y > 4000:
          self.tilt_n(self.norm_values(right_y-3999))
      elif left_y < -4000:
          self.tilt_s(self.norm_values(right_y+3999))

      #Check to see what direction it is going in the x axis
      if left_x > 4000:
          self.tilt_e(self.norm_values(right_x-3999))
      elif left_x < -4000:
          self.tilt_w(self.norm_values(right_x+3999))

   '''
   Uses the normalized values of right x and y for each of the four functions
   '''
   def rise(self, norm_right_y):
      self.pwm.set_pulse_width(self.m1, 1525 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m2, 1525 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m3, 1525 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m4, 1525 + norm_right_y + 30)

   def dive(self, norm_right_y):
      self.pwm.set_pulse_width(self.m1, 1475 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m2, 1475 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m3, 1475 + norm_right_y + 30)
      self.pwm.set_pulse_width(self.m4, 1475 + norm_right_y + 30)

   def rotate_cw(self, norm_right_x):
      self.pwm.set_pulse_width(self.m5, 1525 + norm_right_x + 30)
      self.pwm.set_pulse_width(self.m6, 1525 + norm_right_x + 30)

   def rotate_ccw(self, norm_right_x):
      self.pwm.set_pulse_width(self.m5, 1475 + norm_right_x + 30)
      self.pwm.set_pulse_width(self.m6, 1475 + norm_right_x + 30)

   """
   Controls the light intensity. Needs power which is a variable from 0 to 100
   and will adjust the pwm (1100-1900) as needed
   """
   def light_control(self, power):
      if power == 0:
         self.pwm.set_pulse_width(self.l1, 1100)
      else
         self.pwm.set_pulse_width(self.l1, 1100 + power*8)

   """
   Control for water pump. Needs speed (pwm variable) and enable variable since
   we are just turning it on or off
   """
   def water_pump_control(self, pwm, en)
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

   import motors
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

      '''
      #Test program for water pump
      print("Test program for water pump")

      rov_cont.arm() 

      while(1):
         pwm_check = int(input("Speed?: "))
         en_check = int(input("Is the pump on or off? (0-1): "))

         rov_cont.water_pump_control(pwm_check, en_check)
         time.sleep(2)
      '''
      
   except KeyboardInterrupt:
      rov_cont.disarm()
