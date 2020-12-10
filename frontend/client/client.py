import requests
from typing import Tuple, List, Dict

from client import configsFile

__server_url = configsFile.CONFIG['server_url']


def login(email: str, password: str) -> str:
    credentials = {'email': email, 'password': password}
    response = requests.post(__server_url + 'login', json=credentials).json()
    if 'status' in response and response['status'] == 'success':
        return response['token']
    else:
        raise Exception(response['errors'])


def register(email: str, password: str) -> str:
    credentials = {'email': email, 'password': password}
    response = requests.post(__server_url + 'register', json=credentials).json()
    if 'status' in response and response['status'] == 'success':
        return response['token']
    else:
        raise Exception(response['errors'])


def list_config(token: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    body = {'token': token}
    response = requests.get(__server_url + 'list-config', json=body).json()

    if 'status' in response and response['status'] == 'success':
        return response['default config'], response['user config']
    else:
        raise Exception(response['errors'])


def get_config(token: str, key: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    body = {'token': token}
    response = requests.get(
        __server_url + 'get-config?key=' + key, json=body).json()
    
    if 'status' in response and response['status'] == 'success':
        return response['default config'], response['user config']
    else:
        raise Exception(response['errors'])


def set_config(token: str, key: str, value: str) -> bool:
    body = {'token': token}
    response = requests.post(
        __server_url + 'set-config?key=' + key + '&value=' + value, json=body).json()

    if 'status' in response and response['status'] == 'success':
        return True
    else:
        raise Exception(response['errors'])


def unset_config(token: str, key: str) -> bool:
    body = {'token': token}
    response = requests.delete(
        __server_url + 'unset-config?key=' + key, json=body).json()

    if 'status' in response and response['status'] == 'success':
        return True
    else:
        raise Exception(response['errors'])


def execute_command(token: str, command: str, args: Dict[str, str] = {}) -> bool:
    body = {'token': token}
    args = '&'.join( str(key) + '=' + str(value) for key,value in args.items() )
    response = requests.get(
        __server_url + 'execute/' + command + '/?' + args, json=body).json()

    if 'status' in response and response['status'] == 'success':
        return response
    else:
        raise Exception(response['errors'])
