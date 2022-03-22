from django.contrib.auth.hashers import make_password, check_password
from utils import db_connector
from pymongo.errors import DuplicateKeyError, InvalidName


def authenticate_user(user: dict):
    db_users = db_connector.db_handle['Users']
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
