import socket
import sys
import os

server_address = './uds_socket'

try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
print('starting up on %s' % server_address)
sock.bind(server_address)

sock.listen(1)

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
