import json

config = {
    "user": "root"
}
config["location"] = "bg"
with open("barry.conf", "w+") as file:
    json.dump(config, file, indent=4)
