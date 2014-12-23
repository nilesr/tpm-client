#!/usr/bin/env python3

import sys

sys.path.append("../daemon/")

import argparse, time, configparser, curses, traceback, socket, socket_utils

# Vars
sock = False

# Parser 
parser = argparse.ArgumentParser()

parser.add_argument("action", help = "Action to perform.")
parser.add_argument("packages", help = "Packages to install.", nargs = '*', type = str)
args = parser.parse_args()

# Curses
stdscr = curses.initscr()

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

def daemon_get_list_location():
	socket_utils.writeln(sock, "GET LIST")
	return socket_utils.read_line(sock)

if __name__ == '__main__':

	config = configparser.ConfigParser()
	try:
		config.read("/etc/tpm/config.ini")
	except:
		print("Error reading config file at: {0}, exiting...".format("/etc/tpm/config.ini"))
		sys.exit(1)
	
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	server_address = config["daemon"]["socket"]
	
	try:
		sock.connect(server_address)
	except:
		print(traceback.format_exc())
		sys.exit(1)

	daemon_handshake("PROTOCOL 1.0");

	database_location = daemon_get_list_location();

	print(database_location)

	actions.get(args.action,command_not_found)()
	#print(args)
else:
	print("Do not execute indirectly. Prepare to die")
	sys.exit(1)
