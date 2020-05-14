"""
Logger class, which provides easy interface to log messages to systemd journal

@require systemd
"""
from systemd import journal


class Logger:
    """Interface to the systemd logger"""

    def __init__(self, name):
        self.name = name

        self.logger = journal.logging.getLogger(self.name)
        journald_handler = journal.JournaldLogHandler()
        journald_handler.setFormatter(journal.logging.Formatter(
            '[%(levelname)s] %(message)s'
        ))
        self.logger.addHandler(journald_handler)
        # Logging level to display INFO logs
        self.logger.setLevel(journal.logging.DEBUG)

    def info(self, message: str) -> None:
        """
        Log a message to systemd journal as INFO
        """
        self.logger.info(message)

    def error(self, message: str) -> None:
        """
        Log a message to systemd journal as ERROR
        """
        self.logger.error(message)
