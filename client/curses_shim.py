import curses

class CursesShim():

	def __init__(self, stdscr):
		pass

	def write(*args):
		string = " ".join(args)
		stdscr.addstr(string)
		stdscr.refresh()
		sys.stdout.flush()

	def write_line(*args):
		string = " ".join(args) + "\n"
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