#!/usr/bin/python
# -*- coding: utf-8 -*-
#	----------------------------------------------------------------------
#
#	This file is subject to the terms and conditions defined in
#	file 'LICENSE.txt', which is part of this source code package.
#
#   ----------------------------------------------------------------------
#
#	File: gpio_status.py
#
#	Last modified: 21/05-2015
#
#	Description:
#		Implements methods for setting and returning status on output pins
#		Reads and writes to PIN_STATUS file
#
#	Authors:
#		Lars Erik Midtsundstad Storbukås <larserik.storbukas@gmail.com>
#		Ole Eirik Heggelund <oeheggel@gmail.com>
#
#	Website:
#		http://storbukas.no/lightswitch
#
#	----------------------------------------------------------------------

DIR = "/opt/lightswitch/"
LOCATION = DIR + "values/"
FILENAME = LOCATION + "PIN_STATUS"
DELIMITER = "|"

# TODO: Complete path on methods or implemented to fit this program?

##############################################################################
# methods for setting and getting pin information

def get_pins():
	"""returns a list of ints with either 1 or 0 (active / unactive)"""
	# get first line from PIN_STATUS
	line = read_from_file(FILENAME)

	# put data into int-array
	pins = []
	for i in line.split(DELIMITER):
		pins.append(int(i))

	return pins


def get_string_representation(pin_array):
	"""returns a string representation of an array of pins with DELIMITER as delimiter"""
	return DELIMITER.join(map(str, pin_array)) 


def set_pins(pins, action):
	"""modifies PIN_STATUS-file pins with action"""
	# get current pin status
	pin_values = get_pins()

	# modify pins with input
	for i in pins:
		pin_values[int(i)-1] = action

	# concatenate pin values to string
	string_representation = get_string_representation(pin_values)
	# write string representation to file
	write_to_file(string_representation, FILENAME)


def set_pin(pin, action):
	"""modifies PIN_STATUS-file pin with action"""
	# use multipin method to save space
	set_pins([pin], action)

##############################################################################
# methods for reading and writing to file (updating gpio status)

def write_to_file(content, filename):
	"""writes 'content' to 'filename'"""
	# open file for writing
	file = open(filename, 'w')

	# delete whatever is in the file from before
	file.truncate()

	# write content to file
	file.write(content)

	# close file
	file.close()


def read_from_file(filename):
	"""return first line from 'filename'"""
	# open file for reading
	file = open(filename, 'r')

	# read one line from file
	line = file.readline()

	# close file
	file.close()

	return line