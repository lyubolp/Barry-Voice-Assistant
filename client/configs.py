import configparser
import os

CONFIG = configparser.RawConfigParser()
CONFIG.optionxform = str

current_dir = os.path.dirname(os.path.realpath(__file__)) + '/'

with open(current_dir + "client.conf") as stream:
    CONFIG.read_string("[dummy]\n" + stream.read())
    CONFIG = dict(CONFIG['dummy'])
