import argparse, sys, time
import curses
# Parser 
parser = argparse.ArgumentParser()

parser.add_argument("action", help = "Action to perform.")
parser.add_argument("packages", help = "Packages to install.", nargs = '*', type = str)
args = parser.parse_args()

# Curses
stdscr = curses.initscr()

def write_line(string):
	stdscr.addstr(string)
	stdscr.refresh()
	sys.stdout.flush()

def overwrite_line(string):
	stdscr.addstr(str(curses.getsyx()))
	stdscr.move(curses.getsyx()[0], 0);
	stdscr.clrtoeol();
	stdscr.addstr(string)
	stdscr.refresh()
	sys.stdout.flush()

def command_not_found():
	write_line("Action '" + args.action + "' not found.")

def download():
	pass

def install():
	for package in args.packages:
		overwrite_line("Determining dependencies for packages: " + package + "..."); # Ethan you misspelled dependencies
		# Ok Ethan
		# Functions that start with an "_" are METHODS of a CLASS that you don't want other people using.
		# Functions that start and end with "__" are RESERVED and should NEVER be used to do something other than OBJECT actions, such as being able to use myObject[index] or str(myObject)
	write_line("Done\n")

def remove():
	pass

def purge():
	pass

def search():
	pass

if __name__ == '__main__':
	{
	  "install": install
	, "download": download
	, "remove": remove
	, "purge": purge
	, "search": search
	}.get(args.action,command_not_found)()
	#print(args)
else:
	print("Do not execute indirectly. Prepare to die")
	sys.exit(1)