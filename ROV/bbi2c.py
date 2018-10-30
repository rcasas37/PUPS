#Test program for Bit-Bang I2C line

import pigpio
import time

#pi = pigpio.pi()

class BitBangI2C(object):
   """
   Bitbang of I2C line using pigpio
   """

   # GPIO configuration and frequency constants
   SDA = 4
   SCL = 5
   CF = 50000

   # Pigpio BB Constants
   BB_END = 0
   BB_ESCAPE = 1
   BB_START = 2
   BB_STOP = 3
   BB_ADDRESS = 4
   BB_FLAGS = 5
   BB_READ = 6
   BB_WRITE = 7

   def __init__(self, pi=0):
      self.pi = pi

   def stop(self):
      #Stop pigpio connection
      self.pi.stop()

   def open_bus(self):
      """
      Creates bitbang handle with given SDA/SCL GPIO and I2C freq (CF)
      """
      self.handle = self.pi.bb_i2c_open(self.SDA, self.SCL, self.CF)

   def close_bus(self):
      """
      Closes open bitbang handle
      """
      self.handle = self.pi.bb_i2c_open(self.SDA, self.SCL, self.CF)

   def read(self, address, pointer_reg, read_bytes):
      """
      Performs I2C read operation on a particular address. Requires the 7-bit
      I2C address, the pointer register to write to, and the number of bytes to
      read from the pointer register
      """
      read_bytes += 1
      arg_list = [self.BB_ADDRESS, address, self.BB_START, self.BB_WRITE,
                  self.BB_ESCAPE, pointer_reg, self.BB_START, self.BB_READ,
                  read_bytes, self.BB_STOP, self.BB_END]
      count, data = self.pi.bb_i2c_zip(self.SDA, arg_list)
      return data


   def write(self, address, pointer_reg, data_array):
      """
      Performs I2C write operation on a particular address. Requires the 7-bit
      I2C address, the pointer register and a data array of the data package to send
      """
      read_bytes += 1
      arg_list = [self.BB_ADDRESS, address, self.BB_START, self.BB_WRITE,
                  len(data_array)+1, pointer_reg] + data_array + [self.BB_STOP, self.BB_END]
      count, data = self.pi.bb_i2c_zip(self.SDA, arg_list)
      return data

