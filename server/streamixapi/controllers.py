from rest_framework import status
from rest_framework.response import Response
from .services import authenticate_user, signup_user


class AuthController():
    def login(req: dict):
        user = {
            'username': req['username'],
            'password': req['password']
        }
        if authenticate_user(user):
            return Response(f'User \'{user["username"]}\' successfully authenticated', status=status.HTTP_200_OK)
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
            return Response(f'User \'{user["username"]}\' successfully signed up', status=status.HTTP_201_CREATED)
        else:
            return Response(f'User \'{user["username"]}\' could not be signed up', status=status.HTTP_401_UNAUTHORIZED)
