from django.urls import path, re_path
from streamixapi import views

urlpatterns = [
    # Auth routes
    re_path(r'auth\/login\/?$', views.AuthUser.as_view()),
    re_path(r'auth\/signup\/?$', views.SignupUser.as_view()),
    # JWT routes
    re_path(r'auth\/token\/?$', views.TokenObtain.as_view()),
    re_path(r'auth\/token\/verify\/?$', views.TokenVerify.as_view()),
    # Spotify auth routes
    re_path(r'auth\/spotify\/?$', views.SpotifyAuth.as_view()),
    re_path(r'auth\/spotify\/callback\/$', views.SpotifyCallback.as_view()),
    # Spotify CRUD routes
    re_path(r'spotify\/user\/$', views.SpotifyUser.as_view()),
    re_path(r'spotify\/playlists\/$', views.SpotifyPlaylists.as_view()),
    re_path(r'spotify\/tracks\/(?P<playlist_id>\w+)\/$',
            views.SpotifyTracks.as_view()),
    # Youtube auth routes
    re_path(r'auth\/youtube\/?$', views.YoutubeAuth.as_view()),
    re_path(r'auth\/youtube\/callback\/$', views.YoutubeCallback.as_view()),
    re_path(r'youtube\/tracks\/$', views.YoutubeTracks.as_view()),
    # Youtube CRUD routes
    re_path(r'youtube\/playlists\/$', views.YoutubePlaylists.as_view()),
    # Migration route
    re_path(r'playlist\/create\/(?P<to_platform>\w+)\/$',   # ! Runtime error when no trailing slash
            views.PlaylistCreate.as_view()),
]
