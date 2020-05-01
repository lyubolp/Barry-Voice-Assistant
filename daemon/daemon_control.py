#!/bin/python3

import sys

from barry_client import BarryClient
from barry_daemon import BarryGenericDaemon

name = "barry"

daemon = BarryGenericDaemon(name)
client = BarryClient(name)

# /var/run/ PID file
# /run/ SOCKET file
if len(sys.argv) >= 2:
    if 'start' == sys.argv[1]:
        try:
            daemon.start()
        except IOError:
            print("Daemon must be started as root")
    elif 'stop' == sys.argv[1]:
        try:
            daemon.stop()
        except IOError:
            print("Daemon must be stopped as root")
    elif 'restart' == sys.argv[1]:
        try:
            daemon.restart()
        except IOError:
            print("Daemon must be restarted as root")
    elif 'ping' == sys.argv[1]:
        try:
            response = client.message('ping')
            print(response)
        except IOError as err:
            print(err)
    else:
        print("Unknown command")
        sys.exit(1)
    sys.exit(0)
else:
    print("usage: %s start|stop|restart" % sys.argv[0])
    sys.exit(2)
