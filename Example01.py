# Compatability between python 2 and 3
from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import time

# Load all functions from SylvacCtrl
from SylvacCtrl import *

# Create an indicator object
syl = Sylvac()

# Wake up the sensor and wait until it is running
syl.send('ON')
time.sleep(0.5)

# Read the current value (if the indicator is still initialising a blank string will be returned)
reading = ""
while (reading == ""):
  reading = syl.send('?')
print(reading)

# Turn off the indicator
syl.send('OFF')
