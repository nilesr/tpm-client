#!/usr/bin/env python3

from daemon import Daemon
from tpm_protocol import TPMProtocol
import sys, os, time
import configparser

PID_FILE = '/var/run/tpm-daemon.pid'
LOG_FILE = '/var/log/tpm-daemon.log'
CWD		= '/var/cache/tpm/'
UX_SOCK = '/var/run/tpm-socket'

class TPMDaemon(Daemon):
	def run(self):
		tpm_protocol = TPMProtocol(UX_SOCK)
		while True:
			time.sleep(60)
					
if __name__ == "__main__":
	daemon = TPMDaemon(PID_FILE, CWD, stdout = LOG_FILE, stderr = LOG_FILE);
	root = os.geteuid() == 0

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
				print("TPM-Daemon is running %s." % pid)
			else:
				print("TPM-Daemon is not running")
		else:
			print("usage: %s start|stop|restart|status" % sys.argv[0])
			sys.exit(2);
	else:
		print("usage: %s start|stop|restart|status" % sys.argv[0])
		sys.exit(2)

