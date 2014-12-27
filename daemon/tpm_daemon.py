#!/usr/bin/env python3

from daemon import Daemon
from tpm_protocol import TPMProtocol
import sys, os, time, configparser

class TPMDaemon(Daemon):
	def run(self):
		tpm_protocol = TPMProtocol(socket_path)
		while True:
			time.sleep(60)
					
if __name__ == "__main__":

	""" Load variables from configuration file """
	try:
		config = configparser.ConfigParser()
		config.read("/etc/tpm/config.ini")
		pidfile = config["daemon"]["pidfile"]
		logfile = config["daemon"]["logfile"]
		socket_path = config["daemon"]["socket"]
	except:
		print("Error reading config file at: {0}, exiting...".format("/etc/tpm/config.ini"))
		sys.exit(1)

	daemon = TPMDaemon(pidfile, "/tmp/", stdout = logfile, stderr = logfile);

	root = os.geteuid() == 0

	""" Daemon methods, convert to dict. and methods """
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1].lower():
			if not root:
				print("You must be root to start TPM-Daemon.")
				sys.exit(1)

			print("Starting TPM-Daemon.")
			try:
				daemon.start()
			except Exception as e:
				print(e)

		elif 'stop' == sys.argv[1].lower():
			if not root:
				print("You must be root to stop TPM-Daemon.")
				sys.exit(1)
			
			print("Stopping TPM-Daemon.")
			try:
				daemon.stop()
			except Exception as e:
				print(e)

		elif 'restart' == sys.argv[1].lower():
			if not root:
				print("You must be root to restart TPM-Daemon.")
				sys.exit(1)
					
			try:
				print("Stopping TPM-Daemon.");
				daemon.stop(True)
				print("Starting TPM-Daemon.")
				daemon.start()
			except Exception as e:
				print(e)

		elif 'status' == sys.argv[1].lower():
			pid = daemon.get_pid();
			if pid != -1:
				print("TPM-Daemon is running with PID: {0}.".format(pid))
			else:
				print("TPM-Daemon is not running")
		else:
			print("usage: {0} start|stop|restart|status".format(sys.argv[0]))
			sys.exit(2);
	else:
		print("usage: {0} start|stop|restart|status".format(sys.argv[0]))
		sys.exit(2)

