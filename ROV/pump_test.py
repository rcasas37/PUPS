#Pump test


import pigpio
import time

#Setting up defined pins for IN1, IN2, and PWM
PWM = 19
IN1 = 13
IN2 = 6

#Setting up GPIOs on local pi
pi = pigpio.pi()

#Setting up PWM pin to 50% duty cycle
pi.set_PWM_dutycycle(PWM, 192)

#Function used to switch the pump to forward, reverse, or stopped
def pump_control(x):
    print("x = " + str(x))
    if int(x) == 0:
        pi.write(IN1, 0)
        pi.write(IN2, 0)
        print("Motor stopped")
    elif int(x) == 1:
        pi.write(IN1, 0)
        pi.write(IN2, 1)
        print("IN1 = " + str(pi.read(IN1)))
        print("IN2 = " + str(pi.read(IN2)))
        print("Motor forward")
    elif int(x) == 2:
        pi.write(IN1, 1)
        pi.write(IN2, 0)
        print("Motor reverse")

#while-loop that constantly runs checking to see what the user wanted the pump to do
try:
    pump_control(0)
    time.sleep(5)
    while(1):
        pump_state = input("Pump in forward or reverse? (1 or 2) ")
        print("Pump state = " + pump_state)
        pump_control(pump_state)
        time.sleep(10)

except KeyboardInterrupt:
    pi.set_PWM_dutycycle(PWM, 0)
    pi.stop()





