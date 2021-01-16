import jwt
from pymongo.errors import DuplicateKeyError
import bcrypt
import datetime
from pymongo import MongoClient
from configs import SERVER_CONFIG
from pymongo.errors import DuplicateKeyError, ConnectionFailure

try:
    db_client = MongoClient(SERVER_CONFIG['mongodb_key'])
    barry_db = db_client.barry
except Exception as err:
    barry_db = None
    print(err)

# TODO Create index on email


def register(email, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()
    new_user = {
        'email': email,
        'password': hashed_password,
    }
    try:
        _result = barry_db.users.insert_one(new_user)
        return encode_auth_token(email)
    except DuplicateKeyError:
        raise DuplicateKeyError("User already exists")
    except:
        raise ConnectionFailure("Failed to connect to the database")

def login(email, password):
    try:
        user = barry_db.users.find_one({'email': email})
    except:
        raise ConnectionFailure("Failed to connect to the database")

    if not user:
        raise ValueError("No such user.")
    
    hashed_password = user['password']
    if bcrypt.checkpw(password.encode(), hashed_password.encode()):
        return encode_auth_token(email)
    else:
        raise ValueError("Wrong password")

def list_config(email):
    try:
        user = barry_db.users.find_one({'email': email})
    except:
        raise ConnectionFailure("Failed to connect to the database")

    if 'config' in user:
        return user['config']
    return {}

def set_config(email, key, val):
    try:
        result = barry_db.users.update_one(
            {'email': email}, {'$set': {'config.' + key: val}})
    except:
        raise ConnectionFailure("Failed to connect to the database")

def unset_config(email, key):
    try:
        result = barry_db.users.update_one(
            {'email': email}, {'$unset': {'config.' + key: ''}})
    except:
        raise ConnectionFailure("Failed to connect to the database")

def get_config(email, key):
    try:
        user = barry_db.users.find_one({'email': email})
    except:
        raise ConnectionFailure("Failed to connect to the database")

    if 'config' in user and key in user['config']:
        return user['config'][key]
    raise Exception("No such key in user configs")

def encode_auth_token(email):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': email
        }
        
        return jwt.encode(
            payload,
            SERVER_CONFIG['jwt_secret'],
            algorithm='HS256'
        ).decode()
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    payload = jwt.decode(auth_token, SERVER_CONFIG['jwt_secret'])
    return payload['sub']

def validate_token(data):
    response = {'errors': []}
    response['status'] = 'fail'
    if 'token' not in data:
        response['errors'].append('No token provided')

    if response['errors']:
        return response

    token = data['token']
    try:
        email = decode_auth_token(token)
        return response, email
    except jwt.ExpiredSignatureError:
        response['errors'].append('Token expired. Please log in again.')
    except jwt.InvalidTokenError:
        response['errors'].append('Invalid token. Please log in again.')

    return response, None
