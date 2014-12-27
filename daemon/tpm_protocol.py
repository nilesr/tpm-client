import sys, os, socket, _thread, traceback, configparser

# Versions
from protocol_versions.protocol_1_0 import Protocol_1_0

from socket_utils import SocketUtils

#TODO: Convert _thread to threading

class TPMProtocol(SocketUtils):
	
	def run(self, thread_name, thread_id):
		""" Route incomming connection to handler """

		while True:
			try:
				sock, client = self.socket.accept()
				self.handler(sock, client)	
			except Exception as e:
				traceback.print_exception(*sys.exc_info())
				sys.stderr.write("err: {0}\n".format(e))

	def __init__(self, socket_path):

		""" Dict. of valid protocols and their handler classes """
		self.valid_protocols = {
			"PROTOCOL 1.0": Protocol_1_0
		}
		
		self.socket_path = socket_path

		sys.stdout.write("Starting socket at: {0}\n".format(self.socket_path))

		""" Load configuration files """
		self.config = configparser.ConfigParser()
		try:
			self.config.read("/etc/tpm/config.ini")
		except:
			print("Error reading config file at: {0}, exiting...".format("/etc/tpm/config.ini"))

		""" Construct objects of all valid protocols """
		for protocol in self.valid_protocols:
			self.valid_protocols[protocol] = self.valid_protocols[protocol](self.config)


		""" Ensure that domain socket is not running, and file doesn't exist """
		try:
			os.unlink(self.socket_path)
		except Exception as e:
			if os.path.exists(self.socket_path):
				sys.stderr.write("Socket file at: {0} exists, exiting...".format(self.socket_path))
				sys.exit(1)

		""" Create and bind unix domain socket for the daemon """
		try:
			self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			self.socket.bind(self.socket_path)
			self.socket.listen(0)

			# Start listener
			_thread.start_new_thread(self.run, ("Server", 0))
		except Exception as e:
			sys.stderr.write(e + "\n")


	""" Route incomming connection to protocol """
	def handler(self, sock, client):
		handshake = self.read_line(sock)

		if handshake in self.valid_protocols:
			protocol = self.valid_protocols[handshake];
			protocol.run(sock, client)
		else:
			sock.send(b"ERROR XXX - Invalid Protocol\n");
			sock.close()
