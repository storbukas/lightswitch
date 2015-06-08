#!/usr/bin/python
# -*- coding: utf-8 -*-
#	----------------------------------------------------------------------
#
#	This file is subject to the terms and conditions defined in
#	file 'LICENSE.txt', which is part of this source code package.
#
#   ----------------------------------------------------------------------
#
#	File: lightswitch.py
#
#	Last modified: 21/05-2015
#
#	Description:
#		Main control application for output pins (GPIO) on Light Switch
#
#	Authors:
#		Lars Erik Midtsundstad Storbukås <larserik.storbukas@gmail.com>
#		Ole Eirik Heggelund <oeheggel@gmail.com>
#
#	Website:
#		http://storbukas.no/lightswitch
#
#	----------------------------------------------------------------------

# import wiringpi to modify gpio pins
import wiringpi2 as wiringpi

# import self written code to view/modify gpio pins
import gpio_status

# other imports
import sys


# make sure input is correct
if (not len(sys.argv) > 2):
    print ("Usage: lightswitch.py action pins")
    sys.exit()


# decide action based on input (on/off)
action = 0
if (str(sys.argv[1]).lower() == "on"):
    action = 1
elif (str(sys.argv[1]).lower() == "off"):
    action = 0


# get pins to perform action on
liste = []
if (str(sys.argv[2]).strip().lower() == "all"): # all pins
    for i in range(1,7):
        liste.append(i)

elif("-" in str(sys.argv[2])): # if hyphen, it's a range
    var = str(sys.argv[2]).split("-")
    for i in range(int(var[0]),int(var[1])+1):
        liste.append(i)

elif("," in str(sys.argv[2])): # if comma separated list
    var = str(sys.argv[2]).split(",")
    for i in range(len(var)):
        liste.append(int(var[i]))

else: # single pin number
    liste.append(int(sys.argv[2]))


# handles out the action on pins in the list
def perform(pins, action):
	# perform action on hardware
    wiringpi.wiringPiSetup()
    for i in pins:
        wiringpi.pinMode(i-1,action) # -1 to be able to write logical pin numbers as input

    # update gpio-status
    gpio-status.set_pins(pins, action)


# perform action on given pins
perform(liste, action)