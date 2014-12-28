import sys

class ScreenShim():

	def __init__(self):
		pass

	def end(self):
		""" Cleanup """
		pass

	def write(self, *args):
		""" Write data to stdout """
		string = " ".join(args)
		sys.stdout.write(string)
		sys.stdout.flush()

	def write_line(self, *args):
		""" Write line to stdout """
		string = " ".join(args) + "\n"
		sys.stdout.write(string)
		sys.stdout.flush()

	def overwrite(self, *args):
		""" Clean line and overwrite it """
		string = " ".join(args)
		sys.stdout.write("\r\033[K")
		sys.stdout.write(string)
		sys.stdout.flush()