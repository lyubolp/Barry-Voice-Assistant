import os
import socket

from logger import Logger


class UnixSocketServer:
    def __init__(self, name: str):
        self.name = name
        self.socketPath = '/run/' + self.name + '.sock'
        self.logger = Logger(self.name + '-USocket')

    def startListening(self):
        """
        Enter listening mode, waiting for a connection
        """
        self.logger.info("Initializing Unix Socket")

        self.__removeOldSocketFile()
        self.__initSocket()
        self.__loop()

    def __removeOldSocketFile(self):
        self.logger.info("Removing old socket")

        try:
            os.remove(self.socketPath)
        except OSError:
            if os.path.exists(self.socketPath):
                self.logger.error("File exists: " + self.socketPath)

    def __initSocket(self):
        self.logger.info("Opening Unix socket on " + self.socketPath)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.socketPath)
        self.sock.listen(1)

    def __loop(self):
        self.logger.info("Entering listening mode, waitin for connections")
        while True:
            self.logger.info("Unix Socket waiting for a connection")
            self.connection, self.client_address = self.sock.accept()
            self.logger.info("Unix Socket established connection")
            try:
                message = self.__readMessage()

                # TODO use message
                message = message.lower()
                # TODO use message

                self.__writeMessage("Acknowledged")
            finally:
                self.logger.info("Unix Socket closing connection")
                self.connection.close()

    def __readMessage(self) -> str:
        """
        Read a message from a socket connection
        """
        message = b''
        buffer_size = 4096
        while True:
            message_part = self.connection.recv(buffer_size)
            message += message_part
            if len(message_part) < buffer_size:
                break

        messageDecoded = message.decode('utf-8')
        self.logger.info("Unix Socket received a message: " + messageDecoded)

        return messageDecoded

    def __writeMessage(self, message: str) -> None:
        self.logger.info("Unix socket sending message: " + message)

        messageInBytes = message.encode('utf-8')
        self.connection.sendall(messageInBytes)
