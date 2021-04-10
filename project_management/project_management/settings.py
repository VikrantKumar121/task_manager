"""
Django settings for project_management project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from .config import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#khuy7o@i4rv2s+ghy7t+&i%n5&eq0)gi^p%d$yadk5dqqyd1k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_mongoengine',
    'organization',
    'user',
    'project',
    'task',
    'mongo_auth',
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

ROOT_URLCONF = 'project_management.urls'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'base.permissions.permissions.AuthenticatedOnly',
        'base.permissions.permissions.IsTokenValid'
         ]}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project_management.wsgi.application'

# allowscross platform requests from any platform
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL=True

# allowscross platform requests from these platform
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:8000',
#     'http://localhost:3000',
#     'http://127.0.0.1:3000'
# ]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

import mongoengine
# DATABASES = {
#     'default': {
#     'ENGINE': '',
#     'NAME':'',
#     },
# }
MONGO_USER = DB_USER
MONGO_PASS = DB_PASSWORD
MONGO_HOST = DB_HOST
MONGO_NAME = DB_NAME
MONGO_PORT = DB_PORT
MONGO_DATABASE_HOST = \
'mongodb://%s:%s@%s/%s' \
% (MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_NAME)
# print(MONGO_DATABASE_HOST)
# mongoengine.connect(MONGO_NAME)
mongoengine.connect(MONGO_NAME, host= MONGO_DATABASE_HOST)
# import mongoengine
# mongoengine.connect(db='pm', host='localhost')

# AUTHENTICATION_BACKENDS = ('mongoengine.django.auth.MongoEngineBackend', )

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


"""
CUSTOM USER JWT TOKEN
"""
from datetime import timedelta

# Minimal settings (all mandatory)
MANGO_JWT_SETTINGS = {
    "db_host": DB_HOST, # Use srv host if connecting with MongoDB Atlas Cluster
    "db_port": DB_PORT, # Don't include this field if connecting with MongoDB Atlas Cluster
    "db_user": DB_USER,
    "auth_collection": DB_COLLECTION,
    "db_pass": DB_PASSWORD,
    "db_name": DB_NAME,
    "secondary_username_field": "email",
    "fields": ("email", "password")
    # "auth_collection": "User"
}


'''Email BAckend '''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'team@namasys.co'
EMAIL_HOST_PASSWORD = 'remht997#$'

# Or use Advanced Settings (including optional settings)
# MANGO_JWT_SETTINGS = {
#     "db_host": "some_db_host",
#     "db_port": "some_db_port",
#     "db_name": "for_example_auth_db",
#     "db_user": "username",
#     "db_pass": "password",
#     "auth_collection": "name_your_auth_collection", # default is "user_profile"
#     "fields": ("email", "password"), # default
#     "jwt_secret": "secret", # default
#     "jwt_life": 7, # default (in days)
#     "secondary_username_field": "email" # default is None
# }

# CELERY CONF
BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'