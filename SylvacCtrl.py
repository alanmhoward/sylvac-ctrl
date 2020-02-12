# Class definition for the sylvac indicator
# Should be compatible with python 2 and 3 (in particular serial communication requires en/decoding in python3)

from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import input		# Python 2 + 3 compatible method of getting user input strings
import serial				# Communication over usb interface
import time				# Insert pauses due to limited data transfer speed
import sys				# Exit command

# Sylvac indicator class
class Sylvac:

	# Defualt class object - initialise the connection already 
	def __init__(self):
		
		# Setup the serial communication
		SERIALPORT = "/dev/ttyUSB0" # Check dmesg output if unsure (unplug and replug USB cable)
		BAUDRATE = "4800" # Setting this higher causes corruption, 4800 is safe and fast enough
		
		try:
			self.ser = serial.Serial(SERIALPORT, BAUDRATE)
		except:
			print("Cannot open serial connection on " + SERIALPORT)
			exit(1)
		
		# Format of data to be sent and received	
		self.ser.bytesize = serial.SEVENBITS
		self.ser.parity = serial.PARITY_EVEN
		self.ser.stopbits = serial.STOPBITS_TWO
		self.ser.timeout = 0

	# Function to send a command string to the indicator, returns a string upon successful completion	
	def send(self, command):
	
		# Serial port may already be open - ser.open() may be required if this fails
		if self.ser.isOpen():
			try:
				
				self.ser.flushInput() #flush input buffer, discarding all its contents
				self.ser.flushOutput()#flush output buffer, aborting current output
				
				# Add a carriage return and send the requested command (encoded) to the indicator
				command = command + "\r"
				self.ser.write(command.encode())
				
				# Wait at least 100ms for the response
				time.sleep(0.15)
    
				# Read one line from the serial connection and print it
				response = self.ser.readline()
    
				# Decode the response before returning
				return response.decode()
  
			except (Exception) as e:
				print("error communicating...: " + str(e))
				exit(1)
    
		else:
			print("Cannot open serial port")
			exit(1)
	
	# Close the connection	
	def close(self):
		self.ser.close()

	# Print a list of available commands (intended for interactive use)
	def help(self):
		s = ("#################################\n"
			"Command\tDescription\n"
			"#################################\n"
			"?\tCurrent reading\n"
			"REF?\tReference value\n"
			"BAT?\tBattery status (BAT1=ok, BAT0=low)\n"
			"OFF\t Turn off\n"
			"SBY\tEnter standby mode\n"
			"RST\tRe-initialise instrument\n")
		print(s)

# The main() routine only runs if this script is run directly
# If the module is imported in another script this will be ignored
def main():

  # Create a Sylvac object
	syl = Sylvac()

  # If a single argument is passed, send just this as a command
	if ( len(sys.argv) == 2):
	  value = syl.send(sys.argv[1])
	  print(value)

  # If no arguments are passed enter interactive mode
	elif (len(sys.argv)) == 1: 
	  print("Interactive mode, to quit enter 'q'")
	  
	  # Start an infinite loop, exit only when user prompts
	  while True:
		  command = input('Enter command ("q" to quit, "h" for command list)->')
		  assert isinstance(command, str)
		  
		  # quit	
		  if (command=="q"):
			  break
		  
		  # Print a help screen
		  elif (command=="h"):
			  syl.help()

		  # Otherwise send the command and print the reponse
		  else:	
			  response = syl.send(command)
			  print(response)
			  
	else:
	  print("Expected either zero or one arguments")
			  
	# End of if statements		  	
	syl.close()	

# does not execute main if this module was imported
if __name__ == "__main__": 
	main()
