import socket
import sys

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = './uds_socket'
print('connecting to %s' % server_address)
try:
    sock.connect(server_address)
except socket.error as msg:
    print(msg)
    sys.exit(1)
try:
    
    # Send data
    message = 'Hello there, General Kenobi'.encode('utf-8')
    print('sending "%s"' % message)
    sock.sendall(message)

    response = b''
    buffer_size = 4096
    while True:
        message_part = sock.recv(buffer_size)
        response += message_part
        if len(message_part) < buffer_size:
            break
    print('received "%s"' % response)

finally:
    print('closing socket')
    sock.close()
