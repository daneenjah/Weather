# A little python script that pulls clientraw.txt from a server and parses it.
# It copies the clientraw.txt locally, then pulls the needed into for temp
# and baro. It will then pull the previously recorded temp/baro and compare
# them to current values, providing a way to show if the values are rising,
# falling, or staying the same. The script should be ran in longer intervals
# (10 minutes or so) to provide a proper indication. The script can easily
# be split into two smaller scripts for a taskbar, etc.
# Can also add functionality for anything recorded in clientraw fairly easily.
# This was my second python project, mirroring a bash script I use for my
# status bar on my desktop machine. Enjoy!

import requests
import decimal
import os.path

from config import address

decimal.getcontext().rounding = decimal.ROUND_DOWN

# Pull the clientraw.txt from the server and save it as .cr.txt.
clientraw = requests.get(address)

f = open('.cr.txt', 'wb')
f.write(clientraw.content)
f.close()

# Pull the variables for current temperature and baro from .cr.txt.
f = open('.cr.txt')
for line in f:
    fields = line.strip().split()
    # Array indices start at 0 unlike AWK
    temp = float(fields[4])
    bar = float(fields[6])
f.close()

# Do the math to make them merica.
tempf = str(temp * 1.8 + 32)
barf = str(bar * 0.029529980164712)

# Round temp decimals to 2 places.
tempr = decimal.Decimal(tempf)
temprd = round(tempr,2)

# Round baro decimals to 4 places.
barr = decimal.Decimal(barf)
barrd = round(barr,4)

# Check if the .crt and .crb files exist, if not, write them.
if os.path.isfile('.crt.txt'):
    exists = '1'
else:
    f = open('.crt.txt', 'w')
    f.write("0")
f.close()

if os.path.isfile('.crb.txt'):
    exists = '1'
else:
    f = open('.crb.txt', 'w')
    f.write("0")
f.close()

# Open .cft.txt to pull last known temp.
f = open('.crt.txt')
for line in f:
    fields = line.strip().split()
    # Array indices start at 0 unlike AWK
    ontemp = str(fields[0])
f.close()

# Some if statements for equal to, less than, greater than
# the previously recorded temperature.
if ontemp == (str(temprd)):
    print (str(temprd) + " =")
elif ontemp > (str(temprd)):
    print (str(temprd) + " -")
elif ontemp < (str(temprd)):
    print (str(temprd) + " +")
else:
    print ("We have a problem!")

# Open .cfb.txt to pull last known baro.
f = open('.crb.txt')
for line in f:
    fields = line.strip().split()
    # Array indices start at 0 unlike AWK
    onbar = str(fields[0])
f.close()

# Some if statements for equal to, less than, greater than
# the previously recorded baro.
if onbar == (str(barrd)):
    print (str(barrd) + " =")
elif onbar > (str(barrd)):
    print (str(barrd) + " -")
elif onbar < (str(barrd)):
    print (str(barrd) + " +")
else:
    print ("We have a problem!")

# Write current temp to text file for next run.
with open('.crt.txt', 'w') as f:
    f.write(str(temprd))
f.close()

# Write current baro to text file for next run.
with open('.crb.txt', 'w') as f:
    f.write(str(barrd))
f.close()
