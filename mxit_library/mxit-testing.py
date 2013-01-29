#!/usr/bin/python

#Creates an SSH connection to the server and binds to a particular address for testing.
import subprocess

enter_username = raw_input("Rational Products MXit Testing User? [rod,brad]")
if enter_username == "brad":
	remote_port = 82
elif enter_username == "rod":
	remote_port = 81
print "Creating connection on port %s" % remote_port
subprocess.call(["ssh","-R %s:127.0.0.1:5000" % remote_port,"root@rationalproducts.co.za"])