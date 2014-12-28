#!/usr/bin/env python3

import os, sys, BTEdb, argparse, time, configparser, curses, traceback, socket, atexit, platform, json
from daemon_communication import DaemonCommunication
from screen_shim import ScreenShim

""" Global Defines """
daemon = False
config = False
screen = False
database = False

""" Clean up method """
@atexit.register
def clean_up():
	if screen != False:
		screen.end()

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
		try:
			tmp = tuple(package.split(":"))
			parameters =  tmp + (None,) * (3 - len(tmp))

			package = {
				"name": parameters[0],
				"version": parameters[1] if parameters[1] != None else "Latest",
				"arch": parameters[2] if parameters[2] != None else platform.processor()
			}
			
			if TableExists(package["name"]):
				for version in database.Dump(package["name"]):
					print(version)
			else:
				raise Exception("Package doesn't exist in database.")	

			"""
			for version in database.Dump(packagename):
				if version["Version"] == packageversion:
					if version["Version"] != "Latest":
						screen.write_line(version["Dependencies"] + "\n")
					else:
						for version_ in database.Dump(packagename):
							if verison_["Version"] == version["LatestVersion"]:
								write_line(version["Dependencies"] + "\n")
			print(packagename, packageversion, packagearch, "\n")
			"""
		except Exception as e:
			print("Failed to locate package {0}:{1}:{2}".format(package["name"], package["version"], package["arch"]))

def link():
	pass

def unlink():
	pass


def remove():
	pass

def purge():
	pass

def search():
	pass

""" Actions->function() table """
actions = {
	"install": install,
	"link": link,
	"unlink": unlink,
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

	screen = ScreenShim()

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
		database = BTEdb.Database()
		database.OpenDatabase(location)
		print(database.Dump())
	except Exception as e:
		print("Error reading package list " + location + str(e))
		sys.exit(1)

	actions.get(args.action, command_not_found)()
else:
	print("Do not execute indirectly. Prepare to die")
	sys.exit(1)