class BNO055(object):
   """
   Class used to interface with the BNO055 Orientation Sensor. This is a modified version
   of the Adafruit BNO055 class created by Tony DiCola which uses a bit bang created I2C
   line using the pigpio class
   """

   # Constants needed for BNO055
   # I2C addresses
   BNOO55_ADDRESS_A                     = 0x28
   BNO055_ADDRESS_B			= 0x29
   BNO055_ID				= 0xA0

   # Page id register definition
   BNO055_PAGE_ID_ADDR			= 0x07

   # Page 0 register definition start
   BNO055_CHIP_ID_ADDR			= 0x00
   BNO055_ACCEL_REV_ID_ADDR		= 0x01
   BNO055_MAG_REV_ID_ADDR		= 0x02
   BNO055_GYRO_REV_ID_ADDR		= 0x03
   BNO055_SW_REV_ID_LSB_ADDR		= 0x04
   BNO055_SW_REV_ID_MSB_ADDR		= 0x05
   BNO055_BL_REV_ID_ADDR		= 0x06

   # Accel data register
   BNO055_ACCEL_DATA_X_LSB_ADDR		= 0x08
   BNO055_ACCEL_DATA_X_MSB_ADDR		= 0x09
   BNO055_ACCEL_DATA_Y_LSB_ADDR		= 0x0A
   BNO055_ACCEL_DATA_Y_MSB_ADDR		= 0x0B
   BNO055_ACCEL_DATA_Z_LSB_ADDR		= 0x0C
   BNO055_ACCEL_DATA_Z_MSB_ADDR		= 0x0D

   # Mag data register
   BNO055_MAG_DATA_X_LSB_ADDR		= 0x0E
   BNO055_MAG_DATA_X_MSB_ADDR		= 0x0F
   BNO055_MAG_DATA_Y_LSB_ADDR		= 0x10
   BNO055_MAG_DATA_Y_MSB_ADDR		= 0x11
   BNO055_MAG_DATA_Z_LSB_ADDR		= 0x12
   BNO055_MAG_DATA_Z_MSB_ADDR		= 0x13

   # Gyro data register
   BNO055_GYRO_DATA_X_LSB_ADDR		= 0x14
   BNO055_GYRO_DATA_X_MSB_ADDR		= 0x15
   BNO055_GYRO_DATA_Y_LSB_ADDR		= 0x16
   BNO055_GYRO_DATA_Y_MSB_ADDR		= 0x17
   BNO055_GYRO_DATA_Z_LSB_ADDR		= 0x18
   BNO055_GYRO_DATA_Z_MSB_ADDR		= 0x19

   # Euler data register
   BNO055_EULER_H_LSB_ADDR		= 0x1A
   BNO055_EULER_H_MSB_ADDR		= 0x1B
   BNO055_EULER_R_LSB_ADDR		= 0x1C
   BNO055_EULER_R_MSB_ADDR		= 0x1D
   BNO055_EULER_P_LSB_ADDR		= 0x1E
   BNO055_EULER_P_MSB_ADDR		= 0x1F

   # Quaternion data register
   BNO055_QUATERNION_DATA_W_LSB_ADDR	= 0x20
   BNO055_QUATERNION_DATA_W_MSB_ADDR	= 0x21
   BNO055_QUATERNION_DATA_X_LSB_ADDR	= 0x22
   BNO055_QUATERNION_DATA_X_MSB_ADDR	= 0x23
   BNO055_QUATERNION_DATA_Y_LSB_ADDR	= 0x24
   BNO055_QUATERNION_DATA_Y_MSB_ADDR	= 0x25
   BNO055_QUATERNION_DATA_Z_LSB_ADDR	= 0x26
   BNO055_QUATERNION_DATA_Z_MSB_ADDR	= 0x27

   # Linear acceleration data registers
   BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR	= 0x28
   BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR	= 0x29
   BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR	= 0x2A
   BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR	= 0x2B
   BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR	= 0x2C
   BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR	= 0x2D

   # Gravity data registers
   BNO055_GRAVITY_ACCEL_DATA_X_LSB_ADDR	= 0x2E
   BNO055_GRAVITY_ACCEL_DATA_X_MSB_ADDR	= 0x2F
   BNO055_GRAVITY_ACCEL_DATA_Y_LSB_ADDR	= 0x30
   BNO055_GRAVITY_ACCEL_DATA_Y_MSB_ADDR	= 0x31
   BNO055_GRAVITY_ACCEL_DATA_Z_LSB_ADDR	= 0x32
   BNO055_GRAVITY_ACCEL_DATA_Z_MSB_ADDR	= 0x33

   # Temperature data register
   BNO055_TEMP_DATA			= 0x34

   # Status registers
   BNO055_CALIB_STAT_ADDR		= 0x35
   BNO055_SELFTEST_RESULT_ADDR		= 0x36
   BNO055_INTR_STAT_ADDR		= 0x37

   BNO055_SYS_CLK_STAT_ADDR		= 0x38
   BNO055_SYS_STAT_ADDR			= 0x39
   BNO055_SYS_ERR_ADDR			= 0x3A

   # Unit selection register
   BNO055_UNIT_SEL_ADDR			= 0x3B
   BNO055_DATA_SELECT_ADDR		= 0x3C

   # Mode registers
   BNO055_OPR_MODE_ADDR			= 0x3D
   BNO055_PWR_MODE_ADDR			= 0x3E

   BNO055_SYS_TRIGGER_ADDR		= 0x3F
   BNO055_TEMP_SOURCE_ADDR		= 0x40

   # Axis remap registers
   BNO055_AXIS_MAP_CONFIG_ADDR		= 0x41
   BNO055_AXIS_MAP_SIGN_ADDR		= 0x42

   # Axis remap values
   BNO055_REMAP_X			= 0x00
   BNO055_REMAP_Y			= 0x01
   BNO055_REMAP_Z			= 0x02
   BNO055_REMAP_POSITIVE		= 0x00
   BNO055_REMAP_NEGATIVE		= 0x01

   # SIC registers
   BNO055_SIC_MATRIX_0_LSB_ADDR		= 0x43
   BNO055_SIC_MATRIX_0_MSB_ADDR		= 0x44
   BNO055_SIC_MATRIX_1_LSB_ADDR		= 0x45
   BNO055_SIC_MATRIX_1_MSB_ADDR		= 0x46
   BNO055_SIC_MATRIX_2_LSB_ADDR		= 0x47
   BNO055_SIC_MATRIX_2_MSB_ADDR		= 0x48
   BNO055_SIC_MATRIX_3_LSB_ADDR		= 0x49
   BNO055_SIC_MATRIX_3_MSB_ADDR		= 0x4A
   BNO055_SIC_MATRIX_4_LSB_ADDR		= 0x4B
   BNO055_SIC_MATRIX_4_MSB_ADDR		= 0x4C
   BNO055_SIC_MATRIX_5_LSB_ADDR		= 0x4D
   BNO055_SIC_MATRIX_5_MSB_ADDR		= 0x4E
   BNO055_SIC_MATRIX_6_LSB_ADDR		= 0x4F
   BNO055_SIC_MATRIX_6_MSB_ADDR		= 0x50
   BNO055_SIC_MATRIX_7_LSB_ADDR		= 0x51
   BNO055_SIC_MATRIX_7_MSB_ADDR		= 0x52
   BNO055_SIC_MATRIX_8_LSB_ADDR		= 0x53
   BNO055_SIC_MATRIX_8_MSB_ADDR		= 0x54

   # Accelerometer Offset registers
   ACCEL_OFFSET_X_LSB_ADDR		= 0x55
   ACCEL_OFFSET_X_MSB_ADDR		= 0x56
   ACCEL_OFFSET_Y_LSB_ADDR		= 0x57
   ACCEL_OFFSET_Y_MSB_ADDR		= 0x58
   ACCEL_OFFSET_Z_LSB_ADDR		= 0x59
   ACCEL_OFFSET_Z_MSB_ADDR		= 0x5A

   # Magnetometer Offset registers
   MAG_OFFSET_X_LSB_ADDR		= 0x5B
   MAG_OFFSET_X_MSB_ADDR		= 0x5C
   MAG_OFFSET_Y_LSB_ADDR		= 0x5D
   MAG_OFFSET_Y_MSB_ADDR		= 0x5E
   MAG_OFFSET_Z_LSB_ADDR		= 0x5F
   MAG_OFFSET_Z_MSB_ADDR		= 0x60

   # Gyroscope Offset registers
   GYRO_OFFSET_X_LSB_ADDR		= 0x61
   GYRO_OFFSET_X_MSB_ADDR		= 0x62
   GYRO_OFFSET_Y_LSB_ADDR		= 0x63
   GYRO_OFFSET_Y_MSB_ADDR		= 0x64
   GYRO_OFFSET_Z_LSB_ADDR		= 0x65
   GYRO_OFFSET_Z_MSB_ADDR		= 0x66

   # Radius registers
   ACCEL_RADIUS_LSB_ADDR		= 0x67
   ACCEL_RADIUS_MSB_ADDR		= 0x68
   MAG_RADIUS_LSB_ADDR			= 0x69
   MAG_RADIUS_MSB_ADDR			= 0x6A

   # Power modes
   POWER_MODE_NORMAL			= 0x00
   POWER_MODE_LOWPOWER			= 0x01
   POWER_MODE_SUSPEND			= 0x02

   # Operation mode settings
   OPERATION_MODE_CONFIG		= 0x00
   OPERATION_MODE_ACCONLY		= 0x01
   OPERATION_MODE_MAGONLY		= 0x02
   OPERATION_MODE_GYRONLY		= 0x03
   OPERATION_MODE_ACCMAG		= 0x04
   OPERATION_MODE_ACCGYRO		= 0x05
   OPERATION_MODE_MAGGYRO		= 0x06
   OPERATION_MODE_AMG			= 0x07
   OPERATION_MODE_IMUPLUS		= 0x08
   OPERATION_MODE_COMPASS		= 0x09
   OPERATION_MODE_M4G			= 0x0A
   OPERATION_MODE_NDOF_FMC_OFF		= 0x0B
   OPERATION_MODE_NDOF			= 0x0C

   def __init__(self, rst=None, address=0, i2c=None, pi=None, **kwargs):
      self.address = self.BNO055_ADDRESS_A
      # If reset pin is provided then save it and save pigpio.pi reference
      self.rst = rst
      self.pi = pi
      # Setting up reset pin and setting it high
      self.pi.set_mode(self.rst, pigpio.OUTPUT)
      self.pi.write(self.rst, 1)
      # Wait 650 milliseconds in case resetting high resets the chip
      time.sleep(0.65)

      # Use the bitbang I2C
      self.i2c_channel = BitBangI2C()
      self.i2c_channel.open_bus()

   def _write_bytes(self, address, data, ack=True):
      # Write a list of 8-bit values starting at the provided register address
      self.i2c_channel.write(self.SDA, address, data)

   def _write_byte(self, address, value,ack=True):
      # Write an 8-bit value to the provided register address.
      self.i2c_channel.write(self.SDA, address, value)

   def _read_bytes(self, address, length):
      # Read a number of unsigned byte values starting from the provided address
      count, data = self.i2c_channel.read(self.SDA, address, length)
      return data

   def _read_byte(self, address):
      # Read an 8-bit unsigned value from the provided register address
      count, data = self.i2c_channel.read(self.SDA, address, 1)
      return data

   def _read_signed_byte(self, address):
      # read an 8-bit signed value from the provided register address
      count, data = self.i2c_channel.read(self.SDA, address, 1)
      if data > 127:
         return data - 256
      else:
         return data

   def _config_mode(self):
      # Enter configuration mode
      self.set_mode(self.OPERATION_MODE_CONFIG)

   def _operation_mode(self):
      # Enter operation mode to read sensor data
      self.set_mode(self._mode)

   def begin (self, mode=OPERATION_MODE_NDOF):
      """
      Initialize the BNO055 sensor. Must be called once before any other BNO055
      library functions. Will return True if the BNO055 was successfully initialized
      """
      # Save the desired normal operation mode
      self.mode = mode

      # First send a throw-away command and ignore any response or I2C errors
      # just to make sure that the BNO is in a good state and ready to accept
      # commands (this seems to be necessary after a hard power down).
      try:
         self._write_byte(self.BNO055_PAGE_ID_ADDR, 0, ack=False)
      except IOError:
         # Swallow an IOError to allow it to start up
         pass

      # Make sure we're in config mode and on page 0
      self._config_mode()
      self._write_byte(BNO055_PAGE_ID_ADDR, 0)
      # Check the chip ID
      bno_id = self._read_byte(BNO055_CHIP_ID_ADDR)

      if bno_id != self.BNO055_ID:
         return False

      # Reset the device
      if self._rst is not None:
         # Use hardware reset pin if provided
         self.pi.write(self._rst, 0)
         time.sleep(0.01)
         self.pi.write(self._rst, 1)
      else:
         # Use the reset command if not provided HW reset pin
         self._write_byte(self.BNO055_SYS_TRIGGER_ADDR, 0x20, ack=False)

      # Wait 650ms after resetting chip to be ready
      time.sleep(0.65)

      # Set to normal power mode
      self._write_byte(self.BNO055_PWR_MODE_ADDR, self.POWER_MODE_NORMAL)

      # Default to internal oscillator
      self._write_byte(self.BNO055_SYS_TRIGGER_ADDR, 0x00)

      # Enter normal operation mode
      self._operation_mode()
      return True

   def set_mode(self, mode):
      """
      Set operation mode for BNO055 sensor.
      """
      self._write_byte(self.BNO055_OPR_MODE_ADDR, mode & 0xFF)
      time.sleep(0.03)

   
