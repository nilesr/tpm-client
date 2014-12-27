import sys

class ScreenShim():

	def __init__(self):
		pass

	def end(self):
		pass

	def write(self, *args):
		string = " ".join(args)
		sys.stdout.write(string)
		sys.stdout.flush()

	def write_line(self, *args):
		string = " ".join(args) + "\n"
		sys.stdout.write(string)
		sys.stdout.flush()

	def overwrite(self, *args):
		string = " ".join(args)
		sys.stdout.write("\r\033[K")
		sys.stdout.write(string)
		sys.stdout.flush()