#!/bin/python3

import sys
import os
import barry_client
import barry_daemon

name = "barry"

daemon = barry_daemon.BarryDaemon(name)
client = barry_client.BarryClient(name)

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
    elif 'config' == sys.argv[1]:
        if 'set' == sys.argv[2]:
            response = client.message('config:set:' + sys.argv[3] + ':' + sys.argv[4])
            print(response)
        elif 'get' == sys.argv[2]:
            response = client.message('config:get:' + sys.argv[3])
            print(response)
        elif 'unset' == sys.argv[2]:
            response = client.message('config:unset:' + sys.argv[3])
            print(response)
    elif 'add' == sys.argv[1]:
        file = os.path.abspath(sys.argv[3])
        phrase = sys.argv[2]
        arguments = ':'.join([x.strip(':') for x in sys.argv[4:]])
        response = client.message('add:' + phrase + ':' + str(file) + ':' + str(arguments))
        print(response)
    elif 'exec' == sys.argv[1]:
        response = client.message('exec:' + ':'.join(sys.argv[2:]))
        print(response)
    elif 'remove' == sys.argv[1]:
        response = client.message('remove:' + sys.argv[2])
        print(response)
    elif 'list' == sys.argv[1]:
        response = client.message('list')
        print(response)

    else:
        print("Unknown command")
        sys.exit(1)
    sys.exit(0)
else:
    print("usage: %s start|stop|restart" % sys.argv[0])
    sys.exit(2)
