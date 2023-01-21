from .base import *

import environ
import os

env = environ.Env()

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = False

SECRET_KEY = env("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("MYSQL_NAME"),
        'USER': env("MYSQL_USER"),
        'PASSWORD': env("MYSQL_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_USE_SSL = True

try:
    from .local import *
except ImportError:
    pass
