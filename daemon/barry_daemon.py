import generic_daemon
import os
import json
import subprocess


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
                return 'ACK'

        if len(messageParts) == 3:
            if messageParts[0] == 'config' and messageParts[1] == 'get':
                if messageParts[2] in self.config.keys():
                    return self.config[messageParts[2]]
                return ''
            if messageParts[0] == 'config' and messageParts[1] == 'unset':
                if messageParts[2] in self.config.keys():
                    del self.config[messageParts[2]]
                    self.__saveConfig()
                return 'ACK'

        if messageParts[0] == 'add':
            self.__addScript(messageParts)
            return 'ACK'

        if len(messageParts) == 1:
            if messageParts[0] == 'list':
                return json.dumps(self.__getAllScripts(), indent=4)

        if messageParts[0] == 'exec':
            response = self.__execute(messageParts)
            return response

        if messageParts[0] == 'remove':
            if 'scripts' in self.config.keys():
                if messageParts[1] in self.config['scripts']:
                    del self.config['scripts'][messageParts[1]]
                    self.__saveConfig()
            return 'ACK'

        return 'ERR'

    def __execute(self, message: []) -> str:
        message = message[1:]
        phrase = message[0]
        arguments = []
        if len(message) > 1:
            arguments = message[1:]
        self.logger.info('Looking to execute "' + phrase + '"')
        script = self.__getScript(phrase)
        if script == '':
            self.logger.info("No script to execute for " + phrase)
            return

        args = self.__getArgs(phrase)
        executable = [script] + args + arguments

        self.logger.info('Executing script ' + script + ' with arguments: ' + str(arguments))
        # Change user
        fileStat = os.stat(script)
        sudo = ['sudo', '-u', '#' + str(fileStat.st_uid)]

        out = subprocess.Popen(sudo + executable, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        stdout = stdout.decode('utf-8')
        self.logger.info("Script returned " + stdout)
        return stdout

    def __getScript(self, phrase: str) -> str:
        if 'scripts' in self.config.keys():
            if phrase in self.config['scripts']:
                return self.config['scripts'][phrase]['script']
        return ''

    def __getArgs(self, phrase: str) -> []:
        if 'scripts' in self.config.keys():
            if phrase in self.config['scripts']:
                args = self.config['scripts'][phrase]['args']
                argsParsed = []
                for arg in args:
                    if arg in self.config.keys():
                        argsParsed.append(self.config[arg])
                    else:
                        argsParsed.append('-')
                return argsParsed
        return []

    def __getAllScripts(self) -> {}:
        if 'scripts' in self.config.keys():
            self.logger.info("hi")
            return self.config['scripts']
        return {}

    def __addScript(self, message: []) -> None:
        message = message[1:]
        phrase = message[0]
        script = message[1]
        arguments = message[2:]
        self.logger.info('Adding phrase: ' + phrase + ', script:' + script + ', arguments: ' + str(arguments))
        if 'scripts' not in self.config.keys():
            self.config['scripts'] = {}

        if not os.path.isfile(script):
            self.logger.info("Invalid script " + script)
            return

        # if not os.path.isdir('/etc/barry/scripts/'):
        #     self.logger.info("Creating scripts directory /etc/barry/scripts/")
        #     os.mkdir('/etc/barry/scripts/')

        # self.logger.info("Copying " + script + " to " + '/etc/barry/scripts/')
        # copiedFile = shutil.copy(script, '/etc/barry/scripts/')

        self.config['scripts'][phrase] = {}
        self.config['scripts'][phrase]['script'] = os.path.abspath(script)
        argumentsCleared = [x for x in arguments if x != '']
        self.config['scripts'][phrase]['args'] = argumentsCleared
        self.logger.info(str(self.config['scripts'][phrase]))
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
                configFile.write('{\n}\n')

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
