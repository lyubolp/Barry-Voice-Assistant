from flask import Flask, request, jsonify
from configs import BARRY_CONFIG
import dbcon as DB
from executer import execute_command

DEFAULT_TEXT_TO_SAY = "Sorry, I could not understand"

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    response = {'errors': []}
    response['status'] = 'fail'

    if 'email' not in data:
        response['errors'].append('No email provided')
    if 'password' not in data:
        response['errors'].append('No password provided')

    if response['errors']:
        return jsonify(response)

    try:
        response['token'] = DB.register(data['email'], data['password'])
    except Exception as err:
        response['errors'].append(str(err))

    if response['errors']:
        return jsonify(response)

    response['status'] = 'success'
    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    response = {'errors': []}
    response['status'] = 'fail'

    if 'email' not in data:
        response['errors'].append('No email provided')
    if 'email' not in data:
        response['errors'].append('No password provided')

    if response['errors']:
        return jsonify(response)
    
    try:
        response['token'] = DB.login(data['email'], data['password'])
    except Exception as err:
        response['errors'].append(str(err))

    if response['errors']:
        return jsonify(response)

    response['status'] = 'success'
    return jsonify(response)


@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    response, email = DB.validate_token(data)
    if response['errors']:
        return jsonify(response)

    # TODO black lists?

    response['status'] = 'success'
    return jsonify(response)

@app.route('/execute/<command>/', methods=['GET'])
def execute(command):
    data = request.json
    response, email = DB.validate_token(data)
    if response['errors']:
        return jsonify(response)

    if response['errors']:
        return jsonify(response)

    try:
        message, details = execute_command(command, request.args)
        response['message'] = message
        response['details'] = details
    except Exception as err:
        response['errors'].append(str(err))
    if response['errors']:
        return jsonify(response)

    response['status'] = 'success'
    return jsonify(response)

@app.route('/list-config', methods=['GET'])
def list_config():
    data = request.json
    response, email = DB.validate_token(data)
    if response['errors']:
        return jsonify(response)

    try:
        response['user config'] = DB.list_config(email)
    except Exception as err:
        response['errors'].append(str(err))
    
    if response['errors']:
        return jsonify(response)

    response['default config'] = BARRY_CONFIG

    response['status'] = 'success'
    return jsonify(response)

@app.route('/set-config', methods=['POST'])
def set_config():
    data = request.json
    response, email = DB.validate_token(data)
    if response['errors']:
        return jsonify(response)

    args = request.args
    if 'key' not in args:
        response['errors'].append('Incorrect query. Missing argument "key"')
    if 'value' not in args:
        response['errors'].append('Incorrect query. Missing argument "value"')

    if response['errors']:
        return jsonify(response)

    try:
        DB.set_config(email, args['key'], args['value'])
    except Exception as err:
        response['errors']

    if response['errors']:
        return jsonify(response)

    response['status'] = 'success'
    return jsonify(response)


@app.route('/unset-config', methods=['DELETE'])
def unset_config():
    data = request.json
    response, email = DB.validate_token(data)
    if response['errors']:
        return jsonify(response)

    args = request.args
    if 'key' not in args:
        response['errors'].append('Incorrect query. Missing argument "key"')

    if response['errors']:
        return jsonify(response)
    try:
        DB.unset_config(email, args['key'])
    except Exception as err:
        response['errors'].append(str(err))
    if response['errors']:
        return jsonify(response)

    response['status'] = 'success'
    return jsonify(response)

@app.route('/get-config', methods=['GET'])
def get_config():
    data = request.json
    response, email = DB.validate_token(data)
    if response['errors']:
        return jsonify(response)

    args = request.args
    if 'key' not in args:
        response['errors'].append('Incorrect query. Missing argument "key"')

    if response['errors']:
        return jsonify(response)

    key = args['key']
    try:
        response['user config'] = {key: DB.get_config(email, key)}
    except Exception as err:
        response['errors'].append(str(err))

    if key in BARRY_CONFIG:
        response['default config'] = {key: BARRY_CONFIG[key]}
    else:
        response['errors'].append('No such key in default configs')

    if response['errors']:
        return jsonify(response)

    response['status'] = 'success'
    return jsonify(response)


app.run(debug=True)
