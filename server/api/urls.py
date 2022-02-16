from django.contrib import admin
from django.urls import path, include

from streamixapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('streamixapi.urls')),
]
