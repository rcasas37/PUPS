#Testing pigpio for PWM and GPIO functions

import pigpio
import time

#Setting up defined pins with variable names (using BCM numbering)
MOTOR = 4 #Board pin 7

#Current microseconds the motor is at
FREQ = 0

#Setting up GPIOs on local pi
pi = pigpio.pi()

#Initializes the motor using a signal of 1500 microseconds (667 Hz) and allows it time to process the signal
def initializeMotor():
    pi.set_servo_pulsewidth(MOTOR, 1500)
    global FREQ
    FREQ = 1500
    print("Sending initialize signal (1500 microseconds)")

#Sends a signal (from 1525-1900 microseconds) that moves the motor in forward with 1900 microseconds being the fastest
def motorForward():
    pi.set_servo_pulsewidth(MOTOR, 1730) #DO NOT go above 1730 as the power supply only allows for 5A and any higher could damage equipment
    global FREQ
    FREQ = 1730
    print("Motor in forward direction")

#Sends a signal (from 1100-1475 microseconds) that moves the motor in reverse with 1100 microseconds being the fastest
def motorReverse():
    pi.set_servo_pulsewidth(MOTOR, 1270) #DO NOT go below 1270 as the power supply only allows for 5A and any higher could damage equipment
    global FREQ
    FREQ = 1270
    print("Motor in reverse direction")

#Used to prevent the motor from harshly stopping and switching directions. Probably won't be used in final program just for test
def slowdown():
    print("Slowing down to 1500 microseconds")

    if FREQ > 1500:
        for x in range(FREQ-1500):
            newFreq = FREQ-(x+1)
            pi.set_servo_pulsewidth(MOTOR, newFreq)
            time.sleep(0.025)
    elif FREQ < 1500:
        for x in range(1500-FREQ):
            newFreq = FREQ+(x+1)
            pi.set_servo_pulsewidth(MOTOR, newFreq)
            time.sleep(0.025)

#Testing the initalization of the motor and moving the motor forward. Will interrupt if CNTL+C is pressed and cleanly exit
try:
    initializeMotor()
    time.sleep(5)
    while(1):
        motorForward()
        time.sleep(5)
        slowdown()
        time.sleep(1)
        motorReverse()
        time.sleep(5)
        slowdown()

except KeyboardInterrupt:
    pi.set_servo_pulsewidth(MOTOR, 0)
    pi.stop()
