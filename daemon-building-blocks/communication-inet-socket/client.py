import socket
import sys


addr = ("127.0.0.1", 8080)
try:
    sock = socket.create_connection(addr)
except Exception as msg:
    print("Connection refused")
    exit(1)

try:
    # Send data
    message = 'Hello there, General Kenobi'.encode('utf-8')
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
