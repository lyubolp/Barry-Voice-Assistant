#!/usr/bin/python3
import json
import os
import sys
from typing import List

STORAGE_PATH = 'actions/todo/lists.json'


def add_item(list_type: str, item: str) -> bool:
    if not os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "w+") as f:
            f.write('{}')

    with open(STORAGE_PATH) as json_file:
        data = json.load(json_file)

        if list_type not in data:
            data[list_type] = []

        items = data[list_type]
        if item in items:
            return False

        items.append(item)

    with open(STORAGE_PATH, 'w') as json_file:
        json.dump(data, json_file)

    return True


def remove_item(list_type: str, item: str) -> bool:
    if not os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "w+") as f:
            f.write('{}')

    with open(STORAGE_PATH) as json_file:
        data = json.load(json_file)

        if list_type not in data:
            data[list_type] = []

        items = data[list_type]
        if item not in items:
            return False

        items.remove(item)

    with open(STORAGE_PATH, 'w') as json_file:
        json.dump(data, json_file)

    return True


def get_items(list_type: str) -> List[str]:
    if not os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "w+") as f:
            f.write('{}')

    with open(STORAGE_PATH) as json_file:
        data = json.load(json_file)

        if list_type not in data:
            return []

        return data[list_type]


def clear_items(list_type: str):
    if not os.path.exists(STORAGE_PATH):
        with open(STORAGE_PATH, "w+") as f:
            f.write('{}')

    with open(STORAGE_PATH) as json_file:
        data = json.load(json_file)

        del data[list_type]

    with open(STORAGE_PATH, 'w') as json_file:
        json.dump(data, json_file)


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'add':
        if len(sys.argv) == 5:
            STORAGE_PATH = sys.argv[4]
        if add_item(sys.argv[2], sys.argv[3]):
            print("Item added")
        else:
            print("Item is already present")
    elif command == 'remove':
        if len(sys.argv) == 5:
            STORAGE_PATH = sys.argv[4]
        if remove_item(sys.argv[2], sys.argv[3]):
            print("Item removed")
        else:
            print("No such item is present")
    elif command == 'get':
        if len(sys.argv) == 4:
            STORAGE_PATH = sys.argv[3]
        items = get_items(sys.argv[2])
        if not items:
            print("The list is empty")
        else:
            print(items)

    elif command == 'clear':
        if len(sys.argv) == 4:
            STORAGE_PATH = sys.argv[3]
        clear_items(sys.argv[2])
        print(sys.argv[2] + " list cleared")
    else:
        print("Unknown command")
