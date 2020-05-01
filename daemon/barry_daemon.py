from generic_daemon import GenericDaemon
from unix_socket_server import UnixSocketServer


class BarryGenericDaemon(GenericDaemon):
    def __init__(self, name: str):
        self.name = name
        super().__init__(self.name)
        self.unixSocket = UnixSocketServer(self.name)

    def _run(self):
        self.unixSocket.startListening()
