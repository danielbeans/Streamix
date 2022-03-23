from hashlib import algorithms_available
from django.contrib.auth.hashers import make_password, check_password
from utils import db_connector
from pymongo.errors import DuplicateKeyError, InvalidName
from datetime import datetime, timedelta
from bson import ObjectId
import jwt
import environ
import random
import string


def authenticate_user(user: dict):
    env = environ.Env()
    db_users = db_connector.db_handle['Users']
    print('Authenticating user: ', user)

    def validate_jwt(access_token):
        decoded_jwt = jwt.decode(access_token, env(
            'SECRET_KEY'), algorithms=["HS256"])
        print('JWT', decoded_jwt)
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
    db_users = db_connector.db_handle['Users']
    if db_users.find_one({'username': user['username']}):
        raise DuplicateKeyError('Duplicate user found')
    user['password'] = make_password(user['password'])
    db_users.insert_one(user)
    return True


def create_jwt(user: dict):
    env = environ.Env()
    db_users = db_connector.db_handle['Users']
    found_user = db_users.find_one({'username': user['username']})
    access_token_exp = (datetime.now() + timedelta(days=1)
                        ).strftime('%m%d%Y%H%M%S')

    access_token = jwt.encode({'id': str(found_user['_id']), 'username': found_user['username'], 'name': found_user['name'], 'email': found_user['email'], 'exp': access_token_exp}, env(
        'SECRET_KEY'), algorithm='HS256')

    return {'access_token': access_token}
