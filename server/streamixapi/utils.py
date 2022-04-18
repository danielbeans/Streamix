from os import environ
from pymongo import MongoClient
import environ
import enum
import jwt

env = environ.Env()

SPOTIFY_API_URI = 'https://api.spotify.com/v1'


class db_connector():
    global env
    client = MongoClient(
        f'mongodb+srv://{env("DATABASE_USER")}:{env("DATABASE_PASS")}@streamix.zfoco.mongodb.net/{env("DATABASE_NAME")}?retryWrites=true&w=majority')
    db_handle = client['Streamix']


class GRANT_TYPE(enum.Enum):
    authorization_code = 1
    refresh_token = 2


def decode_jwt(token: str):
    global env
    return jwt.decode(token, env('SECRET_KEY'), algorithms=["HS256"])
