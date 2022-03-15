# Django local settings
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGIN_REDIRECT_URL = '/'

SECRET_KEY = 'PUT YOUR SECRET HERE'

ALLOWED_HOSTS = [
    "korn.com",
    "metalica-caca.com"
]

ADMINS = (
    ('Janathan Davis', 'chanteur-de@korn.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'zython.sql',                      # Or path to database file if using sqlite3.
    }
}


MEDIA_URL = '/medias/'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
INTERNAL_IPS = ('127.0.0.1',)
INTERCEPT_REDIRECTS = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '%s/cache' % BASE_DIR,
    }
}


TWITTER_CONSUMER_KEY         = ''
TWITTER_CONSUMER_SECRET      = ''
FACEBOOK_APP_ID              = ''
FACEBOOK_API_SECRET          = ''
GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''
