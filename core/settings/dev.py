from core.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-m07h7jjcg2ilc9+33s@pd9_zuc_((1j*q@wvw0@__7c_ig8mzx"
)


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

