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
			"get": self.get
		}

	def update(self, args):
		#Todo: actually update
		self.writeln("UPDATED")

	def get(self, args):
		if len(args) >= 2:
			if args[1] == "list":
				self.writeln("LIST %s" % "/var/blah/list/path")

	def run(self):
		self.writeln("%s" % self.version)

		while self.running == True:
			action = shlex.split(self.read_line().lower())
			self.call_method(action)

		self.sock.close();

	def call_method(self, action):
		if action[0] in self.methods:
			self.methods[action[0]](action[0:])
		else:
			self.no_such_method()

	def no_such_method(self):
		self.writeln(b"Error: XXX - No such method")
		self.close()

	def close(self):
		self.running = False