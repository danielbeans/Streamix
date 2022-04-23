from os import environ
from pymongo import MongoClient
import environ
import enum
import jwt
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

env = environ.Env()

SPOTIFY_API_URI = 'https://api.spotify.com/v1'


class db_connector():
    global env
    client = MongoClient(
        f'mongodb+srv://{env("DATABASE_USER")}:{env("DATABASE_PASS")}@streamix.zfoco.mongodb.net/{env("DATABASE_NAME")}?retryWrites=true&w=majority')
    db_handle = client['Streamix']


db_users = db_connector.db_handle['Users']


class GRANT_TYPE(enum.Enum):
    authorization_code = 1
    refresh_token = 2


def decode_jwt(token: str):
    global env
    return jwt.decode(token, env('SECRET_KEY'), algorithms=["HS256"])


def update_user(user: dict, info: dict):
    global db_users
    return db_users.update_one({'username': user['username']}, {'$set': info})


def get_user_data(user: dict, data: str = ''):
    global db_users
    temp = db_users.find_one({'username': user['username']})
    return temp[data] if data in temp else temp


def credentials_to_dict(credentials):
    youtube_auth = {
        'youtube_auth': {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
    }
    return youtube_auth


# Creates a service object to use to query YouTube API
def build_youtube_service(user: dict):
    youtube_auth = get_user_data(user, 'youtube_auth')
    credentials = google.oauth2.credentials.Credentials(
        youtube_auth['token'],
        refresh_token=youtube_auth['refresh_token'],
        token_uri=youtube_auth['token_uri'],
        client_id=youtube_auth['client_id'],
        client_secret=youtube_auth['client_secret'],
        scopes=youtube_auth['scopes']
    )
    update_user(user, credentials_to_dict(credentials))
    return build('youtube', 'v3', credentials=credentials)
