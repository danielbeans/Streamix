from django.urls import path, re_path
from streamixapi import views

urlpatterns = [
    # Auth routes
    re_path(r'auth\/login\/?$', views.AuthUser.as_view()),
    re_path(r'auth\/signup\/?$', views.SignupUser.as_view()),
    # JWT routes
    re_path(r'auth\/token\/?$', views.TokenObtain.as_view()),
    re_path(r'auth\/token\/verify\/?$', views.TokenVerify.as_view()),
]
