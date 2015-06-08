#!/usr/bin/python
# -*- coding: utf-8 -*-
#	----------------------------------------------------------------------
#
#	This file is subject to the terms and conditions defined in
#	file 'LICENSE.txt', which is part of this source code package.
#
#   ----------------------------------------------------------------------
#
#	File: server.py
#
#	Last modified: 21/05-2015
#
#	Description:
#		Server to handle all TCP input connections
#
#	Authors:
#		Lars Erik Midtsundstad Storbukås <larserik.storbukas@gmail.com>
#		Ole Eirik Heggelund <oeheggel@gmail.com>
#
#	Website:
#		http://storbukas.no/lightswitch
#
#	----------------------------------------------------------------------
 
# import all from module socket
from socket import *

# importing all from thread
from thread import *

# import self written code to view/modify gpio pins
import gpio_status

# other imports
import os

DIR = "/opt/lightswitch/"
LOCATION = DIR + "lightswitch.py"
LIGTHSWITCH_COMMAND = "sudo python "+ LOCATION + " "

# defining server address and port
host = ''  # 'localhost' or '127.0.0.1' or '' are all same
port = 12345
buffer_size = 1024 # nr of bytes
 
# creating socket object
sock = socket()

# binding socket to a address
sock.bind((host, port))

# listening at the address
sock.listen(5) # 5 denotes the number of clients that can queue
 
def clientthread(conn):
# infinite loop so that function do not terminate and thread do not end.
    while True:
		# wait for input from client
        data = conn.recv(buffer_size)

        # make sure it's not empty
        if not data: continue

        # print input from client to terminal (for debugging purposes)
        print data

        # client wants status of pins
        if("info" in data):
			# get pin status as string representation
			pin_values = gpio_status.get_pins()
			list = gpio_status.get_string_representation(pin_values)

			#print list
            
			# send list to client
			conn.send(list + "\n")

		# clients ends connection
		elif("exit" in data):
			break
        
        # clients sends a command
        else:
			# compose and evaluate command
			command = LIGTHSWITCH_COMMAND + str(data)
			command = command.replace("\0", "").replace("\n", "")
        
			#print(input)        

			# perform system command
			os.system(command)

	# close connection to conn in each thread
	conn.close() # should i do this ?
 
# always listen for connections
while True:
	# accepting incoming connections
    conn, addr = sock.accept()
	
	# creating new thread
	# start new thread takes 1st argument as a function name to be run
	# second is the tuple of arguments to the function.
    start_new_thread(clientthread,(conn,))

# close connection in parent thread
conn.close()
sock.close()