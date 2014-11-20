import socket

class SocketUtils():
	
	def read_line(self, sock = None, delim = '\n', buffer_size = 4096):
		if sock == None and type(self.sock) != socket:
			sock = self.sock

		buffer = ''
		
		while True:
			data = sock.recv(buffer_size)
			buffer += bytes.decode(data)
		
			if buffer.endswith(delim):
				break

		return buffer.rstrip(delim)

	def write(self, string):
		buffer = bytes(string, encoding = "utf-8")

		self.sock.send(buffer)

	def writeln(self, string, delim = '\n'):
		buffer = bytes(string + delim, encoding = "utf-8")

		self.sock.send(buffer)