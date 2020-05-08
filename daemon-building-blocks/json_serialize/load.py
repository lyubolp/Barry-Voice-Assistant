import json

config = {}

with open("barry.conf", "r+") as file:
    config = json.load(file)

for key in config:
    print(key + ": " + config[key])
