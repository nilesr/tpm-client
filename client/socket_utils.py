import socket, sys, traceback

class SocketUtils():
	""" Class of basic socket utils for convenience, turn into library at some point """

	def read_line(self, sock = None, delim = '\n', buffer_size = 4096):
		""" Read until delim. from socket """

		try:
			if sock == None:
				sock = self.sock

			buffer = ''
			
			while True:
				data = sock.recv(buffer_size)
				buffer += bytes.decode(data)
			
				if buffer.endswith(delim):
					break

			return buffer.rstrip(delim)
		except:
			return False;

	def write(self, string):
		""" Write string to socket """

		buffer = bytes(string, encoding = "utf-8")
		return self.sock.send(buffer)

	def write_line(self, string, delim = '\n'):
		""" Write string to socket, followed by delim characters """

		buffer = bytes(string + delim, encoding = "utf-8")
		return self.sock.send(buffer)


""" Function versions of SocketUtils class methods: """

def read_line(sock, delim = '\n', buffer_size = 4096):
	try:
		buffer = ''
	
		while True:
			data = sock.recv(buffer_size)
			buffer += bytes.decode(data)
	
			if buffer.endswith(delim):
				break
		return buffer.rstrip(delim)
	except:
		sys.exit(1)
		return False

def write(sock, string):
	try:
		buffer = bytes(string, encoding = "utf-8")
		return sock.send(buffer)
	except:
		return False

def write_line(sock, string, delim = '\n'):
	try:
		buffer = bytes(string + delim, encoding = "utf-8")
		return sock.send(buffer)
	except:
		return False