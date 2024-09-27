"""
Django settings for highlightme project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import json
import logging
import os
from pathlib import Path
import environ
import colorlog
from decouple import config

from highlightme.filters import IgnoreMtimeFilter

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = config('ENVIRONMENT', default='development')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#g&@3l@$#%i&5wl+=)1irsq=g&*vo9dwio)9d6g058vv^0)0ny'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #TODO : set false for production use

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'admin_app',
    'discordbot',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'highlightme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'highlightme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('POSTGRES_DB'),
            'USER': config('PG_USER'),
            'PASSWORD': config('PG_PASSWORD'),
            'HOST': config('PG_HOST'),
            'PORT': config('PG_PORT', default='5432'),
        }
    }
    BASE_URL = 'https://highlightmebackend-production.up.railway.app'
    BASE_URL_FRONT = 'https://raid-highlights.netlify.app'
else:
    BASE_URL = 'http://localhost:8000'
    BASE_URL_FRONT = 'http://localhost:4200'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

WARCRAFTLOGS_OAUTH = env.json('WARCRAFTLOGS_OAUTH', {})


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'colored': {
            'format': '{log_color}{levelname} {asctime} {module} {message}',
            'style': '{',
            '()': 'colorlog.ColoredFormatter',
            'log_colors': {
                'DEBUG': 'yellow',
                'INFO': 'blue',
                'WARNING': 'red',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'filters': {
        'ignore_mtime': {
            '()': IgnoreMtimeFilter,
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'filters': ['ignore_mtime'],
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO' if ENVIRONMENT == 'production' else 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO' if ENVIRONMENT == 'production' else 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['console'],
            'level': 'INFO' if ENVIRONMENT == 'production' else 'DEBUG',
            'propagate': False,
        },
        'report': {
            'handlers': ['console'],
            'level': 'INFO' if ENVIRONMENT == 'production' else 'DEBUG',
            'propagate': False,
        },
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Display a big DEBUG MODE message if debug is enabled
if DEBUG:
    logging.getLogger('django').debug("\n" + "#"*50 + "\n" + "DEBUG MODE" + "\n" + "#"*50 + "\n")

