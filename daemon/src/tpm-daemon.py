#!/bin/bash

from daemon import Daemon
import sys

PID_FILE = '/var/run/tpm-daemon.pid'
LOG_FILE = '/var/log/tpm-daemon.log'
CWD		 = '/var/cache/tpm/'

class TPMDaemon(Daemon):

	def run(self):
			
if __name__ == "__main__":
	daemon = TPMDaemon(PID_FILE, CWD);

	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			print("Starting TPM-Daemon.")
			try:
				daemon.start()
			except:
				pass
		elif 'stop' == sys.argv[1]:
			print("Stopping TPM-Daemon.")
			try:
				daemon.stop()
			except:
				pass
		elif 'restart' == sys.argv[1]:
			try:
				print("Stopping TPM-Daemon.");
				daemon.stop()
				print("Starting TPM-Daemon.")
				daemon.start()
			except:
				pass
		elif 'status' == sys.argv[1]:
			pid = daemon.get_pid();
			if pid != -1:
				print("TPM-Daemon is running %s." % pid)
			else:
				print("TPM-Daemon is not running")
		else:
			print("Invalid command");
			sys.exit(2);
			sys.exit(0);
	else:
		print("usage: %s start|stop|restart|status" % sys.argv[0])
		sys.exit(2)

