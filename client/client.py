#!/usr/bin/env python3

import os, sys, BTEdb, argparse, time, configparser, curses, traceback, socket, atexit
from daemon_communication import DaemonCommunication
from curses_shim import CursesShim

""" Defines """
daemon = False
curses = False
config = False
database = False

""" Clean up method """
@atexit.register
def clean_up():
	if curses != False:
		curses.endwin()
		curses.nocbreak()
		stdscr.keypad(False)
		curses.echo()

	if daemon != False:
		if daemon.connected == True:
			try:
				daemon.close()
			except:
				pass;

""" Arg. parser """
parser = argparse.ArgumentParser()

""" Arg. parser actions """
parser.add_argument("action", help = "Action to perform.")
parser.add_argument("arguments", help = "Action arguments.", nargs = '*', type = str)

""" Actions """

def command_not_found():
	screen.write_line("Action '" + args.action + "' not found.")

def download():
	pass

def install():
	for package in args.arguments:
		parameters = package.split(":")
		packagename = parameters[0]
		#overwrite_line("Determining dependencies for packages: '" + packagename + "'.")
		if len(parameters) < 3:
			packagearch = "Default"
			if len(parameters) < 2:
				packageversion = "Latest"
			else:
				packageversion = parameters[1]
		else:
			packagearch = parameters[2]
			packageversion = parameters[1]
		for version in database.Dump(packagename):
			if version["Version"] == packageversion:
				if version["Version"] != "Latest":
					screen.write_line(version["Dependencies"] + "\n")
				else:
					for version_ in database.Dump(packagename):
						if verison_["Version"] == version["LatestVersion"]:
							write_line(version["Dependencies"] + "\n")
		screen.write_line(packagename, packageversion, packagearch, "\n")

def remove():
	pass

def purge():
	pass

def search():
	pass

""" Actions->function() table """
actions = {
	"install": install,
	"download": download,
	"remove": remove,
	"purge": purge,
	"search": search
}

if __name__ == '__main__':

	""" Run args parser """
	args = parser.parse_args()

	if not os.geteuid() == 0:
		print("Please run tpm-client as root.")
		sys.exit(1)

	config = configparser.ConfigParser()
	try:
		config.read("/etc/tpm/config.ini")
	except:
		print("Error reading config file at: {0}, exiting...".format("/etc/tpm/config.ini"))
		sys.exit(1)
	
	""" DaemonCommunication Object """
	daemon = DaemonCommunication(config["daemon"]["socket"], "PROTOCOL 1.0")

	daemon.handshake();


	try:
		location = daemon.get_list()
		database = BTEdb.Database(location)
	except:
		print("Error reading package list " + location)
		sys.exit(1)

	database = BTEdb.Database(daemon.get_list());

	actions.get(args.action, command_not_found)()
else:
	print("Do not execute indirectly. Prepare to die")
	sys.exit(1)