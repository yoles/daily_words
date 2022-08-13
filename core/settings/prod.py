from core.settings.base import *

DEBUG = False

ALLOWED_HOSTS = []
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-m07h7jjcg2ilc9+33s@pd9_zuc_((1j*q@wvw0@__7c_ig8mzx"
)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
