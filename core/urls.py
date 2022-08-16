from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

urlpatterns = [
    path('', lambda request: render(request, 'core/home.html'), name="home"),
    path('user/', include("apps.users.urls"), name="users"),
    path(settings.ADMIN_URL, admin.site.urls),
]
