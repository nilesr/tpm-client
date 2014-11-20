import sys, os, socket, _thread, traceback, configparser

# Versions
from protocol_versions.protocol_1_0 import Protocol_1_0

from socket_utils import SocketUtils

#TODO: Convert _thread to threading

class TPMProtocol(SocketUtils):
	
	def run(self, thread_name, thread_id):
		
		self.valid_protocols = {
			"PROTOCOL 1.0": Protocol_1_0
		}
		
		while True:
			try:
				sock, client = self.socket.accept()
				self.handler(sock, client)	
			except Exception as e:
				sys.stderr.write("%s\n" % e)

	def __init__(self, socket_path):
		self.socket_path = socket_path

		sys.stdout.write("Starting socket at: %s\n" % self.socket_path)
		self.config = configparser.ConfigParser()
		try:
			self.config.read("/etc/tpm/config.ini")
		except:
			print("Error reading config file")
			print(traceback.format_exc())
		try:
			os.unlink(self.socket_path)
		except Exception as e:
			if os.path.exists(self.socket_path):
				sys.stderr.write("Socket file at: %s exists, exiting...")
				sys.exit(1)

		try:
			# Create and bind() UNIX Socket
			self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			self.socket.bind(self.socket_path)
			self.socket.listen(1)
			
			# Start listener
			_thread.start_new_thread(self.run, ("Server", 0))
		except Exception as e:
			sys.stderr.write("%s\n" % e)	

	def handler(self, sock, client):
		handshake = self.read_line(sock)
	
		if handshake in self.valid_protocols:
			protocol = self.valid_protocols[handshake](sock, client, self.config)
			protocol.run()
		else:
			self.writeln("ERROR XXX - Invalid Protocol")
			sock.close()
