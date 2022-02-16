from django.urls import path

from streamixapi import views

urlpatterns = [
    path('', views.UserView.as_view()),
]
