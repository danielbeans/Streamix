from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import GRANT_TYPE
from .controllers import *
from .services import validate_jwt_syntax
from pymongo.errors import DuplicateKeyError, InvalidName
from jwt.exceptions import DecodeError
from django.shortcuts import redirect
from urllib import parse
from django.core.cache import cache


class AuthUser(APIView):
    def post(self, request):
        req_data = request.data
        try:
            res = AuthController.login(req_data)
        except KeyError as e:
            return Response(f'Key {str(e)} not found', status=status.HTTP_400_BAD_REQUEST)
        except InvalidName as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return res


class SignupUser(APIView):
    def post(self, request):
        req_data = request.data
        try:
            res = AuthController.signup(req_data)
        except KeyError as e:
            return Response(f'Key {str(e)} not found', status=status.HTTP_400_BAD_REQUEST)
        except DuplicateKeyError as e:
            return Response('User already exists', status=status.HTTP_400_BAD_REQUEST)
        return res


class TokenObtain(APIView):
    def post(self, request):
        req_data = request.data
        res = AuthController.obtain_jwt(req_data)
        return res


class TokenVerify(APIView):
    def get(self, request):
        try:
            return AuthController.verify_jwt(validate_jwt_syntax(request))
        except DecodeError:
            return Response(f'JWT Invalid', status=status.HTTP_401_UNAUTHORIZED)


class SpotifyAuth(APIView):
    def get(self, request):
        try:
            res = SpotifyController.get_auth_code(
                validate_jwt_syntax(request))
            return redirect('https://accounts.spotify.com/authorize?' + parse.urlencode(res))
        except DecodeError:
            return Response(f'JWT Invalid', status=status.HTTP_401_UNAUTHORIZED)


class SpotifyCallback(APIView):
    def get(self, request):
        try:
            auth_code = request.GET.get('code', '')
            res = SpotifyController.get_tokens(
                auth_code, GRANT_TYPE.authorization_code.name)
            return redirect('http://localhost:3000/dashboard?' + res)
        except:
            return redirect('http://localhost:3000/dashboard?error=1')


# !! TODO Add exceptions
class SpotifyUser(APIView):
    def get(self, request):
        return SpotifyController.get_user(validate_jwt_syntax(request))


class SpotifyPlaylists(APIView):
    def get(self, request):
        return SpotifyController.get_playlists(validate_jwt_syntax(request))
