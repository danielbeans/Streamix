from hashlib import algorithms_available
from django.contrib.auth.hashers import make_password, check_password
from .utils import *
from pymongo.errors import DuplicateKeyError, InvalidName
from jwt.exceptions import DecodeError
from datetime import datetime, timedelta
from bson import ObjectId
import jwt
import environ

env = environ.Env()
db_users = db_connector.db_handle['Users']


def authenticate_user(user: dict):
    global env, db_users
    print('** Authenticating user **')

    def validate_jwt(access_token):
        decoded_jwt = decode_jwt(access_token)
        if db_users.find_one({'_id': ObjectId(decoded_jwt['id'])}) and datetime.strptime(decoded_jwt['exp'], '%m%d%Y%H%M%S') >= datetime.now():
            return True
        return False

    if 'Authorization' in user:
        return validate_jwt(user['Authorization'])
    else:
        found_user = db_users.find_one({'username': user['username']})
        if found_user:
            return check_password(user['password'], found_user['password'])
        else:
            raise InvalidName(f'No User \'{user["username"]}\' found')


def signup_user(user: dict):
    global db_users
    if db_users.find_one({'username': user['username']}):
        raise DuplicateKeyError('Duplicate user found')
    user['password'] = make_password(user['password'])
    db_users.insert_one(user)
    return True


def create_jwt(user: dict):
    global env, db_users
    found_user = db_users.find_one({'username': user['username']})
    access_token_exp = (datetime.now() + timedelta(days=1)
                        ).strftime('%m%d%Y%H%M%S')

    has_spotify_auth = validate_spotify_access_token(
        found_user['spotify_auth'])

    access_token = jwt.encode({'id': str(found_user['_id']),
                               'username': found_user['username'],
                               'name': found_user['name'],
                               'email': found_user['email'],
                               'exp': access_token_exp,
                               'hasSpotifyAuth': has_spotify_auth,
                               'hasYoutubeAuth': False  # ! fetch access token from DB and check if valid
                               },
                              env('SECRET_KEY'), algorithm='HS256')
    return {'access_token': access_token}


def update_user(user: dict, info: dict):
    global db_users
    return db_users.update_one({'username': user['username']}, {'$set': info})


def validate_jwt_syntax(req: dict):
    PREFIX = 'Bearer '
    authHeader: str = req.headers['Authorization']
    if not authHeader.startswith(PREFIX):
        raise DecodeError()
    return authHeader[len(PREFIX):]


# !! TODO Add logic for getting new access tokens if current one is expired
def validate_spotify_access_token(spotify_auth: dict):
    if datetime.utcnow() < datetime.fromisoformat(spotify_auth['expires']):
        return True
    return False
