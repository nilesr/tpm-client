import socket, sys
from socket_utils import SocketUtils

class DaemonCommunication(SocketUtils):
	
	_version = "PROTOCOL 1.0"

	def __init__(self, server_address, version = _version):
		self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.sock.settimeout(10)
		self._connected = False

		try:
			self.sock.connect(server_address)
			self._connected = True
		except:
			print("Failed to connect to dameon, it is either in use, or off.")
			sys.exit(1)

		self._version = version

	def close(self):
		""" Close socket """
		self.write_line("GOODBYE")
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def handshake(self):
		""" Handshake with the daemon """

		self.write_line("PROTOCOL 1.0")

		response = self.read_line()
		if response != self._version:
			print("Daemon handshake failed, with error: {0}".format(response));
			sys.exit(1)

	def get_list(self):
		""" Get LIST location from daemon """

		self.write_line("GET LIST")
		location = self.read_line()

		try:
			if location[:5] == "LIST ":
				location = location[5:]
				db = BTEdb.Database(location)
				return db
			else:
				raise Exception("Error")
		except:
			print("Error reading list. " + location)
			sys.exit(1)


	""" Connected property """
	@property
	def connected(self):
	    return self._connected

	@connected.setter
	def connected(self, value):
	    self._connected = value
	