#C:\Users\lledb\AppData\Local\Programs\Python\Python35-32\%compiles python%this is a test example .py file

# this is a test example .py file
# this file should run on startup based on the bash script I made:
# /etc/init.d/boot_py_script  OR beause of the line I added in:
# /etc/rc.local which runs after everython boots
from decimal import Decimal #Module provides converting a string to decimal

capstone_grade = 0

#Program function definitions
def main():
	while True:
		# Test output
		#for i in range(10):
		#	print("Hello, World! %d \n" %(i + 1))

		#get usr input
		capstone_grade1 = input("What grade do you want in capstone? ")
		capstone_grade = Decimal(capstone_grade1) #convert str to double

		print_grade(capstone_grade)

		"""Main loop terminator must have "return" if used "break" we return
		operation back to where it left off ie we only get out of loop and 
		continue with main definition execution"""
		if capstone_grade == 100:
			print_finalgrade(capstone_grade)
			return 0;
			
#fn definition
def print_grade(capstone_grade):
	print("Your capstone grade: %d" %capstone_grade)

#fn definition
def print_finalgrade(capstone_grade):
	print("Goodbye. Your capstone grade: %d" %capstone_grade )



##########################################################################
#program execution of all functions etc
main()
#if we want more fns to execute after main then we put them here
