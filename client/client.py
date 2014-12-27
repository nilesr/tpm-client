#!/usr/bin/env python3

import sys, BTEdb

sys.path.append("../daemon/")

import argparse, time, configparser, curses, traceback, socket, socket_utils, atexit


# Curses
stdscr = curses.initscr()

# Atexit
@atexit.register
def clean_up():
	curses.endwin()
	if sock != False and connected == True:
		try:
			socket_utils.writeln(sock, "GOODBYE")
			print(socket_utils.read_line(sock))
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()
		except:
			pass;
	


# Vars
connected = False;
sock = False

# Parser 
parser = argparse.ArgumentParser()

parser.add_argument("action", help = "Action to perform.")
parser.add_argument("packages", help = "Packages to install.", nargs = '*', type = str)
args = parser.parse_args()

def write_line(*args):
	string = " ".join(args)
	stdscr.addstr(string)
	stdscr.refresh()
	sys.stdout.flush()

def overwrite_line(*args):
	string = " ".join(args)
	stdscr.addstr(str(curses.getsyx()))
	stdscr.move(curses.getsyx()[0], 0)
	stdscr.clrtoeol()
	stdscr.addstr(string)
	stdscr.refresh()
	sys.stdout.flush()

def command_not_found():
	write_line("Action '" + args.action + "' not found.")

# Actions #

def download():
	pass

def install():
	for package in args.packages:
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
		for version in db.Dump(packagename):
			if version["Version"] == packageversion:
				if version["Version"] != "Latest":
					write_line(version["Dependencies"] + "\n")
				else:
					for version_ in db.Dump(packagename):
						if verison_["Version"] == version["LatestVersion"]:
							write_line(version["Dependencies"] + "\n")
		write_line(packagename, packageversion, packagearch, "\n")
def remove():
	pass

def purge():
	pass

def search():
	pass

actions = {
	"install": install,
	"download": download,
	"remove": remove,
	"purge": purge,
	"search": search
}


def daemon_handshake(protocol_version):
	socket_utils.writeln(sock, protocol_version)

	if socket_utils.read_line(sock) != protocol_version:
		print("Daemon Handshake Failed.");
		sys.exit(1)

def daemon_get_list():
	socket_utils.writeln(sock, "GET LIST")
	location = socket_utils.read_line(sock)

	try:
		if location[:5] == "LIST ":
			location = location[5:]
			db = BTEdb.Database(location)
			return db
		else:
			raise Exception("Error")
	except:
		print("Error reading list. " + location)
		sys.exit(1)

if __name__ == '__main__':

	config = configparser.ConfigParser()
	try:
		config.read("/etc/tpm/config.ini")
	except:
		print("Error reading config file at: {0}, exiting...".format("/etc/tpm/config.ini"))
		sys.exit(1)
	
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	sock.settimeout(10)
	server_address = config["daemon"]["socket"]
	
	try:
		sock.connect(server_address)
		connected = True;
	except:
		print("Failed to connect to dameon, it is either in use, or off.")
		sys.exit(1)

	daemon_handshake("PROTOCOL 1.0");

	db = daemon_get_list();

	actions.get(args.action,command_not_found)()
	#print(args)
else:
	print("Do not execute indirectly. Prepare to die")
	sys.exit(1)
