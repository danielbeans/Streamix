from django.urls import path, re_path

from streamixapi import views

urlpatterns = [
    re_path(r'auth/login\/?', views.AuthUser.as_view()),
    re_path(r'auth/signup\/?', views.SignupUser.as_view()),
]
