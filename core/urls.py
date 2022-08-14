from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('', lambda request: render(request, 'core/home.html'), name="home"),
    path(settings.ADMIN_URL, admin.site.urls),
]
