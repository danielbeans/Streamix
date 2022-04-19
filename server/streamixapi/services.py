from hashlib import algorithms_available
from django.contrib.auth.hashers import make_password, check_password
from .utils import *
from pymongo.errors import DuplicateKeyError, InvalidName
from jwt.exceptions import DecodeError
from datetime import datetime, timedelta
from bson import ObjectId
import jwt
import environ
import requests
from django.core.cache import cache


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

    has_spotify_auth = False
    if 'spotify_auth' in found_user:
        has_spotify_auth = validate_spotify_access_token(
            found_user['spotify_auth'])

    has_youtube_auth = False
    if 'youtube_auth' in found_user:
        has_youtube_auth = True

    access_token = jwt.encode({'id': str(found_user['_id']),
                               'username': found_user['username'],
                               'name': found_user['name'],
                               'email': found_user['email'],
                               'exp': access_token_exp,
                               'hasSpotifyAuth': has_spotify_auth,
                               'hasYoutubeAuth': has_youtube_auth
                               },
                              env('SECRET_KEY'), algorithm='HS256')
    return {'access_token': access_token}


def validate_jwt_syntax(req: dict):
    PREFIX = 'Bearer '
    tokenParam = req.GET.get('access_token')
    if 'Authorization' not in req.headers and tokenParam is None:
        raise DecodeError()
    authHeader: str = tokenParam if tokenParam is not None else req.headers['Authorization']
    if tokenParam is None and not authHeader.startswith(PREFIX):
        raise DecodeError()
    return authHeader[len(PREFIX):] if tokenParam is None else authHeader


# !! TODO Add logic for getting new access tokens if current one is expired
def validate_spotify_access_token(spotify_auth: dict):
    if datetime.utcnow() < datetime.fromisoformat(spotify_auth['expires']):
        return True
    return False


# ! Basic search, not thorough
def search_for_spotify_tracks(tracks):
    headers = cache.get('headers')
    found_track_uris, found_tracks = [], []
    for track in tracks:
        query = track['name']
        search_type = ['track']
        limit = 3
        params = {
            'q': query,
            'type': search_type,
            'limit': limit
        }
        found_track = requests.get(f'{SPOTIFY_API_URI}/search',
                                   headers=headers, params=params).json()['tracks']['items'][0]
        found_tracks.append(found_track['name'])
        found_track_uris.append(found_track['uri'])
    cache.delete('headers')
    # Returns id of first track found and their names
    return found_track_uris, found_tracks
