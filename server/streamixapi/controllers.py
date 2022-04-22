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
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import os

env = environ.Env()
db_users = db_connector.db_handle['Users']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


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
        return Response(f'User \'{user["username"]}\' could not be signed up.', status=status.HTTP_401_UNAUTHORIZED)

    def obtain_jwt(req: dict):
        user = {}
        isAccessToken = 'access_token' in req
        if isAccessToken:
            user = {'Authorization': req['access_token']}
        elif 'username' in req and 'password' in req:
            user = {
                'username': req['username'],
                'password': req['password']
            }
        else:
            # Temporary
            return Response("No correct parameters specified", status=status.HTTP_401_UNAUTHORIZED)
        if authenticate_user(user):
            # ! Throw Exception when there is no token?
            if isAccessToken:
                res = create_jwt(decode_jwt(user['Authorization']))
            else:
                res = create_jwt(user)
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(f'User \'{user["username"]}\' could not be authenticated', status=status.HTTP_401_UNAUTHORIZED)

    def verify_jwt(token: str):
        if authenticate_user({'Authorization': token}):
            env = environ.Env()
            decoded_token = decode_jwt(token)
            formatted_exp = datetime.strftime(datetime.strptime(
                decoded_token['exp'], '%m%d%Y%H%M%S'), '%b %d %Y %I:%M%p')
            return Response('Authentication successful -- Expires ' + formatted_exp, status=status.HTTP_200_OK)
        else:
            return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)


class SpotifyController():
    def __init__(self):
        pass

    def get_auth_code(token: str):
        global env
        if authenticate_user({'Authorization': token}):
            user = decode_jwt(token)
            # Sets user in cache to use later to store access tokens
            cache.set('user', user)
            scope = 'playlist-modify-public playlist-read-private playlist-modify-private'
            res = {
                'client_id': env('SPOTIFY_ID'),
                'response_type': 'code',
                'redirect_uri': 'http://localhost:8000/api/auth/spotify/callback',
                'scope': scope
            }
            return res
        else:
            return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    # !! TODO Logic needs to be placed into a function
    def get_tokens(code: str, grant_type: GRANT_TYPE):
        global env
        if len(code) != 0:
            data = {
                'grant_type': grant_type,
                'code': code,
                'redirect_uri': 'http://localhost:8000/api/auth/spotify/callback'
            }
            spotify_auth_id = env('SPOTIFY_ID') + ':' + env('SPOTIFY_SECRET')
            encoded_spotify_auth = 'Basic '.encode(
                'ascii') + base64.b64encode(spotify_auth_id.encode('ascii'))
            headers = {
                'Authorization': encoded_spotify_auth,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            res = requests.post(
                'https://accounts.spotify.com/api/token', headers=headers, data=data).json()
            if 'access_token' in res:
                user = cache.get('user')
                cache.delete('user')
                spotify_auth = {
                    'spotify_auth': {
                        'access_token': 'Bearer ' + res['access_token'],
                        'expires': (datetime.utcnow() + timedelta(seconds=res['expires_in'])).isoformat(),
                        'refresh_token': res['refresh_token']
                    }
                }
                if update_user(user, spotify_auth).acknowledged:
                    return 'spotify_authenticated=true'
        return 'spotify_authenticated=false'

    def get_user(self, token: str):
        global env, db_users
        if authenticate_user({'Authorization': token}):
            user = decode_jwt(token)
            spotify_auth = get_user_data(user, 'spotify_auth')
            cache.set('user', user)
            if validate_spotify_access_token(spotify_auth):
                headers = {'Authorization': spotify_auth['access_token']}
                # ! Add Exception for when access_token is expired
                res = requests.get(f'{SPOTIFY_API_URI}/me',
                                   headers=headers).json()
                spotify_info = {
                    'spotify_info': {
                        'user_id': res['id']
                    }
                }
                if update_user(user, spotify_info).acknowledged:
                    return Response(res, status=status.HTTP_200_OK)
        return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    def get_playlists(self, token: str):
        global env, db_users
        if authenticate_user({'Authorization': token}):
            # Makes redundant database calls
            if self.get_user(token).status_code == status.HTTP_200_OK:
                user = decode_jwt(token)
                spotify_auth = get_user_data(user, 'spotify_auth')
                if validate_spotify_access_token(spotify_auth):
                    user_id = get_user_data(user, 'spotify_info')['user_id']
                    headers = {'Authorization': spotify_auth['access_token']}
                    res = requests.get(
                        f'{SPOTIFY_API_URI}/users/{user_id}/playlists', headers=headers).json()
                    return Response(res, status=status.HTTP_200_OK)
        return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    def get_playlist_tracks(self, token: str, playlist_id: str):
        global env, db_users
        if authenticate_user({'Authorization': token}):
            # Makes redundant database calls
            if self.get_user(token).status_code == status.HTTP_200_OK:
                user = decode_jwt(token)
                spotify_auth = get_user_data(user, 'spotify_auth')
                if validate_spotify_access_token(spotify_auth):
                    user_id = get_user_data(user, 'spotify_info')['user_id']
                    headers = {'Authorization': spotify_auth['access_token']}
                    res = requests.get(
                        f'{SPOTIFY_API_URI}/playlists/{playlist_id}/tracks', headers=headers).json()
                    return Response(res, status=status.HTTP_200_OK)
        return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)


