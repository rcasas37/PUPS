#C:\Users\lledb\AppData\Local\Programs\Python\Python35-32\%compiles python%this is a test example .py file

# this is a test example .py file
# this file should run on startup based on the bash script I made:
# /etc/init.d/boot_py_script  OR beause of the line I added in:
# /etc/rc.local which runs after everython boots
from decimal import Decimal #Module provides converting a string to decimal
import os
import xml


#Program function definitions
def main():
        capstone_grade = 10        
        capstone_grade1 = 0
        while capstone_grade1 != "66":
                # Test output
                #for i in range(10):
                #        print("Hello, World! %d \n" %(i + 1))

                #get usr input
                capstone_grade1 = input("What grade do you want in capstone? ")
                #capstone_grade = Decimal(capstone_grade1) #convert str to double

                print_grade(capstone_grade)
                capstone_grade += 10

                """Main loop terminator must have "return" if used "break" we return
                operation back to where it left off ie we only get out of loop and 
                continue with main definition execution"""
                if capstone_grade == 100:
                        print_finalgrade(capstone_grade)
                        return;

#fn definition
def print_grade(capstone_grade):
        print("Your capstone grade: %d" %capstone_grade)

#fn definition
def print_finalgrade(capstone_grade):
        print("Goodbye. Your capstone grade: %d \n" %capstone_grade )



class test_class:
        attribute_thing = 90

        """We can get at the attribute attribute_thing
        within our main while loop by simply calling classOjectInstance.attribute_thing
        or classObjectInstance.get_attribute() both work
        """
        def get_attribute(self):
                return self.attribute_thing

##########################################################################
#program execution of all functions etc
if __name__ == '__main__':
        main()
#if we want more fns to execute after main then we put them here
