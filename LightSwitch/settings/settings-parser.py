#!/usr/bin/python
# -*- coding: utf-8 -*-
#	----------------------------------------------------------------------
#
#	This file is subject to the terms and conditions defined in
#	file 'LICENSE.txt', which is part of this source code package.
#
#   ----------------------------------------------------------------------
#
#	File: settings-parser.py
#
#	Last modified: 21/05-2015
#
#	Description:
#		Parses the input in SETTINGS-file to valid actions on Light Switch
#		
#		To be run by cron job to constantly check for changes in sensor
#		values that will affect the status of output pins in Light Switch
#
#	Authors:
#		Lars Erik Midtsundstad Storbukås <larserik.storbukas@gmail.com>
#		Ole Eirik Heggelund <oeheggel@gmail.com>
#
#	Website:
#		http://storbukas.no/lightswitch
#
#	----------------------------------------------------------------------

# imports
import os

# temporary sensor input
sensors = [788]

DIR = "/opt/lightswitch/settings/"
LIGTHSWITCH_SCRIPT_LOCATION = DIR + "ligthswitch.py"
FILENAME = DIR + "SETTINGS" # settings file
EXCEPTIONS = DIR + "EXCEPTIONS" # exceptions file
LIGHTSWITCH_COMMAND = "sudo python "+ LIGHTSWITCH_SCRIPT_LOCATION + " "
DELIMITER = "|"

##############################################################################
# methods for getting information of hardware, and interpreting settings

def interpret_pins(pins):
	"""interprete number of pins affected (separated by - or , ) according to settings file"""
	# hyphen: pins is in a range
	if "-" in pins:
		# split content on hyphen
		pins = pins.split("-")

		# add pins in a list
		newlist = []
		for i in range(int(pins[0]), int(pins[1])+1):
			newlist.append(i)

		pins = newlist

	# comma separated pins
	elif "," in pins:
		# split content on commas
		pins = pins.split(",")

		# update value as ints
		for i in range(len(pins)):
			pins[i] = int(pins[i])

	# single pin
	else:
		pins = [int(pins)]
		
	return pins


def compare_value(sensor_value, settings_value):
	"""compares value of sensor to that of settings"""
	sensor_value = float(sensor_value)
	settings_value = float(settings_value)
	
	if(sensor_value < settings_value): # less than settings value
		return -1
	elif(sensor_value > settings_value): # more than settings value
		return 1
	else:
		return 0
	

def relative_value(value):
	"""returns the relative value based on settings (less, exactly, more)"""
	if(value == "less"):
		return -1
	elif(value == "more"):
		return 1
	else:
		return 0
	

def dependent_value(value):
	"""returns if it is dependent, meaning that if the requirement is false; the value is going to be the opposite"""
	if(value == "else"):
		return True
	else:
		return False


def get_sensor_value(sensor_pin):
	"""return sensor value on 'sensor_pin'"""
	return sensors[int(sensor_pin)] # TODO: must be changed to real sensor values evetually


def get_status(status):
	"""returns boolean value based on settings ON/OFF"""
	if(status=="ON"):
		return True
	else:
		return False

##############################################################################
# methods for modifying hardware and output values

def perform_action(pins, action):
	"""update status on GPIO-pins 'pins' with 'action'"""
    action = ("off","on")[action] # on if True, off if False

    # perform system call
    os.system(LIGHTSWITCH_COMMAND + str(action) + " " + str(pins))


def modify_output(settings):
	"""update output values (GPIO pins)"""
	# go trough every line in settings file
	for line in settings:
		# settings fields
		settings_pins = line[0]	# output pins
		settings_sensor = line[1] # input pins / sensor pins
		settings_sensor_value = line[2]	# sensor pin value
		settings_relation = line[3]	# relation to sensor value (less, more, exactly)
		settings_action = line[4] # action to do if sensor matches relation to value defined in settings
		settings_dependent = line[5] # if set to 'else', !action should happen if it doesn't match relation

		# get sensor value
		sensor_value = get_sensor_value(settings_sensor)
		settings_value = settings_sensor_value

		# if relation betwen sensor_value and settings_value matches line in settings
		if(compare_value(sensor_value, settings_value) == relative(settings_relation)):
			perform_action(settings_pins, get_status(settings_action)) # perform action with value found in settings

		# if relation between sensor_value and settings_value do NOT match, but pin is dependent, opposite should happen
		elif((value(sensor_value, settings_value) != relative_value(settings_relation)) and dependent_value(settings_dependent)):
			perform_action(settings_pins, not get_status(settings_action)) # perform action with opposite value of found in settings

##############################################################################
# methods for adding and removing exceptions 					<<< UNFINISHED

# NOT FINISHED
def notify_change(pins, action, filename):
	"""notifies change of pins, used to add exception if action goes against settings"""
	# if pins affected overlaps with some settings-value, add an exception

	# open exception file for reading and writing
	file = open(filename, 'r')

	# write exception to file
	file.write("pin_number|time_added") # how long should an exception last?

	# close file
	file.close()

# NOT FINISHED
def remove_old_exceptions(filename):
	"""removes expired exceptions from file"""
	# open exception file for reading and writing
	file = open(filename, 'r+')

	# go trough all elements, and remove old ones
	exceptions = file.readlines

	# close file
	file.close()

# NOT FINISHED
def get_exceptions(filename):
	"""returns a lists over pins that should not be altered due to exceptions"""
	# open exception file for reading
	file = open(filename, 'r')

	# read every line from file
	exceptions = file.readlines()

	# close file
	file.close()

	return exceptions

##############################################################################
# methods for adding, changing and removing settings 			<<< UNFINISHED

def add_setting(setting):
	"""adds setting to settings file"""

def change_setting(setting_id, new_setting):
	"""modifies a field in the settings file with new_setting value"""

def remove_setting(setting_id):
	"""deletes a field in the settings with setting_id"""

def activate_setting(setting_id):
	"""activates a previously used setting"""

def deactivate_setting(setting_id):
	"""temorary removes a setting"""


##############################################################################
# main methods for running scripts

def main():
	"""read all settings and update board"""
	# open settings file for reading and get all lines
	file = open(FILENAME, "r")
	settings = file.readlines()
	
	# split every line on DELIMITER and remove newline characters
	for i in range(len(settings)):
		settings[i] = settings[i].replace("\n", "").split(DELIMITER)
	
	# modify input
	modify_output(settings)

if __name__ == "__main__":
	main()