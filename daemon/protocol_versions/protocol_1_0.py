import socket, shlex, traceback, BTEdb, sys, urllib, json, os, platform
from socket_utils import SocketUtils
import libtorrent as lt

class Protocol_1_0(SocketUtils):

	version = "PROTOCOL 1.0"
	
	def __init__(self, sock, client, config):
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

		self.required_directories = {
			self.config["daemon"]["rootdir"] + "/packages"
		}

		for d in self.required_directories:
			if not os.path.exists(d):
				os.makedirs(d)


		self.ses = lt.session()
		try:
			self.ses.listen_on(int(self.config["libtorrent"]["listen_port_lower"]), int(self.config["libtorrent"]["listen_port_upper"]))
		except:
			print(traceback.format_exc())
			sys.exit(1)

		self.ses.start_dht()
		self.ses.start_upnp()

		# NOT LOADING PROPERLY!!!! #
		self.master = BTEdb.Database(self.config["daemon"]["rootdir"] + "/package-index.json")
		self.update_list()
		
	def update(self, args):
		self.update_list();
		self.writeln("UPDATED")

	def get(self, args):
		# Todo: Actually get
		if len(args) >= 2:
			if args[1] == "list":
				self.writeln("LIST {0} ".format("/var/blah/list/path"))

	def download(self, args):
		# Todo: Actually download
		if len(args) >= 4:
			arch = args[3]
		else:
			arch = platform.processor()
		if len(args) >= 3:
			package = args[1]
			version = args[2]
			
			for i in range(100):
				self.writeln("STATUS {0} {1} {2}% {3}kb/s {4}kb/s".format(package, version, i, 100, 25, 10))
				
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

	def update_list(self):
		try:
			self.master.master = json.loads(self.fetch_repo_file("/package-index.json"))
			self.master.Vacuum()
			torrent = lt.bdecode(self.fetch_repo_file("/latest.torrent"))

			torrent_info = lt.torrent_info(torrent)
			pre_downloaded = {}
			
			i = 0
			for f in torrent_info.files():
				if self.valid_tpkg_file(f):
					pre_downloaded[i] = f
				i += 1


			params = {
				"save_path": self.config["daemon"]["rootdir"] + "/packages/",
				"ti": torrent_info
			}
			
			h = self.ses.add_torrent(params)

			for i in pre_downloaded:
				pr = torrent_info.map_file(i, 0, pre_downloaded[i])
				n_pieces = pr.length / torrent_info.piece_length() + 1

				for p in range(torrent_info.num_pieces()):
					if p in range(pr.piece, pr.piece + n_pieces):
						h.piece_priority(p, 7)
					else:
						h.piece_priority(p, 0)

		except Exception as e:
			sys.stderr.write("Failed to update package list: {0}\n".format(e))
			self.writeln("Error: XXX - Failed to update package list.")

	def fetch_remote_hashcode(self, f):
		return fetch_repo_file("/hash/" + f.path)

	def fetch_local_hashcode(self, f):
		return hashlib.sha256(open(self.config["daemon"]["rootdir"] + f.path).read()).hexdigest()

	def fetch_repo_file(self, path, save = False, mode = 'w+'):
		print("Fetching repo file: {0}".format(self.config["repo"]["repo_proto"] + "://" + self.config["repo"]["repo_addr"] + ":" + self.config["repo"]["repo_port"] + path))
		
		data = urllib.request.urlopen(self.config["repo"]["repo_proto"] + "://" + self.config["repo"]["repo_addr"] + ":" + self.config["repo"]["repo_port"] + path).read().decode('utf-8')

		if save != False:
			f = open(save, mode)
			f.write(data)
			f.close()

		return data
		
	def valid_tpkg_file(self, f):
		if os.path.exists(self.config["daemon"]["rootdir"] + f.path):
			return fetch_remote_hashcode(f) == fetch_local_hashcode(f)
		return False