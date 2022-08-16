from core.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-m07h7jjcg2ilc9+33s@pd9_zuc_((1j*q@wvw0@__7c_ig8mzx"
)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

