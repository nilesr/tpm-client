#!/bin/bash

import daemon, time

def run():
    with daemon.DaemonContext():
        print("This is a test!");

if __name__ == "__main__":
    run();
