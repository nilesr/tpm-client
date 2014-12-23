#!/usr/bin/env python3
import argparse, sys, time
import curses
# Parser 
parser = argparse.ArgumentParser()

parser.add_argument("action", help = "Action to perform.")
parser.add_argument("packages", help = "Packages to install.", nargs = '*', type = str)
args = parser.parse_args()

# BTEdb
config = configparser.ConfigParser()
try:
		self.config.read("/etc/tpm/config.ini")
except:
		print("Error reading config file at: {0}, exiting...".format("/etc/tpm/config.ini"))
		sys.exit(1)
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = 
print >>sys.stderr, 'connecting to %s' % server_address
try:
    sock.connect(server_address)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)



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

if __name__ == '__main__':
	actions.get(args.action,command_not_found)()
	#print(args)
else:
	print("Do not execute indirectly. Prepare to die")
	sys.exit(1)
