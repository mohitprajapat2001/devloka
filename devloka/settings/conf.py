from os.path import join
from pathlib import Path

from dotenv import dotenv_values
from utils.constants import EmailConfig, Settings

env = dotenv_values(".env")

# BASE Directory Path
BASE_DIR = Path(__file__).resolve().parent.parent
APPEND_SLASH = True

# Auth User Model
AUTH_USER_MODEL = Settings.AUTH_USER_MODEL

# Project Secret Key
SECRET_KEY = env.get("SECRET_KEY")

ROOT_URLCONF = Settings.ROOT_URLCONF

LANGUAGE_CODE = Settings.LANGUAGE_CODE

USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("hi", "Hindi"),
]
LOCALE_PATHS = [
    join(BASE_DIR, "locale"),
]

TIME_ZONE = Settings.TIME_ZONE

USE_I18N = Settings.USE_I18N


USE_TZ = Settings.USE_TZ
DEFAULT_AUTO_FIELD = Settings.DEFAULT_AUTO_FIELD

# Web Server Gateway Interface
WSGI_APPLICATION = Settings.WSGI_APPLICATION
ASGI_APPLICATION = Settings.ASGI_APPLICATION

# Email Configuration
EMAIL_BACKEND = EmailConfig.EMAIL_BACKEND
EMAIL_HOST = EmailConfig.EMAIL_HOST
EMAIL_USE_SSL = True  # use port 465
EMAIL_USE_TLS = False  # use port 587
EMAIL_PORT = EmailConfig.PORT_465 if EMAIL_USE_SSL else EmailConfig.PORT_587
EMAIL_HOST_USER = env.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.get("EMAIL_HOST_PASSWORD")


# Superuser Configuration
ADMIN_USER = env.get("ADMIN_USER")
ADMIN_PASSWORD = env.get("ADMIN_PASSWORD")
ADMIN_EMAIL = env.get("ADMIN_EMAIL")

# FRONTEND URL
FRONTEND_URL = env.get("FRONTEND_URL")
