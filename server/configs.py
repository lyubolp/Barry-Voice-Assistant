import configparser
import os
import json

SERVER_CONFIG = configparser.RawConfigParser()
SERVER_CONFIG.optionxform = str

current_dir = os.path.dirname(os.path.realpath(__file__)) + '/'

with open(current_dir + "server.conf") as stream:
    SERVER_CONFIG.read_string("[dummy]\n" + stream.read())
    SERVER_CONFIG = dict(SERVER_CONFIG['dummy'])

BARRY_CONFIG = configparser.RawConfigParser()
BARRY_CONFIG.optionxform = str

with open(current_dir + "defaults.conf") as stream:
    BARRY_CONFIG.read_string("[dummy]\n" + stream.read())
    BARRY_CONFIG = dict(BARRY_CONFIG['dummy'])


with open(current_dir + 'actions.json') as stream:
    ACTIONS = json.load(stream)
