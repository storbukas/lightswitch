#!/bin/bash
# -*- coding: utf-8 -*-
#	----------------------------------------------------------------------
#
#	This file is subject to the terms and conditions defined in
#	file 'LICENSE.txt', which is part of this source code package.
#
#   ----------------------------------------------------------------------
#
#	File: lightswitch.sh
#
#	Last modified: 21/05-2015
#
#	Description:
#		@reboot starts the script used to control Light Switch
#
#	Authors:
#		Lars Erik Midtsundstad Storbukås <larserik.storbukas@gmail.com>
#		Ole Eirik Heggelund <oeheggel@gmail.com>
#
#	Website:
#		http://storbukas.no/lightswitch
#
#	----------------------------------------------------------------------

# TODO: Find another way for init.d to start stop the script
# compile python scripts this way:
# 	python -m py_compile fileA.py fileB.py fileC.py

# start the light switch incoming connections server
sudo python /opt/lightswitch/server.py
