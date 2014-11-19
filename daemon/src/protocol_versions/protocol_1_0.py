import socket, shlex
from socket_utils import SocketUtils

class Protocol_1_0(SocketUtils):

	version = "PROTOCOL 1.0"
	
	def __init__(self, sock, client):
		self.sock = sock
		self.client = client
		self.running = True

		self.methods = {
			"update": self.update,
			"get": self.get,
			"download": self.download,
			"installed": self.installed,
			"heartbeat": self.heartbeat,
			"goodbye": self.goodbye
		}

	def update(self, args):
		# Todo: actually update
		self.writeln("UPDATED")

	def get(self, args):
		# Todo: Actually get
		if len(args) >= 2:
			if args[1] == "list":
				self.writeln("LIST {0}".format("/var/blah/list/path"))

	def download(self, args):
		# Todo: Actually download
		if len(args) >= 3:
			package = args[1]
			version = args[2]
 
			for i in range(100):
				self.writeln("STATUS {0} {1} {2}% {3}kb/s {4}kb/s".format(package, version, i, 100, 25, 10))

			self.writeln("DONE {0} {1} /var/cache/tpm/packages/{0}-{1}-x86_64.tpkg".format(package, version))

	def installed(self, args):
		# Todo: Check args, and if installed
		self.writeln("FALSE")

	def goodbye(self, args):
		self.writeln("GOODBYE")
		self.running = False

	def heartbeat(self, args):
		self.writeln(self.last_line)

	def run(self):
		self.writeln(self.version)

		while self.running == True:
			self.last_line = self.read_line();
			action = shlex.split(self.last_line.lower())
			self.call_method(action)

		self.sock.close();

	def call_method(self, action):
		if action[0] in self.methods:
			self.methods[action[0]](action[0:])
		else:
			self.no_such_method()

	def no_such_method(self):
		self.writeln("Error: XXX - No such method")
		self.close()

	def close(self):
		self.running = False