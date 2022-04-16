from rest_framework import status
from rest_framework.response import Response
from .services import *
import jwt
import environ 
import requests
import base64

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
            return Response('Authentication successful', status=status.HTTP_200_OK)
        else:
            return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    def get_spotify_auth_code(token: str):
        env = environ.Env()
        if True: #authenticate_user({'Authorization': token}):
            res = {
                'client_id': env('SPOTIFY_ID'),
                'response_type': 'code',
                'redirect_uri': 'http://localhost:8000/api/auth/spotify/callback'
            }
            return res
        else:
            return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)
    
    def get_spotify_tokens(code: str):
        env = environ.Env()

        if len(code) != 0:
            data = {
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': 'http://localhost:8000/api/auth/spotify/callback'
            }
            spotify_auth = env('SPOTIFY_ID') + ':' + env('SPOTIFY_SECRET') 
            encoded_spotify_auth  = 'Basic '.encode('ascii') + base64.b64encode(spotify_auth.encode('ascii'))
            headers = {
                'Authorization': encoded_spotify_auth,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
            # print(res.text)