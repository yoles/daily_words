# Replace name in container by current project name
sed -i "/container_name:/c\ \ \ \ container_name: $1" local.yml

# Build container and create django projects.
make build && make permissions

echo "# Apps
logs/
path_2_test.py
backup.sql" >> .gitignore

# Find Word 'x' and change (c) whole line by the new content.
sed -i '/SECRET_KEY/c\SECRET_KEY = env("SECRET_KEY")' ./core/settings/base.py
sed -i '/DEBUG/c\DEBUG = env("DEBUG")' ./core/settings/base.py

# Rename project_name/ folder into core/ in base.py
sed -i "s/$1\.urls/core\.settings\.urls/g" ./core/settings/base.py
sed -i "s/$1\.wsgi/core\.wsgi/g" ./core/settings/base.py

# Remove import Path
sed -i '13d' ./core/settings/base.py

#Insert imports at line 12 (os, sys, environ, logger) 
sed -i '12 a import os\nimport sys\nimport environ' ./core/settings/base.py

# Change BASE_DIR to follow new architecture
sed -i '/BASE_DIR =/c\BASE_DIR = dir_name(dir_name(dir_name(os.path.abspath(__file__))))' ./core/settings/base.py

# Load env 
sed -i '17 a env = environ.Env()\ndir_name = os.path.dirname' ./core/settings/base.py
sed -i '20 a sys.path.insert(0, os.path.join(BASE_DIR, "apps"))\nenviron.Env.read_env(os.path.join(BASE_DIR, ".envs", "local", ".env"))' ./core/settings/base.py


# Insert Logger Setup 
echo '
dir_name = os.path.join(BASE_DIR, "logs")
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} - in {filename} l.{lineno} {message}", # noqa
            "datefmt": "%d/%m/%Y %H:%M:%S",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(dir_name, "app.log"),
            "formatter": "verbose"
        },
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}' >> ./core/settings/base.py

# Add Email Settings
echo 'EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"' >> ./core/settings/prod.py
echo 'EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"' >> ./core/settings/prod.py
echo 'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
' >> ./core/settings/dev.py

# Remove SQLite DB
sed -i '82,87d' ./core/settings/base.py

# Add Postgresql as DB
echo 'if sys.argv[1] == "test":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("POSTGRES_NAME"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
            "HOST": env("POSTGRES_HOST"),
            "PORT": 5432
        }
    }
' >> ./core/settings/base.py

make permissions && make up