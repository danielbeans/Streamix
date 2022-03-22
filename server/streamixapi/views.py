from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .controllers import AuthController
from pymongo.errors import DuplicateKeyError, InvalidName


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
