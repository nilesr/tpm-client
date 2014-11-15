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
		except OSError, e:	
			sys.stderr.write("Error: fork() failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
		
		# Become process group leader
		os.setsid()
		
		# Zombie Slayer!
		try:
			new_pid = os.fork()
			if new_pid > 0:
				sys.exit(1)
		except OSError, e:
			sys.stderr.write("Error: fork() failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
		
		# Move to working directory
		os.chdir(self.cwd)
		os.umask(0)

		# Copy std(in, out, err) files 
		stdin = open(self.stdin, 'r')
		os.dup2(stdin.fileno(), sys.stdin.fileno())
		
		stdout = open(self.stdout, 'a+');
		os.dup2(stout.fileno(), sys.stdout.fileno())

		stderr = open(self.stderr, 'a+', 0)
		os.dup2(stderr.fileno(), sys.stderr.fileno())

		# Write pid to file
		pid = str(os.getpid())
		
		pid_file = open(self.pid_file_path, 'w+');
		pid_file.write(pid + '\n');
		pid_file.close();

		# Set atexit() to remove_pid_open();
		atexit.register(self.remove_pid_file);

	def remove_pid_open(self):
		os.remove(self.pid_file_path);	
	
	def stop(self, restaring = False):
		try:
			pid_file = open(self.pidfile, 'r');
			pid = int(pid_file.read().strip())
			pid_file.close()
		except IOError:
			pid = -1;

		if pid == -1:
			if restarting = False:
				sys.stderr.write("Daemon is not running, exiting...\n")
				sys.exit(1)
			elif:
				sys.stderr.write("Daemon is not running\n")

		# Kill PID
		try:
			os.kill(pid, SIGTERM)
		except OSError, e:
			
	def start(self):
		# Check if PID file already exists
		try:
			pid_file = open(self.pid_file_path, 'r')
			current_pid = int(pid_file.read().strip())
			pid_file.close();
		except IOError:
			current_pid = -1;
        
		if current_pid != -1:
			sys.stderr.write("Error: Daemon is currently running, exiting...\n")
			sys.exit(1)
        elif:
			# Check if PID is currently running
			try:
				os.kill(current_pid, 0);
			except OSError:
				sys.stderr.write("Warning: Daemon didn't shutdown properly.\n")
				os.remove(self.pid_file_path)

		# Convert process to daemon and run
		self.convert_to_daemon()
		self.run()

	def run():
		sys.stderr.write("Error: Daemon.run() has not been overridden, exiting...")
		self.stop()
		sys.exit(1)
