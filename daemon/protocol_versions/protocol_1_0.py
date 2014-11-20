import socket, shlex, traceback, BTEdb, sys, urllib
from socket_utils import SocketUtils
import libtorrent as lt

class Protocol_1_0(SocketUtils):

	version = "PROTOCOL 1.0"
	
	def __init__(self,sock,client,config):
		self.sock = sock
		self.client = client
		self.running = True
		self.config = config

		self.methods = {
			"update": self.update,
			"get": self.get,
			"download": self.download,
			"heartbeat": self.heartbeat,
			"goodbye": self.goodbye
		}

		ses = lt.session()
		try:
			ses.listen_on(int(config["libtorrent"]["listen_port_lower"]), int(config["libtorrent"]["listen_port_upper"]))
		except:
			print("Port is not an int")
			print(traceback.format_exc())
			sys.exit(1)
		ses.start_dht()
		ses.start_upnp()
		master = BTEdb.Database(config["daemon"]["rootdir"] + "/package-index.json")

	def update(self, args):
		packageindex = BTEdb.Database("/var/cache/tpm/package-index.json")
		response = urllib.request.urlopen(self.config["repo"]["repo_proto"] + "://" + self.config["repo"]["repo_addr"] + ":" + self.config["repo"]["repo_port"] + "/package-index.json")
		packageindex.master = json.loads(response.read())
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
				self.writeln("STATUS {0} {1} {2}% {3}kb/s {4}kb/s".format(package, version, i,100 , 25, 10))
				
			self.writeln("DONE {0} {1} /var/cache/tpm/packages/{0}-{1}-x86_64.tpkg".format(package, version))
			
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
