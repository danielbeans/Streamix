from rest_framework import status
from rest_framework.response import Response
from .services import *
from .utils import *
import jwt
import environ
import requests
import base64
import json
from datetime import datetime, timedelta
from django.core.cache import cache

env = environ.Env()
db_users = db_connector.db_handle['Users']


class AuthController():
    def login(req: dict):
        user = {
            'username': req['username'],
            'password': req['password']
        }
        if authenticate_user(user):
            return Response(create_jwt(user), status=status.HTTP_200_OK)
        else:
            return Response(f'User \'{user["username"]}\' could not be authenticated', status=status.HTTP_401_UNAUTHORIZED)

    def signup(req: dict):
        user = {
            'name': req['name'],
            'email': req['email'],
            'username': req['username'],
            'password': req['password']
        }
        if signup_user(user):
            return Response(create_jwt(user), status=status.HTTP_201_CREATED)
        else:
            return Response(f'User \'{user["username"]}\' could not be signed up', status=status.HTTP_401_UNAUTHORIZED)

    # !! TODO allow jwt to be used to obtain a new one
    def obtain_jwt(req: dict):
        user = {
            'username': req['username'],
            'password': req['password']
        }
        if authenticate_user(user):
            return Response(create_jwt(user), status=status.HTTP_200_OK)
        else:
            return Response(f'User \'{user["username"]}\' could not be authenticated', status=status.HTTP_401_UNAUTHORIZED)

    def verify_jwt(token: str):
        if authenticate_user({'Authorization': token}):
            env = environ.Env()
            decoded_token = decode_jwt(token)
            print(decoded_token)
            formatted_exp = datetime.strftime(datetime.strptime(
                decoded_token['exp'], '%m%d%Y%H%M%S'), '%b %d %Y %I:%M%p')
            return Response('Authentication successful -- Expires ' + formatted_exp, status=status.HTTP_200_OK)
        else:
            return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)


class SpotifyController():
    def get_auth_code(token: str):
        global env
        if authenticate_user({'Authorization': token}):
            user = decode_jwt(token)
            # Sets user in cache to use later to store access tokens
            cache.set('user', user)
            res = {
                'client_id': env('SPOTIFY_ID'),
                'response_type': 'code',
                'redirect_uri': 'http://localhost:8000/api/auth/spotify/callback'
            }
            return res
        else:
            return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    # !! TODO Write logic for refreshing Spotify tokens
    def get_tokens(code: str, grant_type: GRANT_TYPE):
        global env

        if len(code) != 0:
            data = {
                'grant_type': grant_type,
                'code': code,
                'redirect_uri': 'http://localhost:8000/api/auth/spotify/callback'
            }
            spotify_auth = env('SPOTIFY_ID') + ':' + env('SPOTIFY_SECRET')
            encoded_spotify_auth = 'Basic '.encode(
                'ascii') + base64.b64encode(spotify_auth.encode('ascii'))
            headers = {
                'Authorization': encoded_spotify_auth,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            res = requests.post(
                'https://accounts.spotify.com/api/token', headers=headers, data=data).json()
            if 'access_token' in res:
                spotify_auth = {
                    'spotify_auth': {
                        'access_token': 'Bearer ' + res['access_token'],
                        'expires': (datetime.utcnow() + timedelta(seconds=res['expires_in'])).isoformat(),
                        'refresh_token': res['refresh_token']
                    }
                }
                user = cache.get('user')
                cache.delete('user')
                if update_user(user, spotify_auth).acknowledged:
                    return 'spotify_authenticated=true'
        return 'spotify_authenticated=false'

    def get_user(token: str):
        global env, db_users
        if authenticate_user({'Authorization': token}):
            user = decode_jwt(token)
            spotify_auth = db_users.find_one({'username': user['username']})[
                'spotify_auth']
            if validate_spotify_access_token(spotify_auth):
                headers = {'Authorization': spotify_auth['access_token']}
                res = requests.get(f'{SPOTIFY_API_URI}/me',
                                   headers=headers).json()
                return Response(res, status=status.HTTP_200_OK)
        return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    # def get_playlists(token: str):
    #     global env, db_users
    #     if authenticate_user({'Authorization': token}):
    #         user = decode_jwt(token)
    #         spotify_auth = db_users.find_one({'username': user['username']})[
    #             'spotify_auth']
    #         if validate_spotify_access_token(spotify_auth):
    #             requests.get(f'{SPOTIFY_API_URI}/users/user_id/playlists')
    #             return Response('', status=status.HTTP_200_OK)
    #     return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)
