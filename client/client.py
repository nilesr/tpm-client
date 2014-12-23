#!/usr/bin/env python3
import argparse, sys, time
import curses
# Parser 
parser = argparse.ArgumentParser()

parser.add_argument("action", help = "Action to perform.")
parser.add_argument("packages", help = "Packages to install.", nargs = '*', type = str)
args = parser.parse_args()

# Curses
stdscr = curses.initscr()

def write_line(*args):
	string = args.join(" ")
	stdscr.addstr(string)
	stdscr.refresh()
	sys.stdout.flush()

def overwrite_line(*args):
	string = args.join(" ")
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
		overwrite_line("Determining dependencies for packages: '" + package + "'.")
		parameters = package.split(":")
		packagename = parameters[0]
		if len(parameters) < 3:
			packagearch = "Default"
			if len(parameters) < 2:
				packageversion = "Latest"
		write_line(packagename, packageversion, packagearch)
	write_line("\n")
	
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
	print(args)
else:
	print("Do not execute indirectly. Prepare to die")
	sys.exit(1)
