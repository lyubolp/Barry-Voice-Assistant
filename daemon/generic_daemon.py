import atexit
import os
import signal
import sys
import time

from logger import Logger


class GenericDaemon:
    def __init__(self, name: str):
        """
        Initialize variables
        """
        self.name = name
        self.pidFilePath = '/var/run/' + self.name + '.pid'
        self.logger = Logger(self.name + '-Daemon')

    def _run(self):
        """
        Override this method with daemon logic
        """

    def start(self):
        """
        Start the daemon
        """
        self.logger.info("Starting daemon " + self.name)

        if not self.__checkPermissions():
            raise PermissionError("Daemon must be started as root")

        pid = self.__readPidFromFile()

        if pid:
            self.logger.error("Daemon already running with pid " + str(pid) +
                              " or pid file corrupted " + self.pidFilePath)
            sys.exit(1)

        self.__daemonize()
        self._run()

    def stop(self):
        """
        Stop the daemon
        """
        self.logger.info("Stopping daemon")

        if not self.__checkPermissions():
            raise PermissionError("Daemon must be stopped as root")

        pid = self.__readPidFromFile()
        if not pid:
            self.logger.error("Daemon is not running")
            exit(1)

        self.__killOldDaemon()

    def restart(self):
        self.logger.info("Restarting daemon")

        if not self.__checkPermissions():
            raise PermissionError("Daemon must be restarted as root")

        self.stop()
        self.start()

    def __daemonize(self) -> None:
        """
        Convert the process to a daemon
        """
        self.logger.info("Start daemonizing process")

        self.__forkProcess()
        self.__decoupleEnv()
        self.__preventTty()
        self.__redirectFileDescriptors()
        self.__registerOnCloseMethod()
        self.__createPidFile()
        self.__registerSignalsHandlers()

        self.logger.info("Finished daemonizing process")

    def __checkPermissions(self) -> bool:
        if not os.access('/run/', os.W_OK):
            return False
        if not os.access('/var/run/', os.W_OK):
            return False
        return True

    def __forkProcess(self) -> None:
        """
        Demonize the current process by forking and killing the parent
        The process continues execution in the child
        """
        self.logger.info("Creating a fork")

        try:
            pid = os.fork()
            if pid > 0:
                # Exit parent
                sys.exit(0)
        except OSError as err:
            self.logger.error('Failed to fork: {0}\n'.format(err))
            sys.exit(1)

    def __decoupleEnv(self) -> None:
        """
        Change process dir to a safe one (that always exists)
        Decouple process from environment
        Set umask to 0
        """
        self.logger.info("Decoupling environment")

        try:
            os.chdir('/')
        except OSError:
            self.logger.error("Failed to change directory to /")
            exit(1)

        try:
            os.setsid()
        except OSError:
            self.logger.error("Failed to setsid")
            exit(1)

        try:
            os.umask(0)
        except OSError:
            self.logger.error("Failed set umask")
            exit(1)

    def __preventTty(self) -> None:
        """
        Fork from the current process (the child of the original process)
        and kill the parent (child of the original process)
        This way the process (grandchild of the original process)
        cannot attach itself to a tty
        """
        self.logger.info("Preventing process from attaching to tty"
                         + "by creating a fork")

        self.__forkProcess()

    def __redirectFileDescriptors(self) -> None:
        """
        Close the file descriptors and redirect them to /dev/null
        """
        self.logger.info("Redirecting file descriptors to /dev/null")

        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

    def __registerOnCloseMethod(self) -> None:
        """
        When closing the program run the specified method to cleanup
        """
        self.logger.info("Registering method to call when exiting")

        atexit.register(self.__removePidFile)

    def __createPidFile(self) -> None:
        """
        Create a pid file to keep track when the daemon is started
        This file is used to prevent the daemon from running another instance
        """
        self.logger.info("Creating pid file " + self.pidFilePath)

        pid = str(os.getpid())
        try:
            with open(self.pidFilePath, 'w+') as pidFile:
                pidFile.write(pid + '\n')
        except OSError:
            self.logger.error("Cannot write to " + self.pidFilePath
                              + ". Permission denied")
            exit(1)

    def __registerSignalsHandlers(self):
        """
        Handle gradcefully signals
        """
        self.logger.info("Initializing signal handlers")

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def __removePidFile(self):
        """
        Remove the pid file, used to determine if the daemon is already running
        """
        self.logger.info("Removing pid file " + self.pidFilePath)

        if os.path.exists(self.pidFilePath):
            os.remove(self.pidFilePath)

    def __readPidFromFile(self):
        try:
            with open(self.pidFilePath, 'r') as pidFile:
                return int(pidFile.read().strip())
        except IOError:
            return None

    def __killOldDaemon(self):
        # Try killing the daemon process
        try:
            pid = self.__readPidFromFile()
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            message = str(err.args)
            if message.find("No such process") > 0:
                self.__removePidFile()
            else:
                self.logger.error("Failed to kill daemon with unknown error")
                sys.exit(1)
