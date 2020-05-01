import socket
import sys
import os

addr = ('', 8080)  # all interfaces, port 8080
if socket.has_dualstack_ipv6():
    sock = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
else:
    sock = socket.create_server(addr)

def readMessage(connection):
    message = b''
    buffer_size = 4096
    while True:
        message_part = connection.recv(buffer_size)
        message += message_part
        if len(message_part) < buffer_size:
            break
    return message.decode('utf-8')

while True:
    sys.stderr.write('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        message = readMessage(connection)
        print('received {0}'.format(message))

    finally:
        # Clean up the connection
        connection.close()
