from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-i!hit*$g9ypx_^hch#=^m%+9b1wqfqkja=vz3&zp0+zb-=3+3g"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'the9jafoodblog@gmail.com'
EMAIL_HOST_PASSWORD = 'sftvkflzfhqobuqg'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
EMAIL_PORT = 465
EMAIL_USE_SSL = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

try:
    from .local import *
except ImportError:
    pass
