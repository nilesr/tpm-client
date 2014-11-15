import sys, os, socket, _thread

#TODO: Convert _thread to threading

class TPMProtocol():
	
	def run(self, thread_name, thread_id):
		while True:
			try:
				connection, client_address = self.socket.accept()
				
				connection.send(b"Hello, World!")
				
				connection.close()
			except Exception as e:
				sys.stderr.write("%s\n" % e)

	def __init__(self, socket_path):
		self.socket_path = socket_path

		sys.stdout.write("Starting socket at: %s\n" % self.socket_path)

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

