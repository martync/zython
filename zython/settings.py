# -*- coding: utf-8 -*-

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
sys.path.insert(0, os.path.join(BASE_DIR, "apps-ext"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$6o99)#9hdsjal0+oq=7f10*qw$#)d7z!ajpwo-)(#-c6zcq7w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    "zython.me",
]

DEFAULT_FROM_EMAIL = 'ToBeer <noreply@zython.me>'

SITE_ID = 1

AUTH_USER_MODEL = "auth.User"

LOGIN_REDIRECT_URL = '/recipe/my-recipes/'
ACCOUNT_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL

TEST_RUNNER = "zython.test_runner.ZythonTestRunner"


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',

    "compressor",
    'pagination',
    'account',
    'accounts',
    'calculator',
    'django_social_share',
    'public',
    'brew',
    'units',
    'social_auth',
    'avatar',
    'stocks',
    'guardian',
    'crispy_forms',
    'fm'
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "account.middleware.TimezoneMiddleware",
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'units.context_processors.user_units',
    'units.context_processors.unit_menu',
    'account.context_processors.account',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',

)

ROOT_URLCONF = 'zython.urls'
LOGIN_URL = '/account/login/'
WSGI_APPLICATION = 'zython.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),

)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'en'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

LANGUAGES = (
    ('en', u'English'),
    ('fr', u'Français')
)

USE_I18N = True
USE_L10N = True
USE_TZ = False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/medias/static/'
STATIC_ROOT = '%s/medias/static/' % BASE_DIR
MEDIA_ROOT = '%s/medias/' % BASE_DIR

# Third party settings
ANONYMOUS_USER_ID = -1
ACCOUNT_ACTIVATION_DAYS = 7
AVATAR_ALLOWED_FILE_EXTS = ('.jpg', '.png', '.jpeg', '.gif')
AVATAR_STORAGE_DIR = "medias/avatars/"
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False

SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/account/new-social-auth-user/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/account/new-social-auth-user/'

LOGIN_ERROR_URL = LOGIN_URL

try:
    from local_settings import *
except ImportError:
    pass
