#!/bin/bash

configfile = "/etc/tpm.conf"

defaultserver = "http:niles.mooo.com:5000"

import daemon, time, os, configparser, BTEdb, urllib.request

def run():
    with daemon.DaemonContext():
		config = False
        if os.path.exists(configfile):
			config = configparser.ConfigParser(allow_no_value=True)
			try:
				config.read(configfile)
			except:
				config = False
		if config:
			server = config["servers"]["primary"].split(":")
		else:
			server = defaultserver.split(":")
		if not os.path.isdir("/var/cache/tpm"):
			os.mkdir("/var/cache/tpm")
		packageindex = BTEdb.Database("/var/cache/tpm/package-index.json")
		response = urllib.request.urlopen(server[0] + "://" + server[1] + ":" + server[2] + "/package-index.json")
		packageindex.master = json.loads(response.read())
if __name__ == "__main__":
    run()
