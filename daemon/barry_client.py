import socket

from logger import Logger


class BarryClient:
    def __init__(self, name: str):
        self.name = name
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket_path = "/run/" + self.name + ".sock"
        self.logger = Logger(name + '-Client')

    def message(self, message: str) -> str:
        """Send a message to the daemon and get its response
        """
        try:
            self.sock.connect(self.socket_path)
        except socket.error:
            self.logger.error("Cannot connect to socket " + self.socket_path)
            raise IOError("Cannot connect to socket " + self.socket_path + ". Is the daemon running?")

        response = ""
        try:
            self.logger.info("Sending message to daemon over unix socket: " + message)
            self.sock.sendall(message.encode('utf-8'))

            response = b''
            buffer_size = 4096
            while True:
                response_part = self.sock.recv(buffer_size)
                response += response_part
                if len(response_part) < buffer_size:
                    break

            response = response.decode('utf-8')
            self.logger.info("Received response from daemon over unix socket: " + response)
            self.sock.close()
            return response
        except OSError:
            raise IOError("Cannot send message")
        finally:
            self.sock.close()
            return response
