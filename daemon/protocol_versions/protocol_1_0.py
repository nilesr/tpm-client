import socket, shlex, traceback, BTEdb, sys, urllib, urllib.request, json, hashlib, os, platform, math, time, threading
from socket_utils import SocketUtils
import libtorrent as lt

class Protocol_1_0(SocketUtils):

	version = "PROTOCOL 1.0"
	
	def __init__(self, config):
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

		self.master = BTEdb.Database(self.config["daemon"]["rootdir"] + "/package-index.json")
		self.update_list()
		
	def update(self, args):
		self.update_list();
		self.writeln("UPDATED")

	def get(self, args):
		# Todo: Actually get
		if len(args) >= 2:
			if args[1] == "list":
				self.writeln("LIST {0} ".format(self.config["daemon"]["rootdir"] + "/package-index.json"))

	def download(self, args):
		# Todo: Actually download
		if len(args) >= 4:
			arch = args[3]
		else:
			arch = platform.processor()

		if len(args) >= 3:
			if args[2] == "latest":
				version = "Latest"
			else:
				version = args[2]
		else:
			version = "Latest"

		if len(args) >= 2:
			package = args[1]
			filename = False
			
			versions = self.master.Dump(package)
			for d in versions:
				if d["Version"] == version:
					if d["Version"] != "Latest" and d["Architecture"] == arch:
						filename = d["Filename"]
					else:
						for e in versions:
							if e["Version"] == d["LatestVersion"] and e["Architecture"] == arch:
								filename = e["Filename"]
								version = d["LatestVersion"];
			if not filename:
				self.writeln("ERROR XXX: Package not found.")
				return

			id = 0
			to_download = False
			for f in self.torrent_info.files():
				print(f.path.replace("packages/", "") + " = " + filename);
				if f.path.replace("packages/", "") == filename:
					to_download = f
					break;
				id += 1
			if not to_download:
				print("ERROR XXX: dunno")
				return

			pr = self.torrent_info.map_file(id, 0, to_download.size);
			n_pieces = math.ceil(pr.length / self.torrent_info.piece_length() + 1);

			for i in range(self.torrent_info.num_pieces()):
				if i in range(pr.piece, pr.piece + n_pieces):
					self.handler.piece_priority(i, 7)

			self.print_status(id, pr, package, version, filename)
				
			if self.valid_tpkg_file(to_download.path):
				self.writeln("DONE {0} {1} {2} {3}".format(package, version, arch, self.config["daemon"]["rootdir"] + "/" + to_download.path).replace('//', '/'))
			else:
				self.writeln("ERROR XXX: Hash verification failed.")
		else:
			self.writeln("INVALID ARGUMENTS");	

	def print_status(self, id, pr, package, version, filename):
		progress = self.get_progress(pr, id);
		
		while progress != 100:
			self.writeln("STATUS {0} {1}%".format(package, progress))
			time.sleep(1)
			progress = self.get_progress(pr, id);

		self.writeln("STATUS {0} {1}%".format(package, progress))

	def get_progress(self, pr, id):
		return round((self.handler.file_progress()[id] / pr.length) * 100, )

	def goodbye(self, args):
		self.writeln("GOODBYE")
		self.close();

	def heartbeat(self, args):
		self.writeln(self.last_line)

	def run(self, sock, client):
		self.sock = sock
		self.client = client
		self.writeln(self.version)
		self.running = True;

		while self.running == True:
			try:
				self.last_line = self.read_line();
				if len(self.last_line) != 0:
					action = shlex.split(self.last_line.lower())
					thread = threading.Thread(target = self.call_method, args = [action])
					thread.start()
			except Exception as e:
				print(e)
				break;
		self.close();

	def call_method(self, action):
		if action[0] in self.methods:
			self.methods[action[0]](action[0:])
		else:
			self.no_such_method()

	def no_such_method(self):
		self.writeln("Error: XXX - No such method")
		#self.close()

	def close(self):
		self.running = False
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def update_list(self):
		try:
			self.master.master = json.loads(self.fetch_repo_file("/package-index.json").decode('utf-8'))
			assert(not self.master.TransactionInProgress)
			self.master.Vacuum()

			self.fetch_repo_file("/torrent", self.config["daemon"]["rootdir"] + "/torrent", "wb")
			self.torrent_info = lt.torrent_info(self.config["daemon"]["rootdir"] + "/torrent")
			pre_downloaded = {}
			
			i = 0
			for f in self.torrent_info.files():
				if self.valid_tpkg_file(f.path):
					pre_downloaded[i] = f
				i += 1


			params = {
				"save_path": self.config["daemon"]["rootdir"],
				"ti": self.torrent_info
			}
			
			self.handler = self.ses.add_torrent(params)

			# FIX #
			for p in range(self.torrent_info.num_pieces()):
				self.handler.piece_priority(p, 0)

			for i in self.torrent_info.files():
				if i in pre_downloaded:
					pr = self.torrent_info.map_file(i, 0, pre_downloaded[i].size)
					n_pieces = pr.length / self.torrent_info.piece_length() + 1

					for p in range(self.torrent_info.num_pieces()):
						if p in range(pr.piece, pr.piece + n_pieces):
							self.handler.piece_priority(p, 7)

		except Exception as e:
			sys.stderr.write("Failed to update package list: {0}\n".format(e))
			traceback.print_exc()
			self.writeln("Error: XXX - Failed to update package list.")

	def fetch_remote_hashcode(self, path):
		return self.fetch_repo_file("/hash/" + path.replace("packages/", "")).decode('utf-8').strip()

	def fetch_local_hashcode(self, path):
		return hashlib.sha256(open(self.config["daemon"]["rootdir"] + path, "rb").read()).hexdigest()

	def fetch_repo_file(self, path, save = False, mode = 'w'):
		try:
			print("Fetching repo file: {0}".format(self.config["repo"]["repo_proto"] + "://" + self.config["repo"]["repo_addr"] + ":" + self.config["repo"]["repo_port"] + path))
		
			data = urllib.request.urlopen(self.config["repo"]["repo_proto"] + "://" + self.config["repo"]["repo_addr"] + ":" + self.config["repo"]["repo_port"] + path).read()

			if save != False:
				f = open(save, mode)
				f.write(data)
				f.close()
			return data
		except Exception as e:
			print("Failed to connect to server, exiting...");
			sys.exit(1)
	def valid_tpkg_file(self, path):
		print(self.config["daemon"]["rootdir"] + path)
		if os.path.exists(self.config["daemon"]["rootdir"] + "/" + path):
			return self.fetch_remote_hashcode(path) == self.fetch_local_hashcode(path)
		else:
			print("Package: " + path + " has not been downloaded.");
		return False