class YoutubeController():
    def get_auth_code(token: str):
        global env
        if authenticate_user({'Authorization': token}):
            user = decode_jwt(token)
            client_secret = os.path.abspath(os.path.join(
                os.path.dirname(__file__), env('GOOGLE_SECRET_FILE')))
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                client_secret,
                scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
            flow.redirect_uri = 'http://localhost:8000/api/auth/youtube/callback'
            authorization_url, state = flow.authorization_url(
                access_type='offline', include_granted_scopes='true')
            # Sets state in cache to use later to store access tokens
            cache.set('google_state', state)
            # Sets user in cache to use later to store access tokens
            cache.set('user', user)
            return authorization_url
        else:
            return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    def get_tokens(req):
        state = cache.get('google_state')
        client_secret = os.path.abspath(os.path.join(
            os.path.dirname(__file__), env('GOOGLE_SECRET_FILE')))
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret,
            scopes=['https://www.googleapis.com/auth/youtube.force-ssl'], state=state)
        flow.redirect_uri = 'http://localhost:8000/api/auth/youtube/callback'
        authorization_response = req.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)
        youtube_auth = credentials_to_dict(flow.credentials)
        user = cache.get('user')
        cache.delete('user')
        cache.delete('google_state')

        if update_user(user, youtube_auth).acknowledged:
            return 'youtube_authenticated=true'
        return 'youtube_authenticated=false'

    def get_playlists(token):
        global env, db_users
        if authenticate_user({'Authorization': token}):
            user = decode_jwt(token)
            youtube = build_youtube_service(user)
            playlists = json.dumps(
                youtube.playlists().list(part='snippet', mine=True).execute())
            return Response(json.loads(playlists), status=status.HTTP_200_OK)
        return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    def get_playlist_tracks(token: str, playlist_id: str):
        global env, db_users
        if authenticate_user({'Authorization': token}):
            user = decode_jwt(token)
            youtube = build_youtube_service(user)
            playlistItems = json.dumps(
                youtube.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults="50").execute())
            return Response(json.loads(playlistItems), status=status.HTTP_200_OK)
        return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)


# ! No error handling for when json format is wrong
class PlaylistController():
    # ! Be careful of spamming, it will possibly still create a playlist even if an exception is thown
    def create_spotify(spotify_controller: SpotifyController, token, data):
        global env, db_users
        if authenticate_user({'Authorization': token}):
            # Makes redundant database calls
            if spotify_controller.get_user(token).status_code == status.HTTP_200_OK:
                user = decode_jwt(token)
                spotify_auth = get_user_data(user, 'spotify_auth')
                if validate_spotify_access_token(spotify_auth):
                    user_id = get_user_data(user, 'spotify_info')['user_id']
                    playlist_name = data['playlist_name']
                    playlist_name = json.dumps({'name': playlist_name})
                    headers = {'Authorization': spotify_auth['access_token']}
                    cache.set('headers', headers)
                    # ! Validate this response
                    res = requests.post(
                        f'{SPOTIFY_API_URI}/users/{user_id}/playlists', headers=headers, data=playlist_name).json()
                    playlist_id = res['id']
                    track_uris, track_names = search_for_spotify_tracks(
                        data['tracks'])
                    track_uris = json.dumps({'uris': track_uris})
                    # TODO Response has useful data
                    snapshot_id = requests.post(
                        f'{SPOTIFY_API_URI}/playlists/{playlist_id}/tracks', headers=headers, data=track_uris).json()
                    res = {
                        'found_tracks': track_names
                    }
                    return Response(res, status=status.HTTP_200_OK)
        return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)

    def create_youtube(token, data):
        global env, db_users
        if authenticate_user({'Authorization': token}):
            user = decode_jwt(token)
            youtube = build_youtube_service(user)
            cache.set('youtube_service', youtube)
            playlist_body = {
                'snippet': {
                    'title': data['playlist_name']
                }
            }
            # ! Validate this response
            res = youtube.playlists().insert(part='snippet', body=playlist_body).execute()
            playlist_id = res['id']
            video_ids, video_titles = search_for_youtube_tracks(data['tracks'])
            for id in video_ids:
                tracks_body = {
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            "kind": "youtube#video",
                            'videoId': id
                        }
                    }
                }
                # TODO Response has useful data
                res = youtube.playlistItems().insert(part='snippet', body=tracks_body).execute()
            res = {
                'found_tracks': video_titles
            }
            return Response(res, status=status.HTTP_200_OK)
        return Response(f'Authentication unsuccessful', status=status.HTTP_401_UNAUTHORIZED)
