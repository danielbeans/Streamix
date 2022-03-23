from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .controllers import AuthController
from pymongo.errors import DuplicateKeyError, InvalidName
from jwt.exceptions import DecodeError


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
        PREFIX = 'Bearer '
        authHeader: str = request.headers['Authorization']
        try:
            if not authHeader.startswith(PREFIX):
                raise DecodeError()
            res = AuthController.verify_jwt(authHeader[len(PREFIX):])
        except DecodeError:
            return Response(f'JWT Invalid', status=status.HTTP_401_UNAUTHORIZED)
        return res
