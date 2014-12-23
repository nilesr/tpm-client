import argparse, curses, sys, time

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

def __download__():
	pass

def __install__():
	for package in args.packages:
		overwrite_line("Determining dependancies for packages: '{0}'".format(package));
	write_line("\n")

def __remove__():
	pass

def __purge__():
	pass

def __search__():
	pass

def __doctor__():
	pass



if __name__ == '__main__':



	function = "__" + args.action + "__"

	if function in locals():
		locals()["__" + args.action + "__"]()
	else:
		command_not_found()

	print(args)