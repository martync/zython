# -*- coding: utf-8 -*-

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

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
    "127.0.0.1"
]

DEFAULT_FROM_EMAIL = 'ToBeer <noreply@zython.me>'

SITE_ID = 1

WSGI_APPLICATION = 'zython.wsgi.application'

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
    'django_comments',

    'account',
    'accounts',
    'calculator',
    'django_social_share',
    'public',
    'brew',
    'units',
    'dj_pagination',
    'stocks',
    'guardian',
    'crispy_forms',
    'fm'
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.TimezoneMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',

)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
ROOT_URLCONF = 'zython.urls'
LOGIN_URL = '/account/login/'
WSGI_APPLICATION = 'zython.wsgi.application'

EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
        "context_processors": (
                "django.contrib.auth.context_processors.auth",
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # "django.core.context_processors.i18n",
                # "django.core.context_processors.media",
                # "django.core.context_processors.static",
                # "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                'units.context_processors.user_units',
                'units.context_processors.unit_menu',
                'account.context_processors.account',
                'django.template.context_processors.request'
            )
        },
    },
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

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

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_ROOT = '%s/medias/' % BASE_DIR

# Third party settings
ANONYMOUS_USER_ID = 1
ACCOUNT_ACTIVATION_DAYS = 7
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False
ACCOUNT_EMAIL_UNIQUE = False

LOGIN_ERROR_URL = LOGIN_URL

try:
    from local_settings import *
except ImportError:
    pass
