import sys, os, time, atexit
from signal import SIGTERM 

class Daemon(object):
	def __init__(self, pid_file_path, cwd = '/tmp/', stdin = '/dev/null', stdout = '/dev/null', stderr = '/dev/null'):
		self.pid_file_path = pid_file_path
		self.cwd = cwd
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
	
	def convert_to_daemon(self):
		try:
			new_pid = os.fork()
			if new_pid > 0:
				sys.exit(0)
		except OSError as e:	
			sys.stderr.write("Error: fork() failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
		
		# Become process group leader
		os.setsid()
		
		# Zombie Slayer!
		try:
			new_pid = os.fork()
			if new_pid > 0:
				sys.exit(1)
		except OSError as e:
			sys.stderr.write("Error: fork() failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
		
		# Move to working directory
		if os.path.exists(self.cwd):
			if not os.path.isdir(self.cwd):
				os.rename(self.cwd, self.cwd + ".bak")
		else:
			os.makedirs(self.cwd)
					
		os.chdir(self.cwd)
		os.umask(0)

		# Copy std(in, out, err) files 
		stdin = open(self.stdin, 'r', 1)
		os.dup2(stdin.fileno(), sys.stdin.fileno())
		
		stdout = open(self.stdout, 'a+', 1);
		os.dup2(stdout.fileno(), sys.stdout.fileno())

		stderr = open(self.stderr, 'a+', 1)
		os.dup2(stderr.fileno(), sys.stderr.fileno())

		# Write pid to file
		pid = str(os.getpid())
		pid_file = open(self.pid_file_path, 'w+');
		pid_file.write(pid);
		pid_file.close();

		# Set atexit() to remove_pid_open();
		atexit.register(self.remove_pid_file);

	def get_pid(self):
		try:
			pid_file = open(self.pid_file_path, 'r');
			pid = int(pid_file.read().strip())
			pid_file.close()
		except:
			pid = -1;
		return pid

	def remove_pid_file(self):
		os.remove(self.pid_file_path);	
	
	def stop(self, restarting = False):
		pid = self.get_pid();
	
		if pid == -1:
			if restarting == False:
				sys.stderr.write("Daemon is not running, exiting...\n")
				sys.exit(1)
			else:
				sys.stderr.write("Daemon is not running\n")

		# Kill PID
		try:
			os.kill(pid, SIGTERM)
			self.remove_pid_file()
		except OSError as e:
			#TODO: Make a more advance handler
			sys.exit(1)
			
	def start(self):
		# Check if PID file already exists
		pid = self.get_pid()
		
		if pid != -1:
			sys.stderr.write("Error: Daemon is currently running, exiting...\n")
			sys.exit(1)
		
		# Convert process to daemon and run
		self.convert_to_daemon()
		self.run()

	def run():
		sys.stderr.write("Error: Daemon.run() has not been overridden, exiting...\n")
		self.stop()
		sys.exit(1)
