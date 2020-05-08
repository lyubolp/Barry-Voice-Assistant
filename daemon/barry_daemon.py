import generic_daemon
import os
import json
import subprocess
import shutil


class BarryDaemon(generic_daemon.GenericDaemon):
    def __init__(self, name: str):
        self.name = name
        self.config = {}
        super().__init__(self.name)
        import unix_socket_server
        self.unixSocket = unix_socket_server.UnixSocketServer(self.name, self)

        self.configFilePath = '/etc/barry/barry.conf'

    def _run(self) -> None:
        self.__initConfig()
        self.unixSocket.startListening()

    def parseMessage(self, message: str) -> str:
        self.logger.info("Parsing message " + message)
        messageParts = message.split(':')
        if len(messageParts) == 4:
            if messageParts[0] == 'config' and messageParts[1] == 'set':
                self.__updateConfig(messageParts[2], messageParts[3])

        if len(messageParts) == 3:
            if messageParts[0] == 'config' and messageParts[1] == 'get':
                if messageParts[2] in self.config.keys():
                    return self.config[messageParts[2]]
                return ""
            if messageParts[0] == 'add':
                self.__addScript(messageParts[1], messageParts[2])

        if len(messageParts) == 2:
            if messageParts[0] == 'exec':
                response = self.__execute(messageParts[1])
                return 'RES:' + response
            else:
                return 'ERR'

        return 'ACK'

    def __execute(self, phrase: str) -> str:
        self.logger.info('Looking to execute "' + phrase + '"')
        script = self.__getScript(phrase)
        if script == '':
            self.logger.info("No script to execute for " + phrase)
            return

        self.logger.info("Executing script " + script)
        out = subprocess.Popen([script], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        stdout = stdout.decode('utf-8')
        self.logger.info("Script returned " + stdout)
        return stdout

    def __getScript(self, phrase: str) -> str:
        if 'scripts' in self.config.keys():
            if phrase in self.config['scripts']:
                return self.config['scripts'][phrase]

        return ''

    def __addScript(self, phrase: str, script: str) -> None:
        if 'scripts' not in self.config.keys():
            self.config['scripts'] = {}

        if not os.path.isfile(script):
            self.logger.info("Invalid script " + script)
            return

        if not os.path.isdir('/etc/barry/scripts/'):
            self.logger.info("Creating scripts directory /etc/barry/scripts/")
            os.mkdir('/etc/barry/scripts/')

        self.logger.info("Copying " + script + " to " + '/etc/barry/scripts/')
        copiedFile = shutil.copy(script, '/etc/barry/scripts/')

        self.config['scripts'][phrase] = copiedFile
        self.__saveConfig()

    def __updateConfig(self, key, value) -> None:
        self.logger.info("Updating config " + str(key) + " : " + str(value))
        self.config[key] = value
        self.__saveConfig()

    def __initConfig(self) -> None:
        if not os.path.isdir('/etc/barry/'):
            self.logger.info('Config directory /etc/barry/ not found')
            self.logger.info('Creating config directory /etc/barry/')
            os.mkdir('/etc/barry/')

        if not os.path.isfile(self.configFilePath):
            self.logger.info('Config ' + self.configFilePath + ' not found')
            self.logger.info('Creating ' + self.configFilePath)
            with open(self.configFilePath, 'w+') as configFile:
                configFile.write('\n')

        self.logger.info('Loading config from ' + self.configFilePath)
        with open(self.configFilePath, 'r+') as configFile:
            self.config = json.load(configFile)

    def __saveConfig(self) -> None:
        with open(self.configFilePath, 'w+') as configFile:
            json.dump(self.config, configFile, indent=4)

    def __loadConfig(self) -> None:
        self.logger.info('Loading config from ' + self.configFilePath)
        with open(self.configFilePath, 'r+') as configFile:
            self.config = json.load(configFile)
